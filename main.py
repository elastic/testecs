from dynamic_mapping import process_dynamic_mapping
from ecs import process_ecs
import elastic
from mappings import process_mappings
import os

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Dynamic mapping Settings
dm_url = 'https://raw.githubusercontent.com/elastic/elasticsearch/887e5f3d06fb5fa7bd5b56c11378cc50e4cc6d6e/x-pack/plugin/core/src/main/resources/ecs-dynamic-mappings.json'
# ECS Settings
ecs_url = 'https://raw.githubusercontent.com/elastic/ecs/main/generated/ecs/ecs_flat.yml'

files = ['field_mappings.json', 'dynamic_template.json',
         'ecs_generated.json', 'ecs_flat.json', 'results.json']
# Elasticsearch Settings
es_host = "https://localhost:9200"
es_index = "testindex5"
es_user = "elastic"
es_pass = "changeme"

matched_fields = 0
missmatched_fields = 0


def cleanup_files(files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)


if __name__ == "__main__":
    print(f"Deleting old files: {files}")
    cleanup_files(files)

    dm = process_dynamic_mapping(dm_url)
    ecs_generated, ecs_flat = process_ecs(ecs_url)

    print(f"Connecting to: {es_host}")
    es = elastic.client(es_host, es_user, es_pass)

    print(f"Creating index: {es_index}")
    elastic.create_index(es, es_index, dm)

    print(f"Adding document to index: {es_index}")
    elastic.index_document(es, es_index, ecs_generated)

    print(f"Retrieves mapping from index: {es_index}")
    elastic_mappings = elastic.get_mappings(es, es_index)

    mapping_compare = process_mappings(elastic_mappings, es_index)

    print("Comparing ECS definition with Elasticsearch mapping")
    print(f"Deleting temp files: {files}")
    cleanup_files(files)

    for key, value in mapping_compare.items():
        if key in ecs_flat and ecs_flat[key] == value:
            matched_fields += 1
            continue
        else:
            missmatched_fields += 1
            print(
                f"The key-value pair ({key}: {value}) does not exist. Field type should be: {ecs_flat[key]}")

    print(
        f"Tested {len(mapping_compare)}/{matched_fields + missmatched_fields} Fields")
    print(f"Matched fields: {matched_fields}")
    print(f"Missmatched fields: {missmatched_fields}")
