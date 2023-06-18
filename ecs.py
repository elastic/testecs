import requests
import yaml
import json
from datetime import datetime
from faker import Faker


def process_ecs(url):
    ecs_fields = 0
    ecsoutput = {}
    print(f"Downloading ECS definition from {url}")
    response = requests.get(url)
    data = response.text

    ecsdata = yaml.safe_load(data)

    for key, value in ecsdata.items():
        if isinstance(value, dict) and 'type' in value:
            ecsoutput[key] = value['type']
            ecs_fields += 1
    with open('ecs_flat.json', 'w') as file:
        json.dump(ecsoutput, file, indent=2)
    print(f"Found {ecs_fields} fields in ECS definition")
    custom_data, custom_flat_data = generate_custom_json(ecsoutput)
    with open('ecs_generated.json', 'w') as file:
        json.dump(custom_data, file, indent=2)
    with open('ecs_flat_generated.json', 'w') as file:
        json.dump(custom_flat_data, file, indent=2)
    return custom_data, custom_flat_data, ecsoutput


def generate_custom_value(data_type):
    fake = Faker()

    if data_type == "date":
        return fake.iso8601(tzinfo=datetime.now().astimezone().tzinfo)
    elif data_type in ["keyword", "wildcard", "text", "match_only_text"]:
        return fake.word()
    elif data_type == "constant_keyword":
        return "test"
    elif data_type == "ip":
        return fake.ipv4()
    elif data_type == "boolean":
        return False
    elif data_type == "scaled_float":
        return fake.pyfloat(min_value=0.00, max_value=100.00)
    elif data_type == "float":
        return fake.pyfloat(min_value=0.00, max_value=100.00)
    elif data_type in ["object", "flattened", "nested"]:
        return None
    elif data_type in ["int", "long"]:
        return fake.random_int(min=0, max=100)
    else:
        print("Missing data type: " + data_type)
        return None


def generate_custom_json(ecs_input):
    custom_data = {}
    custom_flat_data = {}
    generated_fields = 0
    print("Generating custom data from ECS definition")
    for field_path, data_type in ecs_input.items():
        field_path_parts = field_path.split(".")
        current = custom_data

        for field in field_path_parts[:-1]:
            if field not in current:
                current[field] = {}
            current = current[field]

        field_name = field_path_parts[-1]
        if data_type == "geo_point":
            generated_fields += 1
            current[field_name] = {"lat": 10.10, "lon": 10.10}
            custom_flat_data[field_path] = [20.20, 20.20]
        else:
            test_value = generate_custom_value(data_type)
            if test_value is not None:
                generated_fields += 1
                current[field_name] = test_value
                custom_flat_data[field_path] = test_value

    print(f"Generated {generated_fields} fields in custom data")
    return custom_data, custom_flat_data
