import random

import pytest
from elasticsearch import NotFoundError

from es_data_load.pv.mappings.PVMappingsManager import AVAILABLE_MAPPING_FILES
from es_data_load.pv.schemas.PVSchemaManager import (
    AVAILABLE_SCHEMA_FILES,
    PVSchemaManager,
)


def validate_es_schema(schema):
    pass


def test_schema_mapping_crosswalk():
    assert len(AVAILABLE_SCHEMA_FILES) == len(AVAILABLE_MAPPING_FILES)


def test_pv_schema_load(search):
    sm = PVSchemaManager.load_default_pv_schema(suffix="_test", es=search.es)
    assert len(sm.schemas) == len(AVAILABLE_SCHEMA_FILES)
    random_choices = random.sample(list(AVAILABLE_SCHEMA_FILES.keys()), k=3)
    print("Random choices are {c}".format(c=", ".join(random_choices)))
    sm = PVSchemaManager.load_default_pv_schema(
        suffix="_test", es=search.es, schema_files=random_choices
    )
    assert len(sm.schemas) == 3
    for file_name in sm.schemas.keys():
        index_name = sm.schemas[file_name]["index_name"]
        print(f"Deleting :{index_name}")
        try:
            search.es.indices.delete(index=index_name)
        except NotFoundError:
            pass
    sm.create_es_indices()
    for file_name in sm.schemas:
        index_name = sm.schemas[file_name]["index_name"]
        field_mapping = sm.schemas[file_name]["field_mapping"]
        print(f"Verifying :{index_name}")
        mapping_from_es = search.es.indices.get_mapping(index=index_name)
        assert field_mapping == mapping_from_es[index_name]["mappings"]["properties"]
    for file_name in sm.schemas.keys():
        index_name = sm.schemas[file_name]["index_name"]
        print(f"Deleting :{index_name}")
        search.es.indices.delete(index=index_name)


def test_go_live(search):
    random_choices = random.sample(list(AVAILABLE_SCHEMA_FILES.keys()), k=3)
    print("Random choices are {c}".format(c=", ".join(random_choices)))
    live_flag_name = "_test_live"
    suffix_name = "_test"
    sm = PVSchemaManager.load_default_pv_schema(
        suffix=suffix_name, es=search.es, schema_files=random_choices
    )

    for file_name in random_choices:
        pattern = AVAILABLE_SCHEMA_FILES[file_name]
        alias_name = pattern.format(suffix=live_flag_name)
        index_name = pattern.format(suffix=suffix_name)
        print(f"Verifying :{alias_name}")
        # mapping_from_es = search.es.indices.get_mapping(index=index_name)
        with pytest.raises(NotFoundError):
            search.es.indices.get_alias(index=index_name, name=alias_name)
    sm.create_es_indices()
    sm.go_live(live_pattern=live_flag_name)
    for file_name in random_choices:
        pattern = AVAILABLE_SCHEMA_FILES[file_name]
        alias_name = pattern.format(suffix=live_flag_name)
        index_name = pattern.format(suffix=suffix_name)
        print(f"Verifying :{alias_name}")
        search.es.indices.get_alias(index=index_name, name=alias_name)
        mapping_from_es = search.es.indices.get_mapping(index=alias_name)
        assert (
            sm.schemas[file_name]["field_mapping"]
            == mapping_from_es[index_name]["mappings"]["properties"]
        )
        search.es.indices.delete_alias(index=index_name, name=alias_name)
