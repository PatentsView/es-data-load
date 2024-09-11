import json
import logging

from es_data_load.es import ElasticsearchWrapper
from es_data_load.schema.SchemaManager import SchemaManager

AVAILABLE_SCHEMA_FILES = {
    "granted": {
        "assignees_fields.json": "assignees{suffix}",
        "attorneys_fields.json": "attorneys{suffix}",
        "cpc_classes_fields.json": "cpc_classes{suffix}",
        "cpc_groups_fields.json": "cpc_groups{suffix}",
        "cpc_subclasses_fields.json": "cpc_subclasses{suffix}",
        "foreign_citations_fields.json": "foreign_citations{suffix}",
        "inventors_fields.json": "inventors{suffix}",
        "ipcr_fields.json": "ipcr{suffix}",
        "locations_fields.json": "locations{suffix}",
        "other_references_fields.json": "other_references{suffix}",
        "patents_fields.json": "patents{suffix}",
        "rel_app_text_fields.json": "rel_app_text{suffix}",
        "us_application_citations_fields.json": "us_application_citations{suffix}",
        "us_patent_citations_fields.json": "us_patent_citations{suffix}",
        "uspc_mainclasses_fields.json": "uspc_mainclasses{suffix}",
        "uspc_subclasses_fields.json": "uspc_subclasses{suffix}",
        "wipo_fields.json": "wipo{suffix}",
        "brf_sum_text.json": "brf_sum_text{suffix}",
        "claim.json": "claim{suffix}",
        "detail_desc_text.json": "detail_desc_text{suffix}",
        "draw_desc_text.json": "draw_desc_text{suffix}",
        "rawapplicants_fields.json": "rawapplicants{suffix}",
    },
    "pregrant": {
        "publication_fields.json": "publications{suffix}",
        "rel_app_text_publications_fields.json": "rel_app_text_publications{suffix}"
    },
}
logger = logging.getLogger("es-data-load")


class PVSchemaManager(SchemaManager):
    def __init__(self, search_wrapper, suffix, schemas: dict):
        super().__init__(search_wrapper, schemas)
        self.suffix = suffix
        self.search_wrapper = search_wrapper
        self.schemas = schemas.copy()

    @classmethod
    def load_default_schema(cls, schema_files, suffix, schema_path_prefix):
        schemas = {}
        for file_name in schema_files:
            index_pattern = AVAILABLE_SCHEMA_FILES[schema_path_prefix][file_name]
            # DATA_PATH = pkg_resources.path('es_data_load', 'pv/schema')
            import importlib.resources as pkg_resources

            with pkg_resources.path(
                f"es_data_load.pv.schemas.{schema_path_prefix}", file_name
            ) as schema_file:
                field_mapping = json.load(open(schema_file, "r"))
            index_name = index_pattern.format(suffix=suffix)
            schemas[f"{schema_path_prefix}_{file_name}"] = {
                "index_name": index_name,
                "field_mapping": field_mapping,
                "type": schema_path_prefix,
                "index_pattern": index_pattern,
            }
        return schemas

    @classmethod
    def load_default_pv_schema(
        cls,
        search_wrapper: ElasticsearchWrapper,
        suffix,
        granted_schema_files=None,
        pregrant_schema_files=None,
    ):
        if granted_schema_files is None:
            granted_schema_files = AVAILABLE_SCHEMA_FILES["granted"].keys()
        if pregrant_schema_files is None:
            pregrant_schema_files = AVAILABLE_SCHEMA_FILES["pregrant"].keys()
        selected_schemas = cls.load_default_schema(
            granted_schema_files, suffix, "granted"
        )
        selected_schemas.update(
            cls.load_default_schema(pregrant_schema_files, suffix, "pregrant")
        )
        return cls(
            search_wrapper=search_wrapper, schemas=selected_schemas, suffix=suffix
        )

    def go_live(self, live_pattern=""):
        for filename in self.schemas:
            index_pattern = self.schemas[filename]["index_pattern"]
            index_name = index_pattern.format(suffix=self.suffix)
            alias_name = index_pattern.format(suffix=live_pattern)
            logger.info(
                f"Going live with {filename}: mapping {alias_name} to {index_name}"
            )
            self.search_wrapper.es.indices.put_alias(
                index=index_name,
                name=alias_name,
            )
