## Dynamic ECS Mapping tool

This is a quick and easy way to test if the newest dynamic ECS templates matches the newest ECS field definition correctly.

As it was made quick, this is not coded with many best practices in mind, so use at your own responsibility :)

Requires connection to an Elasticsearch instance, all parameters exist at the top of main.py

```
marius@machine:~/testecs $ python main.py
Deleting old files: ['field_mappings.json', 'dynamic_template.json', 'ecs_generated.json', 'ecs_flat.json', 'results.json']
Downloading Dynamic mapping from https://raw.githubusercontent.com/elastic/elasticsearch/887e5f3d06fb5fa7bd5b56c11378cc50e4cc6d6e/x-pack/plugin/core/src/main/resources/ecs-dynamic-mappings.json
Downloading ECS definition from https://raw.githubusercontent.com/elastic/ecs/main/generated/ecs/ecs_flat.yml
Found 1644 fields in ECS definition
Generating custom data from ECS definition
Generated 1574 fields in custom data
Connecting to: https://localhost:9200
Comparing ECS definition with Elasticsearch mapping
The key-value pair (container.cpu.usage: float) does not exist. Field type should be: scaled_float
The key-value pair (container.memory.usage: float) does not exist. Field type should be: scaled_float
The key-value pair (email.message_id: keyword) does not exist. Field type should be: wildcard
The key-value pair (host.cpu.usage: float) does not exist. Field type should be: scaled_float
The key-value pair (threat.enrichments.indicator.registry.data.strings: keyword) does not exist. Field type should be: wildcard
The key-value pair (threat.indicator.registry.data.strings: keyword) does not exist. Field type should be: wildcard
Matched fields: 1568
Missmatched fields: 6
```