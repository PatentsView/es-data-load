import importlib.resources as pkg_resources
import json
import random
import re

import pytest

from es_data_load.specification import validate_mapping_structure
from es_data_load.pv.mappings.PVMappingsManager import (
    PVLoadConfiguration,
    AVAILABLE_MAPPING_FILES,
)


def validate_jinja_sql(sql_template, variable):
    assert variable not in sql_template


def test_pv_mappings():
    assert len(AVAILABLE_MAPPING_FILES["granted"]) == 21
    assert len(AVAILABLE_MAPPING_FILES["pregrant"]) == 2
    for idx, fname in enumerate(
            [
                pkg_resources.path("es_data_load.pv.mappings.production.granted", fl)
                for fl in AVAILABLE_MAPPING_FILES["granted"]
            ]
    ):
        with fname as fname:
            current_operation = json.load(open(fname, "r"))
        validate_mapping_structure(current_operation)
        key_field = current_operation["source_setting"]["key_field"]
        assert key_field in current_operation["source_setting"]["key_field"]

        col_list_string = re.search(
            r"select(.*?)from",
            current_operation["source_setting"]["source"],
            flags=re.IGNORECASE,
        ).group(1)
        columns = col_list_string.split(",")
        assert max(current_operation["source_setting"]["field_mapping"].values()) < len(
            columns
        )


@pytest.mark.skip()
def test_pv_mapping_queries():
    all_configs = PVLoadConfiguration.load_default_pv_configuration()


def test_pv_load_configuration():
    pv_configuration = PVLoadConfiguration.load_default_pv_configuration(
        suffix="_test",
        granted_files=random.sample(AVAILABLE_MAPPING_FILES["granted"], k=5),
        pregrant_files=random.sample(AVAILABLE_MAPPING_FILES["pregrant"], k=2),
    )
    assert len(pv_configuration.get_load_operation_names()) == 7
    for setting_name in pv_configuration.get_load_operation_names():
        setting = pv_configuration.get_load_operation(setting_name)
        validate_mapping_structure(setting)
        validate_jinja_sql(
            sql_template=setting["source_setting"]["source"],
            variable="{elastic_production_source}",
        )
        validate_jinja_sql(
            sql_template=setting["source_setting"]["source"],
            variable="{reporting_data_source}",
        )
        validate_jinja_sql(
            sql_template=setting["source_setting"]["count_source"],
            variable="{elastic_production_source}",
        )
        validate_jinja_sql(
            sql_template=setting["source_setting"]["count_source"],
            variable="{reporting_data_source}",
        )
