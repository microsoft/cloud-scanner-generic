# cloud-scanner-generic

Generic package of adapters for [cloud-scanner]() library. Includes services and their required configurations.

### Running Locally

You can run unit tests in a Python 3.6 virtual environment:

```python
virtualenv env
source env/bin/activate
(env) pip install -r requirements.txt
(env) python -m pytest
```

### Storage Adapters
- ElasticSearch
    - Needs `ELASTIC_SEARCH_URL` and `ELASTIC_SEARCH_ACCESS_KEY`
- MySQL
    - Needs `MYSQL_HOST`, `MYSQL_DATABASE`, `MYSQL_USERNAME` and `MYSQL_PASSWORD`
- Rest API Post Request
    - Needs `REST_STORAGE_URL`