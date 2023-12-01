from es_data_load.es import ElasticsearchWrapper
from es_data_load.lib.utilities import create_recreate_index


class SchemaManager:
    def __init__(self, search_wrapper: ElasticsearchWrapper, schemas):
        self.search_wrapper = search_wrapper
        self.schemas = schemas

    def create_es_indices(self, drop_and_recreate=False, exists_ok=True):
        for file_name in self.schemas:
            index_name = self.schemas[file_name]["index_name"]
            field_mapping = self.schemas[file_name]["field_mapping"]
            create_recreate_index(
                self.search_wrapper.es,
                index_name=index_name,
                aliases=[],
                fields=field_mapping,
                delete_index=drop_and_recreate,
                exists_ok=exists_ok,
            )
