import importlib.resources as pkg_resources
import json
import re

from es_data_load.specification import validate_mapping_structure


def test_pv_mappings():
    from es_data_load.pv.mappings.PVMappingsManager import (
        PVLoadConfiguration,
        AVAILABLE_MAPPING_FILES,
    )

    assert len(AVAILABLE_MAPPING_FILES) == 17
    for idx, fname in enumerate(
            [
                pkg_resources.path("es_data_load.pv.mappings.production", fl)
                for fl in AVAILABLE_MAPPING_FILES
            ]
    ):
        current_operation = json.load(open(fname, "r"))
        validate_mapping_structure(current_operation)
        key_field = current_operation["source_setting"]["key_field"]
        assert key_field in current_operation["source_setting"]["key_field"]

        col_list_string = re.search(r'select(.*?)from', current_operation["source_setting"]["source"],
                                    flags=re.IGNORECASE).group(1)
        columns = col_list_string.split(",")
        assert max(current_operation["source_setting"]["field_mapping"].values()) < len(columns)
