import json

from es_data_load.schema.SchemaManager import SchemaManager

AVAILABLE_SCHEMA_FILES = {'assignees_fields.json': 'assignees{suffix}',
                          'attorneys_fields.json': 'attorneys{suffix}',
                          'cpc_classes_fields.json': 'cpc_classes{suffix}',
                          'cpc_groups_fields.json': 'cpc_groups{suffix}',
                          'cpc_subclasses_fields.json': 'cpc_subclasses{suffix}',
                          'foreign_citations_fields.json': 'foreign_citations{suffix}',
                          'inventors_fields.json': 'inventors{suffix}',
                          'ipcr_fields.json': 'ipcr{suffix}',
                          'locations_fields.json': 'locations{suffix}',
                          'other_references_fields.json': 'other_references{suffix}',
                          'patents_fields.json': 'patents{suffix}',
                          'rel_app_text_fields.json': 'rel_app_text{suffix}',
                          'us_application_citations_fields.json': 'us_application_citations{suffix}',
                          'us_patent_citations_fields.json': 'us_patent_citations{suffix}',
                          'uspc_mainclasses_fields.json': 'uspc_mainclasses{suffix}',
                          'uspc_subclasses_fields.json': 'uspc_subclasses{suffix}',
                          'wipo_fields.json': 'wipo{suffix}'}


class PVSchemaManager(SchemaManager):
    def __init__(self, es, suffix, schemas: dict):
        super().__init__(es, schemas)
        self.suffix = suffix
        self.es = es
        self.schemas = schemas.copy()

    @classmethod
    def load_default_pv_schema(cls, es, suffix, schema_files=None):
        schemas = {}
        if schema_files is None:
            schema_files = AVAILABLE_SCHEMA_FILES.keys()
        import importlib.resources as pkg_resources
        for file_name in schema_files:
            index_pattern = AVAILABLE_SCHEMA_FILES[file_name]
            # DATA_PATH = pkg_resources.path('es_data_load', 'pv/schema')
            with pkg_resources.path('es_data_load.pv.schemas', file_name) as schema_file:
                field_mapping = json.load(open(schema_file, 'r'))
            index_name = index_pattern.format(suffix=suffix)
            schemas[file_name] = {"index_name": index_name, "field_mapping": field_mapping}
        return cls(es=es, schemas=schemas, suffix=suffix)

    def go_live(self, live_pattern=""):
        for filename in self.schemas:
            index_pattern = AVAILABLE_SCHEMA_FILES[filename]
            self.es.indices.put_alias(
                index=index_pattern.format(suffix=self.suffix), name=index_pattern.format(suffix=live_pattern))
