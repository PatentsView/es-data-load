import json
from es_data_load.specification import LoadConfiguration
import logging

logger = logging.getLogger("es-data-load")

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
    "pregrant": [
        "publications.json",
        "rel_app_text_publications.json",
        "claim.json",
        "brf_sum_text.json",
        "detail_desc_text.json",
        "draw_desc_text.json",
    ],
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
        elastic_source_patent="elastic_production",
        elastic_source_pregrant="elastic_production",
        reporting_source_patent="PatentsView_",
    ):
        if granted_files is None:
            granted_files = AVAILABLE_MAPPING_FILES["granted"]
            logger.info("Loading configs for all available granted files...")
        elif len(granted_files) == 0:
            logger.info("Skipping granted configs...")
        else:
            logger.info(f"Loading configs for specified subset of granted files:\n{granted_files}")

        if pregrant_files is None:
            pregrant_files = AVAILABLE_MAPPING_FILES["pregrant"]
            logger.info("Loading configs for all available pregrant files...")
        elif len(pregrant_files) == 0:
            logger.info("Skipping pregrant configs...")
        else:
            logger.info(f"Loading configs for specified subset of pregrant files:\n{pregrant_files}")

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
            if source_type == 'granted_package_files':
                elastic_source = elastic_source_patent
                files_list = granted_files
            else:
                elastic_source = elastic_source_pregrant
                files_list = pregrant_files
            for idx, fname in enumerate(files):
                with fname as fname:
                    config_name = "{dname}-{stype}-{fname}".format(
                        dname="es_data_load/pv/mappings/production",
                        stype=source_type,
                        fname=".".join(files_list[idx].split(".")[:-1]),
                    )
                    current_operation = json.load(open(fname, "r"))
                    index_w_o_suffix = current_operation["target_setting"]["index"]
                    index = "{idx}{suffix}".format(idx=index_w_o_suffix, suffix=suffix)
                    source_settings = current_operation["source_setting"]
                    source_settings = partially_inject_databases(
                        source_settings,
                        elastic_source=elastic_source,
                        reporting_source=reporting_source_patent,
                    )
                    if "nested_fields" in source_settings:
                        for nested_operation_key in source_settings["nested_fields"]:
                            source_settings["nested_fields"][
                                nested_operation_key
                            ] = partially_inject_databases(
                                source_settings["nested_fields"][nested_operation_key],
                                elastic_source=elastic_source,
                                reporting_source=reporting_source_patent,
                            )
                    current_operation["source_setting"] = source_settings
                    current_operation["target_setting"]["index"] = index
                    configs[config_name] = current_operation

        load_configuration = PVLoadConfiguration(load_configs=configs)
        return load_configuration
