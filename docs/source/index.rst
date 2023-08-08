..
    Elastic Search Data Loader documentation master file, created by
    sphinx-quickstart on Wed Jun 21 15:41:44 2023.
    You can adapt this file completely to your liking, but it should at least
    contain the root `toctree` directive.

############################
Elastic Search Data Loader
############################


Library for loading tabular data (typically from relational database tables) to elastic search index. Its goal is to provide an interface through which PatentsView data can be loaded into elastic search index

==============
Installation
==============
.. code-block::

      $ pip install -e ssh+git@github.com:PatentsView/es-data-load.git

================
Example Usage
================

.. code-block::


    from pymysql import connect as pymysql_connect

    from es_data_load.DataSources import MySQLDataSource
    from es_data_load.es import PatentsViewElasticSearch
    from es_data_load.schema.SchemaManager import PVSchemaManager
    from es_data_load.specification import LoadConfiguration, LoadJob

    # Configuration for copying data from tabular data to elastic search
    # Can have multiple json files for multiple table/indices
    loadconfigs = LoadConfiguration.generate_load_configuration_from_folder(
        directories=["/path/to/folder/containing/configuration/"])

    # Create Elastic Search connection
    es = PatentsViewElasticSearch(hoststring="hostname", username='es_username', password='es_password', timeout=60)

    # Create index with required schema
    schema_manager = PVSchemaManager(es=es, schemas={'index_name': {'field_1': {"type": "keyword"}}}, suffix='_test')
    schema_manager.create_es_indices(drop_and_recreate=False, exists_ok=True)

    # Create Database Connection
    mysql_source = MySQLDataSource(connection=pymysql_connect(host='mysql_hostname',
                                    user='mysql_username',password='mysql_pasword',
                                    charset='utf8mb4', defer_connect=True,port=int('mysql_port')))

    # Create a load "job"
    load_job = LoadJob(loadconfigs, mysql_source, es, test=0)

    # Process all jobs (all json files)
    load_job.process_all_load_operations()

    # View results
    operations = loadconfigs.get_load_operation_names()
    for operation in operations:
        print("------------")
        print(operation)
        status = load_job.get_load_results(operation)
        print(status)

    loadconfigs = LoadConfiguration.load_default_pv_configuration(suffix="_test")
    es = PatentsViewElasticSearch.from_config(config)


--------------------------------
Breaking it down
--------------------------------
1. Create two configurations
    a. A configuration for how to map data from source to target. `Examples <https://stackoverflow.com/>`_
    b. A second configuration that defines the structure of elastic search index. `Examples <https://stackoverflow.com/>`_
2. Connect to source (delimited file or mysql) & destination (elastic search)
3. Connect to destination and create required ES indices
4. Run the loading process

------------------------------------
Default PatentsView configuration
------------------------------------

- To use the default pv configuration for loading configuration:

.. code-block::

    loadconfigs = LoadConfiguration.load_default_pv_configuration()

- To use the default pv configuration for elastic search index:

.. code-block::

    schema_manager = PVSchemaManager(es=es, suffix='_test')

.. toctree::
   :maxdepth: 2
   :caption: Contents:

modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
