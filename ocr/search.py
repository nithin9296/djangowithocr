from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date
from IPython.core.release import description
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from .import models

connections.create_connection()

class trialbalance2017Index(DocType):
    description = Text()
    debit = int()
    credit = int()
    
    
    class Meta:
        index = 'trialbalance2017-index'
        


def bulk_indexing():
    trialbalance2017Index.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.trialbalance2017.objects.all().iterator()))
    
    
