from typing import Optional


class DatabaseConfig(object):

    def __init__(
        self, *,
        dialect:str,
        host:str,
        port:Optional[str],
        username:str,
        password:str,
        db:str,
        api:str=None,
    ):
        self._dialect = dialect
        self._api = api
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._db = db

    def build_connection_uri(self):
        return '{schema}://{username}:{password}@{host}:{port}/{db}'.format(
            schema=self._build_schema(),
            username=self._username,
            password=self._password,
            host=self._host,
            port=self._port,
            db=self._db,
        )
    
    def _build_schema(self):
        return '{dialect}+{api}'.format(dialect=self._dialect, api=self._api) if self._api else self._dialect


class BaseConfig(object):
    DB_CONFIG:DatabaseConfig


class DefaultConfig(BaseConfig):
    DB_CONFIG = DatabaseConfig(
        dialect='postgres', 
        host='localhost', 
        port=5432, 
        username='postgres', 
        password='1234',
        db='testing_tool',
    )

config = DefaultConfig()