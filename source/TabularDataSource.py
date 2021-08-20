from abc import ABC

from tqdm import tqdm


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
        total_count = self.get_document_count(count_source=kwargs.get('count_source'))
        pbar = tqdm(total=total_count)
        while True:
            exists = False
            for data_row in self.generate_source_chunk(source, offset=offset, **kwargs):
                exists = True
                pbar.update(1)
                yield {field_name: data_row[idx] for idx, field_name in field_mapping.items()}
            if not exists or chunksize is None:
                break
            offset = offset + chunksize
