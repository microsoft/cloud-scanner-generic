from unittest.mock import patch
from .unittest_base import TestCase
from cloud_scanner_generic.services.request_helper import RequestHelper
from requests import Session

class TestRequestHelper(TestCase):
    @patch.object(Session, "post")
    def test_request_helper_post(self, mock_post):
        test_url = "https://my-company.com/test"
        test_payload = {
            "name": "foobar",
            "type": "test"
        }

        RequestHelper.post(test_url, json=test_payload)
        mock_post.assert_called_once_with(test_url, json=test_payload)

