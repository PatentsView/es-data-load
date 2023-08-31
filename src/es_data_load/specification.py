import json

from es_data_load.lib.utilities import load_config_dict_from_json_files, generate_load_statistics


def validate_mapping_structure(mapping):
    assert all([x in mapping for x in
                ['source_setting', 'target_setting']])
    assert all([x in mapping['source_setting'] for x in
                ['field_mapping', 'count_source', 'source', 'key_field']])
    assert all([x in mapping['target_setting'] for x in
                ['index_name', 'indexing_batch_size', 'id_field']])


class LoadConfiguration:
    def __init__(self, load_configs):
        self.load_operations = load_configs.copy()

    @classmethod
    def generate_load_configuration_from_folder(cls, directories):
        load_job_config = load_config_dict_from_json_files(directories)
        return cls(load_job_config)

    def get_load_operation_names(self):
        return self.load_operations.keys()

    def set_load_operation(self, name, setting):
        self.load_operations[name] = setting

    def get_load_operation(self, name=None):
        if name is None or name not in self.load_operations:
            return self.load_operations
        else:
            return self.load_operations[name]


class LoadJob:
    def __init__(self, load_configuration: LoadConfiguration, data_source, data_target, test):
        self.test = test
        self.searchtarget = data_target
        self.data_source = data_source
        self.load_configuration = load_configuration
        self.load_results = {}

    def process_load_operation(self, operation, load_name):
        document_source = self.data_source.document_generator(**operation['source_setting'], load_name=load_name,
                                                              test=self.test)
        responses = self.searchtarget.bulk_load_es_documents(
            document_source=document_source,
            load_config=operation['target_setting'], test=self.test)
        return generate_load_statistics(responses)

    def process_all_load_operations(self):
        for load_operation_name in self.load_configuration.get_load_operation_names():
            self.load_results[load_operation_name] = self.process_load_operation(operation=
            self.load_configuration.get_load_operation(
                load_operation_name),
                load_name=load_operation_name)

    def get_load_results(self, operation_name):
        return self.load_results.get(operation_name, {})
