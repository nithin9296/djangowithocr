from elasticsearch.client import IndicesClient
from django.conf import settings
from django.core.management.base import BaseCommand
from ocr.models import trialbalance2017
class Command(BaseCommand):
    def handle(self, *args, **options):
        self.recreate_index()
    def recreate_index(self):
        indices_client = IndicesClient(client=settings.ES_CLIENT)
        index_name = trialbalance2017._meta.es_index_name
        if indices_client.exists(index_name):
            indices_client.delete(index=index_name)
        indices_client.create(index=index_name)
        indices_client.put_mapping(
            doc_type=trialbalance2017._meta.es_type_name,
            body=trialbalance2017._meta.es_mapping,
            index=index_name
        )