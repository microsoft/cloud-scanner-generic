from random import randint

import pytest

from cloud_scanner_generic.services import MySqlResourceStorage
from cloud_scanner_generic.config import MySqlConfig
from cloud_scanner.contracts import Resource
from .unittest_base import TestCase


@pytest.mark.skip(reason="Integration test")
class TestMySqlResourceStorage(TestCase):
    def _create_provider(self):
        return MySqlResourceStorage(MySqlConfig())

    def test_crud_mysql_resources(self):
        resource_id = f'/resources/foo/bar/{randint(1,1000)}'
        account_id = randint(1, 100)
        resource_name = f'resource {resource_id}'

        resource_dict = {
            "id": resource_id,
            "providerType": "Azure",
            "name": resource_name,
            "accountId": account_id,
            "location": "eastus2",
            "type": "vm"
        }
        resource = Resource(resource_dict)

        with self._create_provider() as provider:
            # Insert the resource
            provider.write(resource.to_dict())

            # Query the resource
            query_result = provider.query(None, resource.id)
            self.assertIsNotNone(query_result)

            # Update the resource
            resource.name = resource.name + " udpated"
            provider.write(resource.to_dict())

            # Re-Query the resource
            query_result = provider.query(None, resource.id)
            self.assertEqual(query_result["name"], resource.name)

            #
            query_results = provider.query_list()
            self.assertGreater(len(query_results), 0)

            # Delete the resource
            provider.delete(None, resource.id)

            # Re-Query the resource
            query_result = provider.query(None, resource.id)
            self.assertIsNone(query_result)

    def test_query_list(self):
        resources = []
        resources_count = 10

        with self._create_provider() as provider:
            for i in range(resources_count):
                resource_id = f'/resources/foo/bar/resource-{i}'
                account_id = randint(1, 100)
                resource_name = f'resource {resource_id}'

                resource_dict = {
                    "id": resource_id,
                    "providerType": "Azure",
                    "name": resource_name,
                    "accountId": account_id,
                    "location": "eastus2",
                    "type": "vm"
                }
                resource = Resource(resource_dict)
                provider.write(resource.to_dict())
                resources.append(resource)

            results = provider.query_list()
            self.assertGreaterEqual(len(results), resources_count)

            for resource in resources:
                provider.delete(None, resource.id)
