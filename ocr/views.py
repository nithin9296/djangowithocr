from django.shortcuts import render, redirect

# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, Http404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, CreateView, DeleteView, View
import _csv
import django_excel as excel
import pyexcel
from pyexcel  import get_sheet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model


from .forms import DocumentForm
from .forms import trialbalanceform
from django.http import HttpResponse
import csv
import ipdb
import tempfile
from Cython.Compiler.Buffer import context
#from .read_image import read_image_from_file
from .models import trialbalance2017
import json
from urllib.parse import urlencode
from copy import deepcopy
from django.conf import settings
from django.db.models import Count
from django.views.generic.base import TemplateView
from lib2to3.pgen2.token import MINUS
from django.db.models import Sum, F
from ocr.models import trialbalance2017




try:
        import Image
except ImportError:
        from PIL import Image
import pytesseract

global i
i = 0





def import_data(request):
    if request.method == "POST":
        form = trialbalanceform(request.POST,
                                request.FILES)        
        if form.is_valid():
            request.FILES['trialbalancefile'].save_book_to_database(
                models=[trialbalance2017],
                initializers=[None],
                mapdicts=[
                    ['description', 'debit', 'credit', 'slug']]
            )
            return redirect('ocr:handson_view')
        else:
            return HttpResponseBadRequest()
    else:
        form = trialbalanceform()
    return render(
        request,
        'prelim_analysis.html',
        {'form': form})
    


    
def trialbalance2017_list(request):
    current_asset = (trialbalance2017.objects
                        .filter(description__in=['cash', 'debtors', 'inventory'])
                        .aggregate(
                            current_asset=Sum('debit')
                            )['current_asset']
                    )
    
    current_liab = (trialbalance2017.objects
                        .filter(description__in=['creditors', 'loans'])
                        .aggregate(
                            current_liab=Sum('credit')
                            )['current_liab']
                    )
    
    #current_asset = trialbalance2017.objects.filter(id='10050').aggregate(Sum(F'debit'))
    
    #current_assets = trialbalance2017.objects.filter(id='10050').aggregate(Sum(F('debit'))) - trialbalance2017.objects.filter(id='10049').aggregate(Sum(F('credit')))
    
    #current_liab = trialbalance2017.objects.filter(id='10054').aggregate(Sum(F'credit'))
    #current_assets = current_asset.debit - current_liab.credit
    
    #current_assets = F(current_asset.debit__sum) - F(current_liab.credit__sum)
    
    current_assets = current_asset - current_liab
    current_ratio = current_asset / current_liab
    #queryset = trialbalance2017.objects.all()
    context = {
        "current_assets": current_assets,
        "current_ratio" : current_ratio,
        #"current_assets": current_assets,
        "title": "current_assets"
    }

    return render(request, "trialbalance2017_list.html", context)






User = get_user_model()

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts.html', {"customers": 10})


def get_data(request, *args, **kwargs):
    
    current_asset = (trialbalance2017.objects
                        .filter(description__in=['cash', 'debtors', 'inventory'])
                        .aggregate(
                            current_asset=Sum('debit')
                            )['current_asset']
                    )
    
    current_liab = (trialbalance2017.objects
                        .filter(description__in=['creditors', 'loans'])
                        .aggregate(
                            current_liab=Sum('credit')
                            )['current_liab']
                    )
    current_assets = current_asset - current_liab
    
    data = {
        "sales" : 100,
        "customers": 10,        
    }

    return JsonResponse(data)

class ChartData(APIView):
   
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs_count = trialbalance2017.objects.all().count()
        
        current_asset = (trialbalance2017.objects
                        .filter(description__in=['cash', 'debtors', 'inventory'])
                        .aggregate(
                            current_asset=Sum('debit')
                            )['current_asset']
                    )
    
        current_liab = (trialbalance2017.objects
                        .filter(description__in=['creditors', 'loans'])
                        .aggregate(
                            current_liab=Sum('credit')
                            )['current_liab']
                    )
        current_assets = current_asset - current_liab 
        labels = ["Users", "current_assets", "current_asset", "current_liab", ]
        default_items = [qs_count, current_assets, current_asset, current_liab,]
        
        
        data = {
                "labels" : labels,
                "default" : default_items,
        } 
        return Response(data)


def delete(request):
    q = trialbalance2017.objects.all()
    q.delete()
    return HttpResponse('deleted')


class trialbalance2017Delete(DeleteView):
    model = trialbalance2017
    success_url = reverse_lazy('trialbalance2017')






def handson_table(request):
    return excel.make_response_from_tables(
        [trialbalance2017], 'handsontable.html')


def embed_handson_table(request):
    """
    Renders two table in a handsontable
    """
    content = excel.pe.save_book_as(
        models=[trialbalance2017],
        dest_file_type='handsontable.html',
        dest_embed=True)
    content.seek(0)
    return render(
        request,
        'custom-handson-table.html',
        {
            'handsontable_content': content.read()
        })


def embed_handson_table_from_a_single_table(request):
    """
    Renders one table in a handsontable
    """
    content = excel.pe.save_as(
        model=trialbalance2017,
        dest_file_type='handsontable.html',
        dest_embed=True)
    content.seek(0)
    return render(
        request,
        'custom-handson-table.html',
        {
            'handsontable_content': content.read()
        })




#===============================================================================
# def list(request):
#     global i
#     # Handle file upload
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             newdoc = Document(docfile=request.FILES['docfile'])
#             newdoc.save()      
#             
#             
#             i += 1 
#             # import ipdb;ipdb.set_trace()
#             d = Document.objects.get(id=i)
#             
#             #print d.docfile
#             k=pytesseract.image_to_string(Image.open(d.docfile))
#             #print k
#             handle = open('data.txt', 'a+')
#             handle.write(k)
#             handle.close()
# 
#             txt_file = r"data.txt"
#             csv_file = r'mycsv.csv'
# 
#             in_txt = csv.reader(open(txt_file, "r"), delimiter = ' ')
#             out_csv = csv.writer(open(csv_file, 'w', encoding='utf-8'))
# 
#             out_csv.writerows(in_txt)
# 
#             # Redirect to the document list after POST
#             return HttpResponseRedirect(reverse('ocr:list'))
#     else:
#         form = DocumentForm()  # A empty, unbound form
# 
#     # Load documents for the list page
#     documents = Document.objects.all()
# 
#     # Render list page with the documents and the form
#     return render(request, 
#         'list.html',
#         {'documents': documents, 'form': form},
#         context
#     )
#===============================================================================