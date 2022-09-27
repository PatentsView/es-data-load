import json

from es import PatentsViewElasticSearch
from source.DelimitedDataSource import DelimitedDataSource
from source.MySQLSource import MySQLDataSource
from source.TabularDataSource import TabularDataSource


def get_source(config, source_type='mysql'):
    source = TabularDataSource()
    if source_type == 'mysql':
        source = MySQLDataSource(config)
    if source_type == 'delimited':
        source = DelimitedDataSource(config)
    return source


def generate_load_statistics(responses):
    batch_count = 0
    record_count = 0
    total_duration = 0
    error_status = False
    for response in responses:
        batch_count += 1
        record_count = record_count + len(response['items'])
        total_duration += response['took']
        if not error_status:
            if response['errors']:
                error_status = True

    return {
        'batches': batch_count,
        'record_count': record_count,
        'complete': True,
        'success': not error_status,
        'duration': total_duration
    }


class LoadJob:
    def __init__(self, load_job_config, connection_config):
        self.load_operations = {}
        self.searchtarget = PatentsViewElasticSearch(connection_config)
        source_type = connection_config['SOURCE']['TYPE']
        self.data_source = get_source(connection_config, source_type)
        for load_job in load_job_config:
            self.add_load_operation(load_job, load_job_config[load_job])

    @classmethod
    def generate_load_job_from_folder(cls, directory, connection_config):
        import os
        if not os.path.exists(directory) or not os.path.isdir(directory):
            raise Exception(f"{directory} is not a folder")
        load_job_config = {}
        for fname in os.listdir(directory):
            if fname.endswith(".json"):
                lname = ".".join(fname.split('.')[:-1])
                json_file = os.path.join(directory, fname)
                load_job_config[lname] = json.load(open(json_file, "r"))
        return cls(load_job_config, connection_config)

    def add_load_operation(self, name, setting: dict):
        setting.update({
            'complete': False,
            'success': False
        })
        self.load_operations[name] = setting.copy()

    def get_load_operation_names(self):
        return self.load_operations.keys()

    def process_load_operation(self, name):
        operation = self.load_operations[name]
        document_source = self.data_source.document_generator(**operation['source_setting'], load_name=name)
        responses = self.searchtarget.bulk_load_es_documents(
            document_source=document_source,
            load_config=operation['target_setting'])
        load_stats = generate_load_statistics(responses)
        self.load_operations[name].update(load_stats)

    def process_all_load_operations(self):
        for load_operation in self.load_operations:
            self.process_load_operation(load_operation)

    def get_load_job_status(self, name=None):
        if name is None or name not in self.load_operations:
            return self.load_operations
        else:
            return self.load_operations[name]
