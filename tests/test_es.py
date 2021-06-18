from es import PatentsViewElasticSearch


def test_es_connection(config):
    es = PatentsViewElasticSearch(config)
    print(es.es.info())


def assert_es_counts(search, target_setting):
    search.es.indices.refresh(index=target_setting['index'])
    count_response = search.es.count(index=target_setting['index'])
    print(count_response)
    assert count_response['count'] == 49
    hits = search.es.search(index=target_setting['index'], body={
            "query": {
                    "term": {
                            "patent_number": "10524402"
                            }
                    }
            })
    assert not hits['timed_out']
    assert hits['hits']['total']['value'] == 49
    hits = search.es.search(index=target_setting['index'], body={
            "query": {
                    "term": {
                            "cited_patent_number": "5606821"
                            }
                    }
            })
    assert not hits['timed_out']
    assert hits['hits']['total']['value'] == 1


def test_bulk_load_es_documents(search, documents, load_job_config):
    target_setting = load_job_config['target_setting']
    search.es.indices.delete(index=target_setting['index'])
    index_responses = search.bulk_load_es_documents(documents, target_setting)
    assert sum([len(index_response['items']) for index_response in index_responses]) == 49
    assert not any([index_response['errors'] for index_response in index_responses])
    assert_es_counts(search, target_setting)
