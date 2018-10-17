from cloud_scanner.config import Config


class ElasticSearchConfig(Config):

    @property
    def access_url(self):
        return self.get_property("ELASTIC_SEARCH_URL")

    @property
    def access_key(self):
        return self.get_property("ELASTIC_SEARCH_ACCESS_KEY")
