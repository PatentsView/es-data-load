import argparse
import pprint

from es_data_load.specification import LoadConfiguration
from specification import LoadJob
from es_data_load.es import PatentsViewElasticSearch
from es_data_load.lib.utilities import get_source, get_config
from schema.SchemaManager import PVSchemaManager

if __name__ == '__main__':
    parser_args = {
        '-d': {
            'help': 'Directory containing mapping files',
            'type': str,
            'argument_count': 1
        },
        '-o': {
            'help': 'Type of operation (create or update)',
            'type': str,
            'argument_count': 1
        },
        '-c': {
            'help': 'Elastic config file',
            'type': str,
            'argument_count': 1
        },
        '-t': {
            'help': 'Test Source Query/Data',
            'type': int,
            'argument_count': 1
        }
    }
    cmdparser = argparse.ArgumentParser()
    for argument_flag, argument_settings in parser_args.items():
        cmdparser.add_argument(
            argument_flag, type=argument_settings['type'],
            nargs=argument_settings['argument_count'],
            help=argument_settings['help'])
    args = cmdparser.parse_args()
    cfile = args.c[0]
    test = args.t[0]
    config = get_config(cfile)
    # loadconfigs = LoadConfiguration.generate_load_configuration_from_folder(directories=[args.d[0]])
    loadconfigs = LoadConfiguration.load_default_pv_configuration(suffix="_test")
    es = PatentsViewElasticSearch.from_config(config)
    schema_manager = PVSchemaManager(es=es, suffix='_test')
    schema_manager.create_es_indices()
    mysql_source = get_source(config, source_type='mysql')
    load_job = LoadJob(loadconfigs, mysql_source, es, test=test)
    load_job.process_all_load_operations()
    operations = loadconfigs.get_load_operation_names()
    for operation in operations:
        print("------------")
        print(operation)
        status = load_job.get_load_results(operation)
        pprint.pprint(status)
