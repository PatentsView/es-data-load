import pymysql

from source.TabularDataSource import TabularDataSource


class MySQLDataSource(TabularDataSource):
    def execute_query(self, query):
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
            except pymysql.Error as e:
                print(query)
                raise e

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
        mapping = args[1]
        query = query_template.format(limit=limit, offset=offset)
        for record in self.execute_query(query=query):
            yield {field_name: record[idx] for field_name, idx in mapping.items()}
