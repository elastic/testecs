import requests
import json


def process_dynamic_mapping(dm_ecs_url):
    dynamic_templates = []

    print(f"Downloading dynamic mappings from {dm_ecs_url}")
    response = requests.get(dm_ecs_url)
    data = response.text

    # Replace the placeholder with a value or leave it as is
    data = data.replace(
        '"version": ${xpack.stack.template.version}', '"version": "1.1"')
    # Convert the modified data to JSON
    json_data = json.loads(data)
    # Extract the dynamic_templates field
    dynamic_templates.extend(
        json_data["template"]["mappings"]["dynamic_templates"])

    with open('dynamic_template.json', 'w') as file:
        json.dump(dynamic_templates, file, indent=2)

    return dynamic_templates
