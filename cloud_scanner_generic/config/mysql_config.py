from cloud_scanner.config import Config


class MySqlConfig(Config):

    @property
    def host(self):
        return self.get_property('MYSQL_HOST')

    @property
    def database(self):
        return self.get_property('MYSQL_DATABASE')

    @property
    def username(self):
        return self.get_property('MYSQL_USERNAME')

    @property
    def password(self):
        return self.get_property('MYSQL_PASSWORD')
