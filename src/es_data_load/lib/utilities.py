import configparser
import csv
import json
import logging
import os
import sys
from typing import List

from elasticsearch import NotFoundError, BadRequestError

logger = logging.getLogger("es-data-load")


def load_config_dict_from_json_files(directories: List):
    configs = {}
    for directory in directories:
        if not os.path.exists(directory) or not os.path.isdir(directory):
            raise Exception(f"{directory} is not a folder")
        for fname in os.listdir(directory):
            if fname.endswith(".json"):
                config_name = "{dname}-{fname}".format(
                    dname=directory, fname=".".join(fname.split(".")[:-1])
                )
                json_file = os.path.join(directory, fname)
                configs[config_name] = json.load(open(json_file, "r"))

    return configs


def create_recreate_index(
    es, index_name, aliases, fields, delete_index=False, exists_ok=True
):
    if delete_index:
        try:
            es.indices.delete(index=index_name)
        except NotFoundError:
            pass
    try:
        es.indices.create(index=index_name, body={"mappings": {"properties": fields}})
    except BadRequestError as e:
        if not exists_ok or e.args[0] != "resource_already_exists_exception":
            raise
    for alias in aliases:
        es.indices.put_alias(index=index_name, name=alias)


def csv_lines(filename, *args, **kwargs):
    delimiter = kwargs.get("delimiter", ",")
    quoting = kwargs.get("quoting", csv.QUOTE_NONNUMERIC)
    quotechar = kwargs.get("quotechar", '"')
    header = kwargs.get("header", False)
    if header:
        counter = -1
    else:
        counter = 0
    csv.field_size_limit(sys.maxsize)
    with open(filename) as fp:
        reader = csv.reader(
            fp, delimiter=delimiter, quotechar=quotechar, quoting=quoting
        )
        for line in reader:
            counter += 1
    return counter


def get_config(config_file_to_use):
    # project_root = os.environ['PROJECT_ROOT']
    # config_file_to_use = "./resources/config.ini"
    config = configparser.ConfigParser()
    config.read(config_file_to_use)
    return config


def get_source(config, source_type="mysql"):
    from es_data_load.DataSources import (
        TabularDataSource,
        MySQLDataSource,
        DelimitedDataSource,
    )

    source = TabularDataSource()
    if source_type == "mysql":
        source = MySQLDataSource.from_config(config=config)
    if source_type == "delimited":
        source = DelimitedDataSource.from_config(config=config)
    return source


def generate_load_statistics(responses):
    batch_count = 0
    record_count = 0
    total_duration = 0
    error_status = False
    errors = set()
    for response in responses:
        batch_count += 1
        if "items" in response:
            record_count = record_count + len(response["items"])
            total_duration += response["took"]
            if response.get("errors", None):
                for error_items in response["items"]:
                    if "error" in error_items["create"]:
                        errors.add(error_items["create"]["error"]["type"])
                error_status = True
    logger.info(f"Load completed. Errors: {errors}")
    return {
        "batches": batch_count,
        "record_count": record_count,
        "complete": True,
        "success": not error_status,
        "duration": total_duration,
        "errors": errors,
    }
