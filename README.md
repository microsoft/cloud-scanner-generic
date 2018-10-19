# cloud-scanner-generic

Generic package of adapters for [cloud-scanner](https://github.com/Microsoft/cloud-scanner) library. Includes services and their required configurations.

### Running Locally

You can run unit tests in a Python 3.6 virtual environment:

```python
virtualenv env
source env/bin/activate
(env) pip install --index-url https://test.pypi.org/simple/ -r requirements-test.txt --extra-index-url https://pypi.org/simple/ -r requirements.txt
(env) pytest
```

### Required environment variables to run with cloud_scanner

#### Storage Adapters
- ElasticSearch
    - Needs `ELASTIC_SEARCH_URL` and `ELASTIC_SEARCH_ACCESS_KEY`
- MySQL
    - Needs `MYSQL_HOST`, `MYSQL_DATABASE`, `MYSQL_USERNAME` and `MYSQL_PASSWORD`
- Rest API Post Request
    - Needs `REST_STORAGE_URL`

# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
