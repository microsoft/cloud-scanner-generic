import pymysql

from cloud_scanner.contracts import TableStorage, register_resource_storage
from cloud_scanner_generic.config import MySqlConfig


@register_resource_storage("mysql", lambda: MySqlResourceStorage.create())
class MySqlResourceStorage(TableStorage):
    def __init__(self, config: MySqlConfig):
        self._connection = None
        self._config = config

    def __enter__(self):
        if self._connection is None:
            self._connection = pymysql.connect(
                host=self._config.host,
                db=self._config.database,
                user=self._config.username,
                password=self._config.password,
                cursorclass=pymysql.cursors.DictCursor)

        return self

    def __exit__(self, type, value, traceback):
        if self._connect is not None:
            self._connection.close()

    def _connect(self) -> pymysql.Connection:
        if self._connection is None:
            self.__enter__()
        else:
            self._connection.ping(True)

        return self._connection

    def check_entry_exists(self, entry):
        resource = self.query(entry["PartitionKey"], entry["RowKey"])
        return False if resource is None else True

    def write(self, resource):
        try:
            entry = resource.to_dict()
            connection = self._connect()
            with connection.cursor() as cursor:
                sql = '''INSERT INTO aws_resources
                        (resourceid, arn, name, type, region, account, service,
                         hash, updatecycle, created_at, updated_at)
                        VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, UNIX_TIMESTAMP(),
                         NOW(), NOW())
                        ON DUPLICATE KEY UPDATE
                        resourceid = %s,
                        arn = %s,
                        name = %s,
                        type = %s,
                        region = %s,
                        account = %s,
                        service = %s,
                        hash = %s,
                        updatecycle = UNIX_TIMESTAMP(),
                        updated_at = NOW()
                        '''

                args = (
                    entry["id"],
                    entry["id"],
                    entry["name"],
                    entry["type"],
                    entry["location"],
                    entry["accountId"],
                    entry["providerType"],
                    "SHA1",
                    entry["id"],
                    entry["id"],
                    entry["name"],
                    entry["type"],
                    entry["location"],
                    entry["accountId"],
                    entry["providerType"],
                    "SHA1")

                rowCount = cursor.execute(sql, args)

                if rowCount == 0:
                    raise ValueError("Error writing resource")
        finally:
            connection.commit()

    def query_list(self) -> list:
        connection = self._connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM aws_resources"
            cursor.execute(sql)

            # TODO Convert to list of resources and return
            return cursor.fetchall()

    def query(self, partition_key, row_key):
        connection = self._connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM aws_resources WHERE resourceid = %s"
            rowCount = cursor.execute(sql, row_key)

            if rowCount == 0:
                return None

            # TODO- Convert to resource and return
            return cursor.fetchone()

    def delete(self, partition_key, row_key):
        try:
            connection = self._connect()
            with connection.cursor() as cursor:
                sql = "DELETE FROM aws_resources WHERE resourceid = %s"
                rowCount = cursor.execute(sql, row_key)

            if rowCount == 0:
                raise ValueError("Error deleting resource from mysql database")
        finally:
            connection.commit()

    @staticmethod
    def create():
        return MySqlResourceStorage(MySqlConfig())
