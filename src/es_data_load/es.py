import configparser
import logging
import typing

import elastic_transport
from elasticsearch import Elasticsearch


class ElasticsearchWrapper:
    """
    Wrapper for Python Elasticsearch client. Allows bulk indexing of data

    Args:
        hoststring: Elasticsearch host (including port)
        timeout: connection timeout
        username: Elasticsearch username
        password: Elasticsearch password

    """

    def __init__(
            self,
            hoststring: str,
            timeout: int = None,
            username: str = None,
            password: str = None,
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        if username is not None:
            self.es = Elasticsearch(
                hosts=hoststring, basic_auth=(username, password), timeout=timeout
            )
            self.logger.debug("Connecting with credentials")
        else:
            self.logger.debug("Connecting without credentials")
            self.es = Elasticsearch(hosts=hoststring, timeout=timeout)
        self.logger.info(self.es.info())

    @classmethod
    def from_config(cls, config: configparser.ConfigParser) -> "ElasticsearchWrapper":
        """
        Build ElasticsearchWrapper object from config(ini)file

        Args:
            config: config object loaded from configparser

        Returns:
            ElasticsearchWrapper object
        """
        return cls(
            hoststring=config["ELASTICSEARCH"]["HOST"],
            timeout=int(config["ELASTICSEARCH"].get("TIMEOUT", "120")),
            username=config["ELASTICSEARCH"].get("USER", None),
            password=config["ELASTICSEARCH"].get("PASSWORD", None),
        )

    @classmethod
    def for_localhost(cls) -> "ElasticsearchWrapper":
        """
        Build ElasticsearchWrapper object for localhost instance. No username/password

        Returns:
            ElasticsearchWrapper object
        """
        return cls(hoststring="localhost:9200")

    def bulk_load_es_documents(
            self,
            document_source: typing.Iterable[dict],
            target_settings: dict,
            test: bool,
    ) -> typing.Generator:
        """
        Bulk load documents from tabular data source according to provided load configuratin

        Args:
            document_source: Data Source
            target_settings: dict containing load configuration (target index, indexing batch size and id field)
            test: Boolean indicating if current run should be a test run. (No data is indexed)

        Returns:
            Bulk indexing results
        """
        target_index = target_settings["index"]
        indexing_batch_size = target_settings["indexing_batch_size"]
        id_field = target_settings["id_field"]
        current_batch_size = 0
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html
        action_data_pairs = []
        for data_row in document_source:
            if current_batch_size >= indexing_batch_size:
                current_batch_size = 0
                if test == 1:
                    yield []
                else:
                    r = self.es.bulk(operations=action_data_pairs, refresh=True)
                    yield r
                action_data_pairs = []
            action_data_pairs.append(
                {"index": {"_id": data_row[id_field], "_index": target_index}}
            )
            action_data_pairs.append(data_row)
            current_batch_size += 2
        if test == 1:
            yield []
        else:
            r = self.es.bulk(operations=action_data_pairs, refresh=True)
            yield r
