import configparser
import json
import os

import pytest

from LoadJob import LoadJob
from es import PatentsViewElasticSearch
from source.MySQLSource import MySQLDataSource


@pytest.fixture()
def project_root():
    yield os.environ['PROJECT_ROOT']


@pytest.fixture()
def config(project_root):
    c = configparser.ConfigParser()
    c.read("{root}/resources/config.ini".format(root=project_root))
    yield c


@pytest.fixture()
def load_job_config(project_root):
    example_load_job_file = 'tests/patent_citations_loads/patent_citation.json'
    full_filepath = "{root}/{relative_file_path}".format(
            relative_file_path=example_load_job_file,
            root=project_root)
    load_job_config = json.load(open(full_filepath))
    yield load_job_config


@pytest.fixture()
def mysql_source(config):
    source = MySQLDataSource(config)
    yield source


@pytest.fixture()
def search(config):
    yield PatentsViewElasticSearch(config)


@pytest.fixture()
def load_job_2(project_root, config):
    test_mapping_folder = "tests/all_citations_loads"
    full_test_mapping_path = "{root}/{relative_folder_path}".format(
            relative_folder_path=test_mapping_folder,
            root=project_root)
    lj = LoadJob.generate_load_job_from_folder(full_test_mapping_path, config)
    yield lj


@pytest.fixture()
def load_job_1(project_root, config):
    test_mapping_folder = "tests/patent_citations_loads"
    full_test_mapping_path = "{root}/{relative_folder_path}".format(
            relative_folder_path=test_mapping_folder,
            root=project_root)
    lj = LoadJob.generate_load_job_from_folder(full_test_mapping_path, config)
    yield lj


@pytest.fixture()
def documents(mysql_source, load_job_config):
    yield mysql_source.document_generator(**load_job_config['source_setting'])


@pytest.fixture()
def responses(search, documents, load_job_config):
    target_setting = load_job_config['target_setting']
    search.es.indices.delete(index=target_setting['index'])
    index_responses = search.bulk_load_es_documents(documents, target_setting)
    yield index_responses
