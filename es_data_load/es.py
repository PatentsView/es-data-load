import logging

from elasticsearch import Elasticsearch


class PatentsViewElasticSearch:
    def __init__(self, hoststring, timeout, username, password):
        self.logger = logging.getLogger(self.__class__.__name__)
        if username is not None:
            self.es = Elasticsearch(hosts=hoststring, http_auth=(username, password), timeout=timeout)
            self.logger.debug("Connecting with credentials")
        else:
            self.logger.debug("Connecting without credentials")
            self.es = Elasticsearch(hosts=hoststring, timeout=timeout)
        self.logger.info(self.es.info())

    @classmethod
    def from_config(cls, config):
        return cls(hoststring="{host}:{port}".format(host=config["ELASTICSEARCH"]["HOSTNAME"],
                                                     port=config["ELASTICSEARCH"].get("PORT")),
                   timeout=int(config["ELASTICSEARCH"]["TIMEOUT"]),
                   username=config["ELASTICSEARCH"].get("USERNAME", None),
                   password=config["ELASTICSEARCH"].get("PASSWORD", None))

    def bulk_load_es_documents(self, document_source, load_config, test):
        target_index = load_config['index']
        indexing_batch_size = load_config['indexing_batch_size']
        id_field = load_config['id_field']
        current_batch_size = 0
        action_data_pairs = []
        for data_row in document_source:
            if current_batch_size >= indexing_batch_size:
                current_batch_size = 0
                if test == 1:
                    yield []
                else:
                    r = self.es.bulk(operations=action_data_pairs, refresh=True)
                    yield r
                action_data_pairs = []
            action_data_pairs.append({
                'index': {
                    '_id': data_row[id_field],
                    '_index': target_index
                }
            })
            action_data_pairs.append(data_row)
            current_batch_size += 2
        if test == 1:
            yield []
        else:
            r = self.es.bulk(operations=action_data_pairs, refresh=True)
            yield r
