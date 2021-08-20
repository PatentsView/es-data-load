import csv
import sys

from lib.utilities import csv_lines
from source.TabularDataSource import TabularDataSource


class DelimitedDataSource(TabularDataSource):

    def __init__(self, config):
        super().__init__()
        if config['SOURCE']['TYPE'] != 'delimited':
            raise Exception("Source type should be delimited")
        self.delimiter = config["SOURCE"]['DELIMITER']
        if self.delimiter == 'tab':
            self.delimiter = "\t"

    def get_document_count(self, count_source):
        filename = count_source
        return csv_lines(filename, delimiter=self.delimiter)

    def generate_source_chunk(self, *args, **kwargs):
        filename = args[0]
        field_mapping = kwargs.get('field_mapping')
        csv.field_size_limit(sys.maxsize)
        with open(filename) as fp:
            reader = csv.reader(fp, delimiter=self.delimiter)
            for line in reader:
                yield {field_name: line[idx] for idx, field_name in field_mapping.items()}
