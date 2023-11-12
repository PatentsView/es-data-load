# Data load for PatentsView Search Platform
For PatentsView data load, the package supports a simplified list of steps to follow. The simplification arises from pre-creating the various specification files required for PatentsView's data structure

Compare these steps to the steps in [General Usage Exmple](01 - usage.md#complete-example)

## Complete Example

```python
# Imports
from es_data_load.DataSources import MySQLDataSource
from es_data_load.es import ElasticsearchWrapper
from es_data_load.pv.schemas.PVSchemaManager import AVAILABLE_SCHEMA_FILES, PVSchemaManager
from es_data_load.pv.mappings.PVMappingsManager import AVAILABLE_MAPPING_FILES, PVLoadConfiguration
from es_data_load.specification import LoadConfiguration, LoadJob
import configparser

# Load config file
config_file_to_use = "somefile.ini"
config = configparser.ConfigParser()
config.read(config_file_to_use)

# Connect to elasticsearch
search_target = ElasticsearchWrapper.from_config(config)

# Load all existing PV schema
sm = PVSchemaManager.load_default_pv_schema(es=search_target.es, suffix="test")

sm.create_es_indices(drop_and_recreate=False, exists_ok=False)

# Connect to MySQL Database
mysql_source = MySQLDataSource.from_config(config)

# Create one or more load configurations
mappings_folder = "mappings/patent_citations_loads"
l_config = PVLoadConfiguration.load_default_pv_configuration(suffix="test",
                                                             elastic_source="elastic_production_20230630",
                                                             reporting_source="PatentsView_20230630")

## Create load job
load_job = LoadJob(load_configuration=l_config, data_source=mysql_source, data_target=search_target,
                   test=False)

# Run load job
load_job.process_all_load_operations()

# View results
operations = l_config.get_load_operation_names()
for operation in operations:
    print("------------")
    print(operation)
    status = load_job.get_load_results(operation)
    print(status)
```

## Customizing Indices List
1. Inspect `AVAILABLE_SCHEMA_FILES`
```python
from es_data_load.pv.schemas.PVSchemaManager import AVAILABLE_SCHEMA_FILES

print(AVAILABLE_SCHEMA_FILES['granted'])
```
2. Supply granted/pregrant index files using same structure
```python
from es_data_load.pv.schemas.PVSchemaManager import PVSchemaManager

selected_sm = (
    PVSchemaManager.load_default_pv_schema(es=search_target.es, suffix="test",
                                           granted_schema_files=['assignees_fields.json'],
                                           pregrant_schema_files=[])
)
```

## Customizing Mappings List
1. Inspect `AVAILABLE_SCHEMA_FILES`
```python
from es_data_load.pv.mappings.PVMappingsManager import AVAILABLE_MAPPING_FILES
print(AVAILABLE_MAPPING_FILES['granted'])
```
2. Supply granted/pregrant index files using same structure
```python
from es_data_load.pv.mappings.PVMappingsManager import PVLoadConfiguration

l_config = (
    PVLoadConfiguration.load_default_pv_configuration(suffix="test",
                                                      elastic_source="elastic_production_20230630",
                                                      reporting_source="PatentsView_20230630",
                                                      granted_files=['assignee.json'],
                                                      pregrant_files=[])
)

```