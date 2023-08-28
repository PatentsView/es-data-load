import json

from es_data_load.lib.utilities import load_config_dict_from_json_files, create_recreate_index


class SchemaManager:
    def __init__(self, es, schemas: dict):
        self.es = es
        self.schemas = schemas

    @classmethod
    def generate_load_configuration_from_folder(cls, directories, es):
        schemas = load_config_dict_from_json_files(directories)
        return cls(es=es, schemas=schemas)

    def create_es_indices(self, drop_and_recreate=False, exists_ok=True):
        for index_name, field_mapping in self.schemas.items():
            create_recreate_index(self.es.es, index_name=index_name, aliases=[], fields=field_mapping,
                                  delete_index=drop_and_recreate, exists_ok=exists_ok)


class PVSchemaManager(SchemaManager):
    schema_index_mapping = {'assignees_fields.json': 'assignees{suffix}',
                            'attorneys_fields.json': 'attorneys{suffix}',
                            'cpc_classes_fields.json': 'cpc_classes',
                            'cpc_groups_fields.json': 'assignees{suffix}',
                            'cpc_subclasses_fields.json': 'cpc_subclasses',
                            'foreign_citations_fields.json': 'foreign_citations{suffix}',
                            'inventors_fields.json': 'inventors{suffix}',
                            'ipcr_fields.json': 'ipcr',
                            'locations_fields.json': 'locations{suffix}',
                            'other_references_fields.json': 'other_references{suffix}',
                            'patents_fields.json': 'patents{suffix}',
                            'rel_app_text_fields.json': 'rel_app_text{suffix}',
                            'us_application_citations_fields.json': 'us_application_citations{suffix}',
                            'us_patent_citations_fields.json': 'us_patent_citations{suffix}',
                            'uspc_mainclasses_fields.json': 'uspc_mainclasses',
                            'uspc_subclasses_fields.json': 'uspc_subclasses',
                            'wipo_fields.json': 'wipo'}

    def __init__(self, es, schemas: dict, suffix):
        self.suffix = suffix
        super().__init__(es, schemas)

    @classmethod
    def load_default_pv_schema(cls, es, suffix):
        schemas = {}
        import importlib.resources as pkg_resources
        for file_name, index_pattern in PVSchemaManager.schema_index_mapping.items():
            # DATA_PATH = pkg_resources.path('es_data_load', 'pv/schema')
            with pkg_resources.path('es_data_load.pv.schemas', file_name) as schema_file:
                field_mapping = json.load(open(schema_file, 'r'))
            index_name = index_pattern.format(suffix=suffix)
            schemas[index_name] = field_mapping
        return cls(es, schemas, suffix)

    def go_live(self):
        for index_pattern in self.schema_index_mapping:
            self.es.indices.put_alias(index=index_pattern.format(suffix=""),
                                      name=index_pattern.format(suffix=self.suffix))
