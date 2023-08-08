import csv
import sys
from abc import ABC

from tqdm import tqdm
import configparser
from pymysql import Connection, Error as PyMySQLError, connect as pymysql_connect

from es_data_load.lib.utilities import csv_lines

from typing import Generator, Tuple


class TabularDataSource(ABC):
    def get_document_count(self, count_source):
        raise NotImplementedError

    def generate_source_chunk(self, *args, **kwargs):
        raise NotImplementedError

    def document_generator(self, **kwargs):
        if not all([x in kwargs for x in ['source', 'field_mapping']]):
            raise Exception("Both 'source' and 'field_mapping' are required parameters")
        chunksize = kwargs.get('chunksize', None)
        source = kwargs.get('source')
        field_mapping = kwargs.get('field_mapping')
        offset = 0
        nested_field_source_settings = kwargs.get('nested_fields', {})
        total_count = self.get_document_count(count_source=kwargs.get('count_source'))
        pbar = tqdm(total=total_count, desc=kwargs.get('load_name', 'Load:'))
        key_field = kwargs.get('key_field')
        while True:
            exists = False
            main_document = self.generate_source_chunk(source, field_mapping, offset=offset, **kwargs)
            sub_documents = {}

            for nested_field, nested_field_setting in nested_field_source_settings.items():
                sub_source = nested_field_setting['source']
                sub_field_mapping = nested_field_setting['field_mapping']
                sub_documents[nested_field] = {}
                for nested_record in self.generate_source_chunk(sub_source, sub_field_mapping, offset=offset,
                                                                **kwargs):
                    key_data = nested_record[key_field]
                    if key_data not in sub_documents[nested_field]:
                        sub_documents[nested_field][key_data] = []
                    nested_record.pop(key_field)
                    sub_documents[nested_field][key_data].append(nested_record)

            for data_row in main_document:
                exists = True
                key_data = data_row[key_field]
                for nested_field, nested_records in sub_documents.items():
                    if key_data in nested_records:
                        data_row[nested_field] = nested_records[key_data]
                pbar.update(1)
                yield data_row
            if not exists or chunksize is None:
                break
            offset = offset + chunksize


class DelimitedDataSource(TabularDataSource):
    def __init__(self, **kwargs):
        super().__init__()
        self.delimiter = kwargs.get('delimiter')
        if self.delimiter == 'tab':
            self.delimiter = "\t"

    @classmethod
    def from_config(cls, config):
        if config['SOURCE']['TYPE'] != 'delimited':
            raise Exception("Source type should be delimited")
        return cls(delimiter=config["SOURCE"]['DELIMITER'])

    def get_document_count(self, count_source):
        filename = count_source
        return csv_lines(filename, delimiter=self.delimiter)

    def generate_source_chunk(self, *args, **kwargs):
        filename = args[0]
        field_mapping = args[1]
        csv.field_size_limit(sys.maxsize)
        with open(filename) as fp:
            reader = csv.reader(fp, delimiter=self.delimiter)
            for line in reader:
                yield {field_name: line[idx] for field_name, idx in field_mapping.items()}


class MySQLDataSource(TabularDataSource):
    connection: Connection

    def execute_query(self, query: str, test: int) -> Generator:
        """
        Yields query results as generator of tuples.

        :param query: Query to execute
        """
        if test == 1:
            end_position = query.rfind(';')
            if end_position == len(query) - 1:
                query = f"{query[0:end_position]} where 1 = 0;"
            elif end_position < 0:
                query = f"{query} where 1 = 0;"
            else:
                raise Exception("Multiple ; found in query")
        attempt = 0
        while True:
            try:
                with self.connection.cursor() as source_cursor:
                    source_cursor.execute(query=query)
                    yield from source_cursor
                break
            except BrokenPipeError:
                attempt += 1
                if attempt > 3:
                    raise
                self.connect()
                continue
            except PyMySQLError as e:
                print(query)
                raise e

    def __init__(self, **kwargs) -> None:
        """
        MySQL Source

        :rtype: MySQLDataSource
        :param connection: PyMYSQL connection
        :param int retries: Number of times to retry a query before giving up
        :param int test: Test flag. Adds where 1=0 to queries. Can be used to test if source tables exist.
        """
        self.connection = kwargs.get('connection')
        self.retries = kwargs.get('retries', 3)
        self.connect()

    @classmethod
    def from_config(cls, config: configparser.ConfigParser) -> object:
        """
        Create an instance of MySQL source by using connection credentials from config object

        :param object config: configparser object
        :param int test: test flag
        :return: instance of MySQLDataSource
        """
        if config['SOURCE']['TYPE'] != 'mysql':
            raise Exception("Source type should be mysql")
        return cls(connection=pymysql_connect(host=config['SOURCE']['HOSTNAME'],
                                              user=config['SOURCE']['USERNAME'],
                                              password=config['SOURCE']['PASSWORD'],
                                              charset='utf8mb4', defer_connect=True,
                                              port=int(config['SOURCE']['PORT'])),
                   retries=int(config['SOURCE']['RETRIES']))

    def connect(self):
        """
        Open PyMSQL connection. Useful when deferred connection object is used.

        """
        if not self.connection.open:
            self.connection.connect()

    def get_document_count(self, count_source: str) -> int:
        """
        Get total number of records available in the current data source

        :param count_source: count query representing the data source
        :return: Number of records
        """
        count_query = count_source
        with self.connection.cursor() as count_cursor:
            count_cursor.execute(count_query)
            return count_cursor.fetchall()[0][0]

    def generate_source_chunk(self, *args, **kwargs):
        """
        Returns a generator for a query. Applies any configured limit/offset rules.

        :rtype: Generator[Tuple]
        :param str query: first positional argument. Templated query with limit/offset
        :param int chunksize: Number of records to fetch
        :param int offset: Number of records to skip
        """
        limit = int(kwargs.get('chunksize', 10000))
        offset = int(kwargs.get('offset'))
        test = int(kwargs.get('test', '0'))
        query_template = args[0]
        mapping = args[1]
        query = query_template.format(limit=limit, offset=offset)
        for record in self.execute_query(query=query, test=test):
            yield {field_name: record[idx] for field_name, idx in mapping.items()}
