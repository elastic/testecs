from dynamic_mapping import process_dynamic_mapping
from ecs import process_ecs
import elastic
from mappings import process_mappings
import os

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Dynamic ECS mappings
dm_ecs_url = 'https://raw.githubusercontent.com/elastic/elasticsearch/275afa7708ccb7ac206ad935ce63cc26c7c9aa67/x-pack/plugin/core/src/main/resources/ecs-dynamic-mappings.json'

# ECS Settings
ecs_url = 'https://raw.githubusercontent.com/elastic/ecs/main/generated/ecs/ecs_flat.yml'

files = ['field_mappings.json', 'dynamic_template.json',
         'ecs_generated.json', 'ecs_flat_generated.json',
         'ecs_flat.json', 'results.json']
# Elasticsearch Settings
es_host = "http://localhost:9200"
es_user = "elastic"
es_pass = "password"

ignore_fields = ["data_stream.dataset", "data_stream.namespace", "data_stream.type"]


def cleanup_files(files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)


def match_mappings(custom_data, test_index_name, subobjects):
    matched_fields = 0
    ignored_fields = 0
    mismatched_fields = 0

    print(f"Creating index: {test_index_name}")
    elastic.create_index(es_client, test_index_name, dm, subobjects)

    print(f"Adding document to index: {test_index_name}")
    elastic.index_document(es_client, test_index_name, custom_data)

    print(f"Retrieves mapping from index: {test_index_name}")
    elastic_mappings = elastic.get_mappings(es_client, test_index_name)

    mapping_compare = process_mappings(elastic_mappings, test_index_name)

    print("Comparing ECS definition with Elasticsearch mapping")
    for key, value in mapping_compare.items():
        if key in ecs_flat:
            if ecs_flat[key] == value:
                matched_fields += 1
                continue
            elif key in ignore_fields:
                ignored_fields += 1
                continue
            else:
                mismatched_fields += 1
                print(
                    f"Incorrect mapping for '{key}'- found '{value}' and should be: '{ecs_flat[key]}'")
        else:
            print(
                f"The key-value pair ({key}: {value}) has no ECS mapping")
    print(
        f"Tested {len(mapping_compare)}/{matched_fields + mismatched_fields} Fields")
    print(f"Matched fields: {matched_fields}")
    print(f"Ignored fields: {ignored_fields}")
    print(f"Missmatched fields: {mismatched_fields}")


if __name__ == "__main__":
    print(f"Deleting old files: {files}")
    cleanup_files(files)

    dm = process_dynamic_mapping(dm_ecs_url)
    ecs_generated, ecs_flat_generated, ecs_flat = process_ecs(ecs_url)

    print(f"Connecting to: {es_host}")
    es_client = elastic.client(es_host, es_user, es_pass)

    print(f"Testing document with nested objects")
    match_mappings(ecs_flat_generated, "testindex_flat", True)

    print(f"Testing flattened document")
    match_mappings(ecs_generated, "testindex_nesting", True)

    print(f"Testing flattened document with 'subobjects: false'")
    match_mappings(ecs_flat_generated, "testindex_flat_subobjects_false", False)

    cleanup_files(files)
