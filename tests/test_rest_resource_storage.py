from unittest.mock import patch

import requests

from cloud_scanner_generic.services import RestStorageService
from cloud_scanner.contracts import Resource
from .unittest_base import TestCase
from cloud_scanner_generic.services.request_helper import RequestHelper


class TestRestResourceStorage(TestCase):
    test_url = "https://test.domain.com/intake"

    def _create_provider(self):
        return RestStorageService(TestRestResourceStorage.test_url)

    @patch.object(RequestHelper, "post")
    def test_write_with_resource(self, mock_post):
        provider = self._create_provider()

        resource_json = {
            "id": "/subscriptions/foo/resourcegroups/bar/Microsoft.Test/resources/baz",
            "accountId": "abcxyz123",
            "name": "Test Resource",
            "type": "Microsoft.Test",
            "location": "westus",
            "tags": {
                "a": "1",
                "b": "2"
            }
        }

        resource = Resource(resource_json)

        expected_url = f"{TestRestResourceStorage.test_url}?AccountId=abcxyz123&ResourceType=Microsoft_Test&Region=westus"
        expected_entry = resource.to_normalized_dict()

        provider.write_entries([resource])
        mock_post.assert_called_once_with(expected_url, json=[expected_entry])

    def test_write_with_none_raises_value_error(self):
        provider = self._create_provider()
        self.assertRaises(ValueError, lambda: provider.write(None))

    @patch.object(RequestHelper, "post")
    def test_with_empty_resource_list_no_post_calls(self, mock_post):
        provider = self._create_provider()
        provider.write_entries([])
        assert not mock_post.called

