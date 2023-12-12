import json
from es_data_load.specification import LoadConfiguration

AVAILABLE_MAPPING_FILES = {
    "granted": [
        "assignee.json",
        "attorney.json",
        "cpc_class.json",
        "cpc_group.json",
        "cpc_subclass.json",
        "fcitation.json",
        "inventor.json",
        "ipcr.json",
        "locations.json",
        "oreference.json",
        "patents.json",
        "rel_app_text.json",
        "us_application_citations.json",
        "us_patent_citations.json",
        "uspc_mainclass.json",
        "uspc_subclass.json",
        "wipo.json",
        "claim.json",
        "brf_sum_text.json",
        "detail_desc_text.json",
        "draw_desc_text.json",
    ],
    "pregrant": [],
}


def partially_inject_databases(configuration, elastic_source, reporting_source):
    source_sql = configuration["source"].format(
        elastic_production_source=elastic_source, reporting_data_source=reporting_source
    )
    configuration["source"] = source_sql
    if "count_source" in configuration:
        count_source = configuration["count_source"].format(
            elastic_production_source=elastic_source,
            reporting_data_source=reporting_source,
        )
        configuration["count_source"] = count_source

    return configuration


class PVLoadConfiguration(LoadConfiguration):
    def __init__(self, load_configs):
        super().__init__(load_configs)

    @classmethod
    def load_default_pv_configuration(
        cls,
        suffix="",
        granted_files=None,
        pregrant_files=None,
        elastic_source="elastic_production",
        reporting_source="PatentsView_",
    ):
        if granted_files is None:
            granted_files = AVAILABLE_MAPPING_FILES["granted"]
        if pregrant_files is None:
            pregrant_files = AVAILABLE_MAPPING_FILES["pregrant"]
        import importlib.resources as pkg_resources

        # schema_file =
        package_files = {
            "granted_package_files": [
                pkg_resources.path("es_data_load.pv.mappings.production.granted", fl)
                for fl in granted_files
            ],
            "pregrant_package_files": [
                pkg_resources.path("es_data_load.pv.mappings.production.pregrant", fl)
                for fl in pregrant_files
            ],
        }

        configs = {}
        for source_type, files in package_files.items():
            for idx, fname in enumerate(files):
                with fname as fname:
                    config_name = "{dname}-{stype}-{fname}".format(
                        dname="es_data_load/pv/mappings/production",
                        stype=source_type,
                        fname=".".join(granted_files[idx].split(".")[:-1]),
                    )
                    current_operation = json.load(open(fname, "r"))
                    index_w_o_suffix = current_operation["target_setting"]["index"]
                    index = "{idx}{suffix}".format(idx=index_w_o_suffix, suffix=suffix)
                    source_settings = current_operation["source_setting"]
                    source_settings = partially_inject_databases(
                        source_settings,
                        elastic_source=elastic_source,
                        reporting_source=reporting_source,
                    )
                    if "nested_fields" in source_settings:
                        for nested_operation_key in source_settings["nested_fields"]:
                            source_settings["nested_fields"][
                                nested_operation_key
                            ] = partially_inject_databases(
                                source_settings["nested_fields"][nested_operation_key],
                                elastic_source=elastic_source,
                                reporting_source=reporting_source,
                            )
                    current_operation["source_setting"] = source_settings
                    current_operation["target_setting"]["index"] = index
                    configs[config_name] = current_operation

        load_configuration = PVLoadConfiguration(load_configs=configs)
        return load_configuration
