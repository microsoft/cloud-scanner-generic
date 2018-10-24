import urllib

from cloud_scanner.config import ProcessConfig
from cloud_scanner.contracts import (
    Resource, register_resource_storage, TableStorage)

from cloud_scanner_generic.services.errors import NotSupportedError
from cloud_scanner_generic.services.request_helper import RequestHelper


@register_resource_storage("rest_storage_service",
                           lambda: RestStorageService.create())
class RestStorageService(TableStorage):

    _url = None

    def __init__(self, url):
        self._url = url

    @staticmethod
    def create():
        url = ProcessConfig().rest_storage_url
        return RestStorageService(url)

    def write(self, resource: Resource):
        if resource is None:
            raise ValueError("resource is required")

        # Query string params are required in addition to the POST body
        entry = resource.to_normalized_dict()

        query = urllib.parse.urlencode({
            'AccountId': entry["OwnerId"],
            'ResourceType': entry["ResourceType"],
            'Region': entry["Region"]
        })

        post_url = f'{self._url}?{query}'
        RequestHelper.post(post_url, json=[entry])

    def write_entries(self, resource_list):
        if resource_list is None:
            raise ValueError("resource_list is required")

        entries = [resource.to_normalized_dict() for resource in resource_list]
        if len(entries) == 0:
            return

        query = urllib.parse.urlencode({
            'AccountId': entries[0]["OwnerId"],
            'ResourceType': entries[0]["ResourceType"],
            'Region': entries[0]["Region"]
        })

        post_url = f'{self._url}?{query}'
        RequestHelper.post(post_url, json=entries)

    def check_entry_exists(self, entry):
        raise NotSupportedError("write not currently supported")

    def query_list(self):
        return NotSupportedError("query_list not currently supported")

    def query(self, partition_key, row_key):
        return NotSupportedError("query not currently supported")

    def delete(self, partition_key, row_key):
        raise NotSupportedError("delete not currently supported")
