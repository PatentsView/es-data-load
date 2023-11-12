# Step-by-Step Usage Examples

## 1. Connecting to Elasticsearch

### Connect using credentials

```python
from es_data_load.es import ElasticsearchWrapper

search_target = ElasticsearchWrapper(hoststring="hostname", username='es_username', password='es_password',
                                     timeout=60)
```

### Connect using configuration

See [config structure](index.md#config-structure-for-elasticsearch-connection)

```python
from es_data_load.es import ElasticsearchWrapper
import configparser

config_file_to_use = "somefile.ini"
config = configparser.ConfigParser()
config.read(config_file_to_use)
search_target = ElasticsearchWrapper.from_config(config)
```

## 2. Create Elasticsearch index

This snippet uses `search_target` from [Connecting to Elasticsearch](#connecting-to-elasticsearch) section above. For
reference to schema, see [specification](index.md#json-structure-for-elasticsearch-index-creation)

```python
from es_data_load.schema.SchemaManager import SchemaManager

sm = SchemaManager(es=search_target.es,
                   schemas={'patent_citations_schema': {'index_name': 'patent_citations_test', 'field_mapping': {
                       "uuid": {"type": "keyword"},
                       "patent_id": {
                           "type": "keyword"
                       },
                       "patent": {
                           "type": "keyword"
                       },
                       "citation_sequence": {
                           "type": "long"
                       },
                       "citation_patent_id": {
                           "type": "keyword"
                       },
                       "citation_patent": {
                           "type": "keyword"
                       },
                       "citation_wipo_kind": {
                           "type": "keyword"
                       },
                       "citation_category": {
                           "type": "keyword"
                       },
                       "citation_date": {
                           "type": "date"
                       },
                       "citation_name": {
                           "type": "keyword"
                       },
                       "patent_zero_prefix": {
                           "type": "keyword"
                       }
                   }}})
sm.create_es_indices(drop_and_recreate=False, exists_ok=False)
```

## 3. Connecting to Tabular Data Source

### Connect directly with settings

```python
import csv
from es_data_load.DataSources import MySQLDataSource, DelimitedDataSource
from pymysql import connect as pymysql_connect

mysql_source = MySQLDataSource(connection=pymysql_connect(host='mysql_hostname',
                                                          user='mysql_username',
                                                          password='mysql_pasword',
                                                          charset='utf8mb4', defer_connect=True,
                                                          port=int('mysql_port')))

# Tab is special because ini file containing "\t" are not processed correctly
delimited_source = DelimitedDataSource(delimiter="tab", quoting=csv.QUOTE_NONNUMERIC)

another_delimited_source = DelimitedDataSource(delimiter=",", quoting=csv.QUOTE_NONNUMERIC)

```

### Connecting using config file

See [Delimited config structure](index.md#config-structure-for-delimited-connection)
or [MySQL config structure](index.md#config-structure-for-mysql-connection)

```python
from es_data_load.DataSources import MySQLDataSource, DelimitedDataSource
import configparser

config_file_to_use = "somefile.ini"
config = configparser.ConfigParser()
config.read(config_file_to_use)

mysql_source = MySQLDataSource.from_config(config)

delimited_source = DelimitedDataSource.from_config(config)
```

## Creating a Load configuration (mapping)

1. Create a folder with a one or more mapping files

```json
{
  "source_setting": {
    "source": "SELECT u.* from patent.uspatentcitation u where u.patent_id='10524402' and uuid > '{offset}' order by uuid limit {limit} ",
    "field_mapping": {
      "uuid": 0,
      "patent_number": 1,
      "cited_patent_number": 2,
      "citation_date": 3,
      "citation_kind": 5,
      "citation_country": 6,
      "citation_category": 7,
      "citation_sequence": 8
    },
    "key_field": "uuid",
    "count_source": "SELECT count(1) from (select * from patent.patent where id=10524402)p  join patent.uspatentcitation u on p.id = u.patent_id",
    "chunksize": 10000
  },
  "target_setting": {
    "index": "patent_citations_test",
    "indexing_batch_size": 10000,
    "id_field": "uuid"
  }
}
```

2. Provide the folder as input to load job configuration

```python
from es_data_load.specification import LoadConfiguration

mappings_folder = "mappings/patent_citations_loads"
l_config = LoadConfiguration.generate_load_configuration_from_folder(directories=[mappings_folder])
```

## 4. Creating a Load Job

This snippet uses variables from above sections

```python
from es_data_load.specification import LoadJob

load_job = LoadJob(load_configuration=l_config, data_source=mysql_source, data_target=search_target,
                   test=False)
```

## 5. Load data

```python
load_job.process_all_load_operations()
```

## 6. Complete Example

```python
# Imports
from pymysql import connect as pymysql_connect

from es_data_load.DataSources import MySQLDataSource
from es_data_load.es import ElasticsearchWrapper
from es_data_load.specification import LoadConfiguration, LoadJob
from es_data_load.schema.SchemaManager import SchemaManager
import configparser, json

# Load config file
config_file_to_use = "somefile.ini"
config = configparser.ConfigParser()
config.read(config_file_to_use)

# Connect to elasticsearch
search_target = ElasticsearchWrapper.from_config(config)

# Create Schema
sm = SchemaManager(es=search_target.es, schemas={'patent_citations_schema': {'index_name': 'patent_citations_test',
                                                                             'field_mapping': json.load(
                                                                                 open("schema.json", "r"))}})
sm.create_es_indices(drop_and_recreate=False, exists_ok=False)

# Connect to MySQL Database
mysql_source = MySQLDataSource.from_config(config)

# Create one or more load configurations
mappings_folder = "mappings/patent_citations_loads"
l_config = LoadConfiguration.generate_load_configuration_from_folder(directories=[mappings_folder])

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



