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
