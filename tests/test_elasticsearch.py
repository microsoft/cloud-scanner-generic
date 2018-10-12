# This test is not meant to run in CI.
# This is an integration test that is meant to validate the Elasticsearch provider.

import json
import uuid
from unittest.mock import patch, MagicMock

import pytest

from cloud_scanner_generic.config import ElasticSearchConfig
from cloud_scanner_generic.services import ElasticSearch
from cloud_scanner_generic.simulators import ResourceServiceSimulator
from .unittest_base import TestCase


class TestScheduler(TestCase):

    def setup(self):
        resource_service = ResourceServiceSimulator()
        self._es_instance = ElasticSearch.create()
        self._resources = resource_service.get_resources()

    @pytest.mark.skip(reason="Integration test")
    def test_insert_query_and_delete(self):
        self.setup()

        for resource in self._resources:
            resource_raw = resource.to_str()
            data = json.loads(resource_raw)

            # insert the entry onto ES
            self._es_instance.write(data)

            # for data in datastore:
            location = data['location']

            # save partition and row key for access later
            partition_key = location
            row_key = str(uuid.uuid3(uuid.NAMESPACE_DNS, data['id']))

            # verify the entry was written to the table
            retrieved_entry = None
            retrieved_entry = self._es_instance.query(partition_key, row_key)

            # verify the entry was inserted on ES
            self.assertIsNotNone(retrieved_entry, "No entry was inserted to Elasticsearch instance")

    @patch.object(ElasticSearch, 'write', return_value=None)
    def test_write_runs_once(self, mock_method):
        elastic_search = ElasticSearch(self.getConfig())
        elastic_search.write(resource="SOME_RESOURCE")
        mock_method.assert_called_once_with(resource="SOME_RESOURCE")

    @patch.object(ElasticSearch, 'query', return_value=None)
    def test_query_runs_once(self, mock_method):
        elastic_search = ElasticSearch(self.getConfig())
        elastic_search.query("P_KEY", "R_KEY")
        mock_method.assert_called_once_with("P_KEY", "R_KEY")

    @patch.object(ElasticSearch, 'query_list', return_value=None)
    def test_query_list_runs_once(self, mock_method):
        elastic_search = ElasticSearch(self.getConfig())
        elastic_search.query_list()
        mock_method.assert_called_once_with()

    @patch.object(ElasticSearch, 'delete', return_value=None)
    def test_delete_runs_once(self, mock_method):
        elastic_search = ElasticSearch(self.getConfig())
        elastic_search.delete("P_KEY", "R_KEY")
        mock_method.assert_called_once_with("P_KEY", "R_KEY")


    @staticmethod
    def getConfig():
        config = ElasticSearchConfig()
        config.get_property = MagicMock(return_value="PROPERTY_VALUE")
        return config