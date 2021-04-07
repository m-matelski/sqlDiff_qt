from collections import namedtuple
from dataclasses import dataclass
from traceback import print_exc
from typing import List

import jaydebeapi as jdbc_api

INT_MAX = 2147483647

connect = jdbc_api.connect


def get_result_set_meta_data_methods_mapping(meta):
    """
    JDBC column metadata to field mapping.
    :param meta: JDBC ResultSetMetaData instance
    :return: field to column metadata JDBC method mapping
    """
    # https://docs.oracle.com/en/java/javase/11/docs/api/java.sql/java/sql/ResultSetMetaData.html
    d = {
        'catalog_name': meta.getCatalogName,
        'display_size': meta.getColumnDisplaySize,
        'label': meta.getColumnLabel,
        'name': meta.getColumnName,
        'type_code': meta.getColumnType,
        'type_name': meta.getColumnTypeName,
        'precision': meta.getPrecision,
        'scale': meta.getScale,
        'schema_name': meta.getSchemaName,
        'table_name': meta.getTableName,
        'is_nullable': meta.isNullable,
        'is_auto_increment': meta.isAutoIncrement,
        'is_case_sensitive': meta.isCaseSensitive,
        'is_currency': meta.isCurrency,
        'is_definitely_writeable': meta.isDefinitelyWritable,
        'is_read_only': meta.isReadOnly,
        'is_searchable': meta.isSearchable,
        'is_signed': meta.isSigned,
        'is_writable': meta.isWritable,
    }
    return d


@dataclass
class JDBCFieldDescription:
    """
    Column metadata fetched from ResultSetMetaData
    """
    catalog_name: str
    display_size: int
    label: str
    name: str
    type_code: int
    type_name: str
    precision: int
    scale: int
    schema_name: str
    table_name: str
    is_nullable: int
    is_auto_increment: bool
    is_case_sensitive: bool
    is_currency: bool
    is_definitely_writeable: bool
    is_read_only: bool
    is_searchable: bool
    is_signed: bool
    is_writable: bool


class JDBCResultDescription:
    """
    Stores metadata for database and all query result columns.
    """

    @staticmethod
    def _get_result_meta_by_cursor_meta(meta) -> List[JDBCFieldDescription]:
        meta_methods = get_result_set_meta_data_methods_mapping(meta)
        description = []
        for i in range(1, meta.getColumnCount() + 1):
            field_description = {attribute: method(i) for attribute, method in meta_methods.items()}
            description.append(JDBCFieldDescription(**field_description))
        return description

    @staticmethod
    def _get_result_meta_by_prepare_statement(cursor: jdbc_api.Cursor, sql_statement: str):
        prep = cursor._connection.jconn.prepareStatement(sql_statement)
        meta = prep.getMetaData()
        return JDBCResultDescription._get_result_meta_by_cursor_meta(meta)

    def __init__(self, cursor: jdbc_api.Cursor, prepare_sql_statement: str = None):
        """
        Create Result Description from already executed query in cursor,
        or using prepare statement with fresh cursor to fetch metadata only without query executing
        :param cursor: Database cursor
        :param prepare_sql_statement: pass query if metadata without query execution is needed
        """
        if prepare_sql_statement is None:
            self.fields_description = JDBCResultDescription._get_result_meta_by_cursor_meta(cursor._meta)
        else:
            self.fields_description = \
                JDBCResultDescription._get_result_meta_by_prepare_statement(cursor, prepare_sql_statement)
        self.cursor = cursor
        self.connection = cursor._connection
        self.db_meta = self.connection.jconn.getMetaData()


DB_API_Description = namedtuple(
    'DB_API_Description',
    ['name', 'type_code', 'display_size', 'internal_size', 'precision', 'scale', 'null_ok'])

JARS = [
    "/home/mateusz/Dev/Db/drivers/teradata/terajdbc4.jar",
    "/home/mateusz/Dev/Db/drivers/teradata/tdgssconfig.jar",
    "/home/mateusz/Dev/Db/drivers/postgresql/postgresql-42.2.19.jar"
]

# con = jdbc_api.connect("org.postgresql.Driver",
#                  "jdbc:postgresql://localhost:5432/postgres",
#                  ["admin", "admin"],
#                  "/home/mateusz/Dev/Db/drivers/postgresql/postgresql-42.2.19.jar")

a = 1
#
#
# postgres_con = jdbc_api.connect("org.postgresql.Driver",
#                                 "jdbc:postgresql://localhost:5432/postgres",
#                                 ["admin", "admin"],
#                                 JARS)
#
# teradata_con = jdbc_api.connect("com.teradata.jdbc.TeraDriver",
#                                 "jdbc:teradata://192.168.1.4",
#                                 ["dbadmin", "dbadmin"],
#                                 JARS)
#
# postgres_cur = postgres_con.cursor()
# postgres_cur.execute("select t.*, t.varchar10 as varchar_alias from test1 t")
# m = postgres_cur._meta
#
#
#
#
#
#
# a = 1
# jaydebeai.DBAPITypeObject

# col_desc = (m.getColumnName(col),
#             dbapi_type,
#             size,
#             size,
#             m.getPrecision(col),
#             m.getScale(col),
#             m.isNullable(col),
#             )


# com.ncr.teradata.TeraDriver
# jdbc:teradata://{host}/DATABASE={database},DBS_PORT={port}
# com.teradata.jdbc.TeraDriver
# 1025
# teradata_con = jdbc_api.connect("com.teradata.jdbc.TeraDriver",
#                                 "jdbc:teradata://192.168.1.4",
#                                 ["dbadmin", "dbadmin"],
#                                 JARS)
# a = 1
# jdbc_api.connect("org.postgresql.Drivere",
#                  "jdbc:postgresql://localhost:5432/postgres",
#                  ["admin", "admin"],
#                  "/home/mateusz/Dev/Db/drivers/postgresql/postgresql-42.2.19.jar")
#
# try:
#     jdbc_api.connect("org.postgresql.Drivere",
#                      "jdbc:postgresql://localhost:5432/postgres",
#                      ["admin", "admin"],
#                      "/home/mateusz/Dev/Db/drivers/postgresql/postgresql-42.2.19.jar")
# except Exception as ex:
#     print(f'type is:{ex.__class__.__name__}')
#     print_exc()
#     a = 1