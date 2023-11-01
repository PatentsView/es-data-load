import csv

from es_data_load.DataSources import DelimitedDataSource, MySQLDataSource, TabularDataSource
from es_data_load.lib.utilities import csv_lines, generate_load_statistics, get_source
import pytest
from elasticsearch import BadRequestError, Elasticsearch, NotFoundError

from es_data_load.lib.utilities import create_recreate_index


def test_get_mysql_source(project_root, config):
    source = get_source(config, 'mysql')
    assert source.__class__ == MySQLDataSource


def test_incorrect_source(project_root, config):
    source = get_source(config, '')
    assert source.__class__ != MySQLDataSource
    assert source.__class__ != DelimitedDataSource
    assert source.__class__ == TabularDataSource


def test_generate_load_statistics(responses):
    stats = generate_load_statistics(responses)
    assert all(x in stats.keys() for x in ['batches', 'record_count', 'complete', 'success', 'duration'])
    assert stats['complete'] and stats['success']


# def pytest_generate_tests(metafunc):
#     if metafunc.function.__name__ == 'test_create_recreate_index':
#         pass

def reset_index(es: Elasticsearch, index_name):
    try:
        es.indices.delete(index=index_name)
    except NotFoundError:
        pass


def verify_test_index_mapping(es: Elasticsearch, index_name):
    index_config = es.indices.get(index=index_name)
    assert index_name in index_config
    assert "assignee_id" in index_config[index_name]["mappings"]["properties"]
    assert index_config[index_name]["mappings"]["properties"]["assignee_id"]["type"] == "keyword"


def test_create_recreate_index(search, ):
    index_name = "test_util_index"
    # Verify index doesn't exist already
    reset_index(search.es, index_name)
    with pytest.raises(NotFoundError):
        search.es.indices.get(index=index_name)

    # Case 1 - Create index from empty
    create_recreate_index(es=search.es, index_name=index_name, aliases=[], fields={"assignee_id": {
        "type": "keyword"
    }, }, delete_index=False, exists_ok=False)
    verify_test_index_mapping(search.es, index_name)

    # Case 2 - Test Failures when index already exists
    with pytest.raises(BadRequestError):
        create_recreate_index(es=search.es, index_name=index_name, aliases=[], fields={"assignee_id": {
            "type": "keyword"
        }, }, delete_index=False, exists_ok=False)

    # Case 3 - Drop existing and recreate
    create_recreate_index(es=search.es, index_name=index_name, aliases=[], fields={"assignee_id": {
        "type": "keyword"
    }, }, delete_index=True, exists_ok=False)
    verify_test_index_mapping(search.es, index_name)

    # Case 4 - Don't drop but accept existing
    create_recreate_index(es=search.es, index_name=index_name, aliases=[], fields={"assignee_id": {
        "type": "keyword"
    }, }, delete_index=False, exists_ok=True)
    verify_test_index_mapping(search.es, index_name)

    # Case 5 - Drop and recreate
    create_recreate_index(es=search.es, index_name=index_name, aliases=[], fields={"assignee_id": {
        "type": "keyword"
    }, }, delete_index=True, exists_ok=True)
    verify_test_index_mapping(search.es, index_name)

    reset_index(search.es, index_name)
    # Case 6 - Drop and recreate
    create_recreate_index(es=search.es, index_name=index_name, aliases=[], fields={"assignee_id": {
        "type": "keyword"
    }, }, delete_index=True, exists_ok=True)
    verify_test_index_mapping(search.es, index_name)

    reset_index(search.es, index_name)
    # Case 7 - Another version of drop and recreate
    create_recreate_index(es=search.es, index_name=index_name, aliases=[], fields={"assignee_id": {
        "type": "keyword"
    }, }, delete_index=True, exists_ok=False)
    verify_test_index_mapping(search.es, index_name)

    # Case 8 - Don't drop but allow recreate
    create_recreate_index(es=search.es, index_name=index_name, aliases=[], fields={"assignee_id": {
        "type": "keyword"
    }, }, delete_index=False, exists_ok=True)
    verify_test_index_mapping(search.es, index_name)


def test_csv_lines():
    some_csv_file = "tests/utilities/artifacts/test.csv"
    assert csv_lines(some_csv_file, quoting=csv.QUOTE_NONE) == 2
