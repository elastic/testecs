import json

output = {}


def convert_mappings(mappings, output, prefix=''):
    for field, properties in mappings.items():
        full_path = prefix + field
        if 'type' in properties:
            output[full_path] = properties['type']
        elif 'properties' in properties:
            convert_mappings(properties['properties'],
                             output, prefix=full_path + '.')


def process_mappings(current_mappings, es_index):
    convert_mappings(current_mappings[es_index]
                     ['mappings']['properties'], output)

    with open('field_mappings.json', 'w') as file:
        json.dump(output, file, indent=2)
    return output
