import configparser
import json
import os

import pytest
from elasticsearch import NotFoundError

from es_data_load.DataSources import MySQLDataSource
from es_data_load.es import PatentsViewElasticSearch
from es_data_load.specification import LoadConfiguration, LoadJob


@pytest.fixture()
def project_root():
    yield os.environ["PROJECT_ROOT"]


@pytest.fixture()
def config(project_root):
    c = configparser.ConfigParser()
    c.read("{root}/resources/config_dev_elastic.ini".format(root=project_root))
    return c


@pytest.fixture()
def load_job_config(project_root):
    example_load_job_file = (
        "tests/mappings/artifacts/patent_citations_loads/patent_citation.json"
    )
    full_filepath = "{root}/{relative_file_path}".format(
        relative_file_path=example_load_job_file, root=project_root
    )
    load_job_config = json.load(open(full_filepath))
    yield load_job_config


@pytest.fixture()
def mysql_source(config):
    source = MySQLDataSource.from_config(config)
    yield source


@pytest.fixture()
def search(config):
    yield PatentsViewElasticSearch.from_config(config)


@pytest.fixture()
def load_job_2(project_root):
    test_mapping_folder = "tests/mappings/artifacts/all_citations_loads"
    full_test_mapping_path = "{root}/{relative_folder_path}".format(
        relative_folder_path=test_mapping_folder, root=project_root
    )
    lj = LoadConfiguration.generate_load_configuration_from_folder(
        [full_test_mapping_path]
    )
    yield lj


@pytest.fixture()
def load_job_configuration_1(project_root):
    test_mapping_folder = "tests/mappings/artifacts/patent_citations_loads"
    full_test_mapping_path = "{root}/{relative_folder_path}".format(
        relative_folder_path=test_mapping_folder, root=project_root
    )
    lj = LoadConfiguration.generate_load_configuration_from_folder(
        [full_test_mapping_path]
    )
    yield lj


@pytest.fixture()
def load_job(project_root, load_job_configuration_1, mysql_source, search):
    lj = LoadJob(
        load_configuration=load_job_configuration_1,
        data_source=mysql_source,
        data_target=search,
        test=False,
    )
    return lj


@pytest.fixture()
def documents(mysql_source: MySQLDataSource, load_job_config):
    yield mysql_source.document_generator(**load_job_config["source_setting"])


@pytest.fixture()
def responses(search, documents, load_job_config):
    target_setting = load_job_config["target_setting"]
    try:
        search.es.indices.delete(index=target_setting["index"])
    except NotFoundError:
        pass
    index_responses = search.bulk_load_es_documents(documents, target_setting, test=0)
    yield index_responses
