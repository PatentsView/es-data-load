import pymysql

from source.TabularDataSource import TabularDataSource


class MySQLDataSource(TabularDataSource):
    def __init__(self, config):
        if config['SOURCE']['TYPE'] != 'mysql':
            raise Exception("Source type should be mysql")
        self.connection = pymysql.connect(host=config['SOURCE']['HOSTNAME'],
                                          user=config['SOURCE']['USERNAME'],
                                          password=config['SOURCE']['PASSWORD'],
                                          charset='utf8mb4', defer_connect=True,
                                          port=int(config['SOURCE']['PORT']))
        self.retries = int(config['SOURCE']['RETRIES'])
        self.connect()

    def connect(self):
        if not self.connection.open:
            self.connection.connect()

    def get_document_count(self, count_source):
        count_query = count_source
        with self.connection.cursor() as count_cursor:
            count_cursor.execute(count_query)
            return count_cursor.fetchall()[0][0]

    def generate_source_chunk(self, *args, **kwargs):
        limit = int(kwargs.get('chunksize', 10000))
        offset = int(kwargs.get('offset'))
        query_template = args[0]
        query = query_template.format(limit=limit, offset=offset)
        attempt = 0
        while True:
            try:
                with self.connection.cursor() as source_cursor:
                    source_cursor.execute(query=query)
                    for data_row in source_cursor:
                        yield data_row
                break
            except BrokenPipeError:
                attempt += 1
                if attempt > 3:
                    raise
                self.connect()
                continue
