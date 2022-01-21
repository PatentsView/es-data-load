import logging

from elasticsearch import Elasticsearch


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

    def bulk_load_es_documents(self, documents, load_config, verb='create'):
        target_index = load_config['index']
        indexing_batch_size = load_config['indexing_batch_size']
        id_field = load_config['id_field']
        current_batch_size = 0
        action_data_pairs = []
        if verb=='update':
            row_name = load_config['nested_field']
            documents = self.group_documents(documents, row_name)
        for data_row in documents:
            if current_batch_size >= indexing_batch_size:
                current_batch_size = 0
                r = self.es.bulk(action_data_pairs)
                yield r
                action_data_pairs = []
            if verb == 'create': #adding these empty fields for nesting is hard coded for now, will need to change
                data_row_id = data_row[id_field]
                data_row['assignees'] = []
                data_row['inventors'] = []
                data_row['cpc'] = []
            elif verb == 'update': #better way to keep track of the patent number?
                data_row_id = data_row['doc'][row_name][0][id_field]
            else:
                data_row_id = data_row[id_field]
            action_data_pairs.append({
                    verb: {
                            '_id':    data_row_id,
                            '_index': target_index
                            }
                    })
            action_data_pairs.append(data_row)
            current_batch_size += 2
        r = self.es.bulk(action_data_pairs)
        yield r

    def group_documents(self, documents, row_name):
        all_docs = {}
        for doc in documents:
            patent_num = doc['patent_number']
            all_docs[patent_num] = all_docs.get(patent_num, []) + [doc]
        rv = []
        for v in all_docs.values():
            rv.append({"doc": {row_name: v}}) #needs to be in format {"doc": {"assignees": [assignee1, assignee2,...]}}
        return rv