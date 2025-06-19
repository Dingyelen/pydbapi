# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-06-02 15:27:41
# @Last Modified by:   longfengpili
# @Last Modified time: 2025-06-19 13:58:00
# @github: https://github.com/longfengpili


import threading
from datetime import date

import clickhouse_connect

from pydbapi.db import DBMixin, DBFileExec
from pydbapi.model import ColumnModel, ColumnsModel
from pydbapi.sql import SqlCompile
from pydbapi.conf import AUTO_RULES


import logging
mytrinologger = logging.getLogger(__name__)


class SqlClickhouseCompile(SqlCompile):
    '''[summary]

    [description]
        构造mysql sql
    Extends:
        SqlCompile
    '''

    def __init__(self, tablename):
        super(SqlClickhouseCompile, self).__init__(tablename)


class ClickhouseDB(DBMixin, DBFileExec):
    _instance_lock = threading.Lock()

    def __init__(self, host: str, user: str, password: str, database: str, 
                 port: int = 8443, safe_rule: bool = True, 
                 **kwargs: dict):
        '''[summary]
        
        [init]
        
        Args:
            host ([str]): [host]
            user ([str]): [username]
            password ([str]): [password]
            database ([str]): [database]
            port (number): [port] (default: `8443`)
            safe_rule (bool): [safe rule] (default: `True`)
            kwargs (dict): [其他trino支持参数，可以询问开发同学，例如source、timezone等]
        '''

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.kwargs = kwargs
        super(ClickhouseDB, self).__init__()
        self.auto_rules = AUTO_RULES if safe_rule else None
        self.dbtype = 'clickhouse'

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(ClickhouseDB, '_instance'):
    #         with ClickhouseDB._instance_lock:
    #             if not hasattr(ClickhouseDB, '_instance'):
    #                 ClickhouseDB._instance = super().__new__(cls)

    #     return ClickhouseDB._instance

    @classmethod
    def get_instance(cls, *args, **kwargs):
        # mytrinologger.info(ClickhouseDB._instance_lock)
        if not hasattr(ClickhouseDB, '_instance'):
            # mytrinologger.info(ClickhouseDB._instance_lock)
            with ClickhouseDB._instance_lock:
                if not hasattr(ClickhouseDB, '_instance'):
                    ClickhouseDB._instance = cls(*args, **kwargs)

        return ClickhouseDB._instance

    def get_conn(self):
        if not hasattr(ClickhouseDB, '_conn'):
            with ClickhouseDB._instance_lock:
                if not hasattr(ClickhouseDB, '_conn'):
                    conn = clickhouse_connect.get_client(host=self.host, user=self.user,
                                                         database=self.database,
                                                         port=self.port, http_scheme="https",
                                                         **self.kwargs)
                    mytrinologger.info(f'connect {self.__class__.__name__}({self.user}@{self.host}:{self.port}/{self.database})')  # noqa: E501
                    ClickhouseDB._conn = conn
        return ClickhouseDB._conn

    def cur_columns(self, cursor):
        pass

    