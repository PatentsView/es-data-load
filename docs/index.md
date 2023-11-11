# Elastic Data Loader

Library for loading tabular data (typically from relational database tables) to elastic search index. Its goal is to
provide an interface through which PatentsView data can be loaded into elastic search index.

# Installation

```shell
$ pip install -e ssh+git@github.com:PatentsView/es-data-load.git
```

# Getting started

If you are attempting to load data for PatentsView Search Platform (API, etc.) you'll find code snippets in
the [Data Load for PatentsView Search Platform](02 - patentsview.md) page.

If you'd like to see some usage examples proceed to [General Usage Examples](01 - usage.md) page.

# Concepts

To effectively use this package, understanding of, and ability to create specifications for the following 3 concepts are
required.

### Note on specifications

Owing to its simplicity, JSON is used as the specification format. Given JSON's limitation pertaining to comments,
documentation on expected structure of all specification is provided in the [specifications](#specifications) section.

## 1. Elasticsearch Index

This corresponds to the "destination" of the data (also referred to as target elsewhere in this documentation).
See [What is an elasticsearch index?](https://www.elastic.co/blog/what-is-an-elasticsearch-index).

As it relates to an elastic search index, the following features are supported:

* Creating indices (drop and recreate if required)
* Loading data into indices
* Adding aliases

See [Usage](#usage) section for examples. See [Specification](#json-structure-for-elasticsearch-index-creation) for JSON
structure

## 2. Tabular Data Source

The next critical piece is the source data. Currently, this package supports only tabular data sources. Specifically,
delimited files and MySQL databases.

### 2.1 Delimited Data Source

Formats such as CSV, TSV, etc. are supported. Quoting follows
pythons [csv module](https://github.com/python/cpython/blob/38035fed9ba543d587c1fbba5c463d34edf3aff9/Lib/csv.py#L18).

**N.B:** Quote character is `"`. Customizing the `quotechar` is not supported.

### 2.2 MySQL Data Source

Connecting to MySQL tables are views for data source is supported. The connection needs to specified
as [PyMySQL](https://pymysql.readthedocs.io/en/latest/index.html) connection.

**N.B.**: Internally, python primary data structures are used to optimize for performance (pandas dataframes for example
are not utilized). Due to this, sqlalchemy connection support is forgone.

### 2.3 INI Specification

The specification for data source is optional. i.e. the delimited file properties or the mysql connection properties can
all be used directly when building the corresponding python objects. A convenience method is provided to
use [config](https://docs.python.org/3/library/configparser.html) files. See [Specification](#specifications) section.

## 3. Mapping

Final piece of the puzzle is bridging the gap between data source(delimited/mysql) and data target(elastic search
index). The mapping allows for the means to collect data incrementally from the source, and load it into the index.
Features supported are:

* incremental data sourcing as well as incremental loading
* upsert (update or insert) via key fields
* load multiple data sources to targets at the same time

### 3.1 JSON Specification

The specification for the mapping allows for the following:

* Specify source SQL
* Specify target index
* Mapping between SQL select columns and elastic index field names
* Specify key fields
* Specify batch processing settings

# Specifications

## Config structure for elasticsearch connection

`HOST` is required. Rest are optional

```ini
[ELASTICSEARCH]
HOST = localhost:9200
USER =
PASSWORD =
TIMEOUT = 120
```

## Config structure for MySQL Connection

`RETRIES` is optional. Rest are required

```ini
[DATABASE_SETUP]
HOST =
PORT =
USERNAME =
PASSWORD =
RETRIES = 3
```

## Config structure for Delimited Connection

Everything is required

```ini
[DELIMITED_SETUP]
TYPE = delimited
DELIMITER = tab
```

## JSON structure for elasticsearch index creation

The JSON specification for creating an index using this package, follows elasticsearch's own specification for creating
an index.
See [Mappings](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html#mappings) in
elasticsearch's documentation.

**N.B:** Note that, only the value of the key "properties" from the above documentation is expected and supported.

```json
{
  "field_name_1": {
    "type": "data_type"
  },
  "field_name_2": {
    "type": "nested",
    "properties": {
      "subfield_name_1": {
        "type": "data_type"
      }
    }
  },
  "field_name_3": {
    "type": "data_type"
  }
}
```

## JSON structure for mappings

The JSON for mapping has 2 components:

```json
{
  "source_setting": {},
  "target_setting": {}
}
```

### SQL Source Settings

```json
{
  "source": "select column1,column2, column3 from elastic_production_20230630.assignees where persistent_assignee_id > '{offset}' order by persistent_assignee_id limit {limit};",
  "field_mapping": {
    "field_name_1": 0,
    "field_name_3": 2
  },
  "key_field": "field_name_3",
  "nested_fields": {
    "field_name_2": {
      "source": "select column_from_another_table from elastic_production_20230630.assignee_years ay join (select assignee_id, persistent_assignee_id from elastic_production_20230630.assignees where persistent_assignee_id > '{offset}' order by persistent_assignee_id limit {limit}) a on a.assignee_id = ay.assignee_id",
      "field_mapping": {
        "subfield_name_1": 0
      }
    }
  },
  "count_source": "SELECT count(1) FROM elastic_production_20230630.assignees",
  "chunksize": 1000000
}
```

| Key           | Value Data Type | Value Description                                                                                         | Notes                                                                                                                              |
|---------------|-----------------|-----------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| source        | String          | Templated SQL query that fetches records from source table. Must include limit/offset templated variable. | Up to the user to create query that makes sense. Typically achieved by using an id field to incrementally fetch subsequent records |
| field_mapping | JSON            | JSON object providing positional mapping between selected columns and elasticsearch index fields          | Keys should be elasticsearch index field names. Values should be numbers that positionally identify column from source             |
| key_field     | String          | Elasticsearch field that identified each record uniquely (primary key)                                    | See `id_field` below in [Target Settings](#target-settings)                                                                        | 
| nested_fields | JSON            | JSON object that specifies the source_setting for nested elasticsearch field                              | All the rules listed in this table are recursively applied to nested_fields                                                        |
| count_source  | String          | SQL query that returns the number of records to be processed                                              | Same rules about `source` field applies. First column of first row is used as count                                                |  
| chunksize     | Numeric         | Used as `limit` variable in `source` to iteratively fetch records                                         |                                                                                                                                    |

### Delimited Source Settings

```json
{
  "source_setting": {
    "source": "tests/mappings/artifacts/g_us_patent_citations.sample.tsv",
    "field_mapping": {
      "uuid": 0,
      "patent_number": 1,
      "cited_patent_number": 3,
      "citation_date": 4,
      "citation_kind": 6,
      "citation_country": 5,
      "citation_category": 7,
      "citation_sequence": 2
    },
    "count_source": "tests/mappings/artifacts/g_us_patent_citations.sample.tsv",
    "key_field": "uuid",
    "chunksize": null
  }
}
```

Rules are same as [SQL Source settings](#sql-source-settings) with few exceptions:

- `source` and `count_source` are just filepaths
- `chunksize` is ignored. Records are streamed from files

### Target Settings

```json
{
  "index": "assignees",
  "indexing_batch_size": 7500,
  "id_field": "assignee_id"
}
```

| Key                 | Value Data Type | Value Description                                    | Notes                                                                                                        | 
|---------------------|-----------------|------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| index               | String          | Index where data needs to be loaded                  | If index doesn't already exists, it'll be created with inferred data types. This is generally not preferable |
| indexing_batch_size | Numeric         | Number of records to send in one batch when indexing |                                                                                                              |
| id_field            | String          | Elasticsearch index ID field                         | Should be same as `key_field` in `source_setting`                                                            |