import logging

from elasticsearch import Elasticsearch

from source.TabularDataSource import TabularDataSource


class PatentsViewElasticSearch:
    def __init__(self, config):
        hoststring = "{host}:{port}".format(host=config["ELASTICSEARCH"]["HOSTNAME"],
                                            port=config["ELASTICSEARCH"]["PORT"])
        timeout = int(config["ELASTICSEARCH"]["TIMEOUT"])
        self.logger = logging.getLogger(self.__class__.__name__)
        if config['ELASTICSEARCH']['USERNAME'] is not None:
            self.es = Elasticsearch(hosts=hoststring, http_auth=(
                config["ELASTICSEARCH"]["USERNAME"], config["ELASTICSEARCH"]["PASSWORD"]), timeout=timeout)
            self.logger.debug("Connecting with credentials")
        else:
            self.logger.debug("Connecting without credentials")
            self.es = Elasticsearch(hosts=hoststring, timeout=timeout)
        self.logger.info(self.es.info())

    def bulk_load_es_documents(self, document_source, load_config):
        target_index = load_config['index']
        indexing_batch_size = load_config['indexing_batch_size']
        id_field = load_config['id_field']
        current_batch_size = 0
        action_data_pairs = []
        for data_row in document_source:
            if current_batch_size >= indexing_batch_size:
                current_batch_size = 0
                r = self.es.bulk(action_data_pairs)
                yield r
                action_data_pairs = []
            action_data_pairs.append({
                'create': {
                    '_id': data_row[id_field],
                    '_index': target_index
                }
            })
            action_data_pairs.append(data_row)
            current_batch_size += 2
        r = self.es.bulk(action_data_pairs)
        yield r
