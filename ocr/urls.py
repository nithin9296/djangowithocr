from django.urls import path, include
from . import views 
from .views import ChartData, HomeView, get_data
from django.views.generic import TemplateView

urlpatterns = [
    
    path('', HomeView.as_view(), name='home' ),
    path('trialbalance2017_list/', views.trialbalance2017_list, name='trialbalance2017_list' ),
    
    path('delete/', views.delete, name='delete' ),
    path('import/', views.import_data, name='import' ),
    path('api/data/', get_data, name='api-data'),
    path('api/chart/data/', ChartData.as_view()),
    path('handson_view/', views.handson_table, name='handson_view'),
    path('trialbalance2017/delete', views.trialbalance2017Delete.as_view(), name='trialbalance2017_delete'),
    ]