from es_data_load.DataSources import MySQLDataSource


def test_connect(mysql_source: MySQLDataSource):
    mysql_source.connect()
    with mysql_source.connection.cursor() as cur:
        cur.execute("select 1")


def test_get_document_count(mysql_source, load_job_config):
    source = load_job_config['source_setting']['count_source']
    assert mysql_source.get_document_count(source) == 49


def test_generate_source_chunk(mysql_source, load_job_config):
    source_setting = load_job_config['source_setting']
    document_generator = mysql_source.generate_source_chunk(
        source_setting['source'], source_setting["field_mapping"],
        offset=0,
        limit=source_setting['chunksize'])
    import types
    assert type(document_generator) == types.GeneratorType
    doc_count = 0
    for document in document_generator:
        doc_count += 1
    assert doc_count == 49
    assert (len(document)) >= len(source_setting['field_mapping'])


def test_document_generator(mysql_source, load_job_config):
    source_setting = load_job_config['source_setting']
    target_setting = load_job_config['target_setting']
    doc_generator = mysql_source.document_generator(**source_setting)
    doc_count = 0
    for document in doc_generator:
        doc_count += 1
    assert doc_count == 49
    assert document.keys() == source_setting['field_mapping'].keys()
    assert target_setting['id_field'] in document.keys()
