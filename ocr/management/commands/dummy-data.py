from django.core.management.base import BaseCommand
from ocr.models import trialbalance2017
from model_mommy import mommy
import random
import names
from elasticsearch.helpers import bulk


class Command(BaseCommand):
    def add_arguments(self,parser):
        parser.add_argument('count', nargs=1, type=int)
    
    def handle(self, *args, **options):
        print ('lala')
        self.make_trialbalance2017(options)
        self.recreate_index()
        self.push_db_to_index()
    
    def make_trialbalance2017(self, options):
        self.trialbalance2017 = []
        for __ in range(options.get('count')[0]):
            tria = mommy.prepare(
                trialbalance2017,
                description=names.get_first_name(),
                debit=random.randint(2000,5000),
                credit=random.randint(3000,4000),
            )
            self.trialbalance2017.append(tria)
        trialbalance2017.objects.bulk_create(self.trialbalance2017) 
        
    def push_db_to_index(self):
        data = [
            self.convert_for_bulk(s, 'create') for t in trialbalance2017.objects.all()
        ]
        bulk(client=settings.ES_CLIENT, actions=data, stats_only=True)
    def convert_for_bulk(self, django_object, action=None):
        data = django_object.es_repr()
        metadata = {
            '_op_type': action,
            "_index": django_object._meta.es_index_name,
            "_type": django_object._meta.es_type_name,
        }
        data.update(**metadata)
        return data