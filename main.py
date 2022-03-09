import argparse
import configparser
import os
import pprint

from LoadJob import LoadJob


def get_config(config_file_to_use):
    # project_root = os.environ['PROJECT_ROOT']
    # config_file_to_use = "./resources/config.ini"
    config = configparser.ConfigParser()
    config.read(config_file_to_use)
    return config


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
    config = get_config(cfile)
    loadjob = LoadJob.generate_load_job_from_folder(directory=args.d[0], connection_config=config)
    loadjob.process_all_load_operations(args.o[0])
    operations = loadjob.get_load_operation_names()
    for operation in operations:
        print("------------")
        print(operation)
        status = loadjob.get_load_job_status(operation)
        pprint.pprint(status)
