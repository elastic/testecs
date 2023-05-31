from datetime import datetime
from elasticsearch import Elasticsearch

settings = {
    'settings': {
        'index.mapping.total_fields.limit': 10000
    },
    "mappings": {
        "dynamic_templates": ""
    }
}


def client(host, user, password):
    es = Elasticsearch(hosts=host, http_auth=(
        user, password), verify_certs=False)
    return es


def create_index(es, index_name, template):
    es.options(ignore_status=[400, 404]).indices.delete(index=index_name)
    settings['mappings']['dynamic_templates'] = template
    es.indices.create(index=index_name, body=settings)


def index_document(es, index_name, document):
    es.index(index=index_name, body=document)


def get_mappings(es, index_name):
    return es.indices.get_mapping(index=index_name)
