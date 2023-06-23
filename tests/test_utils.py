from specification import get_source
from lib.utilities import generate_load_statistics
from source.DelimitedDataSource import DelimitedDataSource
from source.MySQLSource import MySQLDataSource
from source.TabularDataSource import TabularDataSource


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
