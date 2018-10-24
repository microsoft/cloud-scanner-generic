import uuid

from elasticsearch import Elasticsearch

from cloud_scanner.contracts import TableStorage, register_resource_storage
from cloud_scanner_generic.config import ElasticSearchConfig


@register_resource_storage('elastic_serach', lambda: ElasticSearch.create())
class ElasticSearch(TableStorage):
    """ElasticSearch provider for TableStorage."""

    def __init__(self, config: ElasticSearchConfig):
        self._es_instance = Elasticsearch(
            config.access_url, http_auth=('elastic', config.access_key))
        self._doc_type = 'entries'

    def write(self, resource):
        """Write resource to table.

        :param resource: Expecting Resource object
            (see Common.Contracts.Resource)
        :return: None
        """
        entry = resource.to_dict()
        location = entry['location']
        identifier = str(uuid.uuid3(uuid.NAMESPACE_DNS, entry['id']))
        self._es_instance.index(
            index=location, doc_type=self._doc_type, id=identifier, body=entry)

    def query(self, partition_key, row_key):
        """Get entry with specified partition and row keys.

        :param partition_key: Partition key for entry
        :param row_key: Row key for entry
        :return: Entity if found, None otherwise
        """
        task = self._es_instance.get(
            index=partition_key, doc_type=self._doc_type, id=row_key)
        return task

    def query_list(self):
        """Get entities from table.

        :return: List of entities from table
        """
        return self._es_instance.search("*")

    def delete(self, partition_key, row_key):
        """Delete entry with specified partition and row keys.

        :param partition_key: Partition key for entry
        :param row_key: Row key for entry
        :return: None
        """
        self._es_instance.delete(
            index=partition_key, doc_type=self._doc_type, id=row_key)

    @staticmethod
    def create():
        """Initialize ElasticSearch service.

        :return: ElasticSearch service object
        """
        return ElasticSearch(ElasticSearchConfig())
