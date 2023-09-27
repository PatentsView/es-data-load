import json
from es_data_load.specification import LoadConfiguration

AVAILABLE_MAPPING_FILES = [
    'assignee.json',
    'attorney.json',
    'cpc_class.json',
    'cpc_group.json',
    'cpc_subclass.json',
    'fcitation.json',
    'inventor.json',
    'ipcr.json',
    'locations.json',
    'oreference.json',
    'patents.json',
    'rel_app_text.json',
    'us_application_citations.json',
    'us_patent_citations.json',
    'uspc_mainclass.json',
    'uspc_subclass.json',
    'wipo.json'
]


def partially_inject_databases(configuration, elastic_source, reporting_source):
    source_sql = configuration['source'].format(
        elastic_production_source=elastic_source, reporting_data_source=reporting_source)
    configuration['source'] = source_sql
    if 'count_source' in configuration:
        count_source = configuration['count_source'].format(
            elastic_production_source=elastic_source, reporting_data_source=reporting_source)
        configuration['count_source'] = count_source

    return configuration


class PVLoadConfiguration(LoadConfiguration):
    def __init__(self, load_configs):
        super().__init__(load_configs)

    @classmethod
    def load_default_pv_configuration(cls, suffix="", files=None, elastic_source='elastic_production',
            reporting_source='PatentsView_'):
        if files is None:
            files = AVAILABLE_MAPPING_FILES
        import importlib.resources as pkg_resources
        # schema_file =
        package_files = [pkg_resources.path('es_data_load.pv.mappings.production', fl) for fl in files]

        configs = {}
        for idx, fname in enumerate(package_files):
            with fname as fname:
                config_name = "{dname}-{fname}".format(dname='es_data_load/pv/mappings/production',
                                                       fname=".".join(files[idx].split('.')[:-1]))
                current_operation = json.load(open(fname, "r"))
                index_w_o_suffix = current_operation['target_setting']['index']
                index = "{idx}{suffix}".format(idx=index_w_o_suffix, suffix=suffix)
                source_settings = current_operation["source_setting"]
                source_settings = partially_inject_databases(source_settings,
                                                             elastic_source=elastic_source,
                                                             reporting_source=reporting_source)
                if 'nested_fields' in source_settings:
                    for nested_operation_key in source_settings['nested_fields']:
                        source_settings['nested_fields'][
                            nested_operation_key] = partially_inject_databases(
                            source_settings['nested_fields'][nested_operation_key],
                            elastic_source=elastic_source,
                            reporting_source=reporting_source)
                current_operation["source_setting"] = source_settings
                current_operation['target_setting']['index'] = index
                configs[config_name] = current_operation

        load_configuration = PVLoadConfiguration(load_configs=configs)
        return load_configuration
