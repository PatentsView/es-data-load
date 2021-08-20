import csv
import sys


def csv_lines(filename, *args, **kwargs):
    delimiter = kwargs.get('delimiter', ",")
    quoting = kwargs.get('quoting', csv.QUOTE_NONNUMERIC)
    quotechar = kwargs.get('quotechar', '"')
    header = kwargs.get('header', False)
    if header:
        counter = -1
    else:
        counter = 0
    csv.field_size_limit(sys.maxsize)
    with open(filename) as fp:
        reader = csv.reader(fp, delimiter=delimiter, quotechar=quotechar, quoting=quoting)
        for line in reader:
            counter += 1
    return counter
