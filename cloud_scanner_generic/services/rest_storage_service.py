import urllib

import requests

from cloud_scanner.config import ProcessConfig
from cloud_scanner.contracts.resource import Resource
from cloud_scanner.contracts.resource_storage_factory import register_resource_storage
from cloud_scanner.contracts.table_storage import TableStorage
from .request_helper import RequestHelper


@register_resource_storage(
    "rest_storage_service",
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
        raise NotImplementedError("write not currently supported")

    def query_list(self):
        return []

    def query(self, partition_key, row_key):
        return None

    def delete(self, partition_key, row_key):
        raise NotImplementedError("delete not currently supported")
