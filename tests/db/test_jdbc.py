import unittest

import jaydebeapi as jdbc_api

from sqldiff.db.jdbc import JDBCResultDescription


class TestJDBCResult(unittest.TestCase):

    def setUp(self):
        """DB connection used in tests"""
        # TODO use JDBC mock, it's more about API than data
        pass
        self.con = jdbc_api.connect("org.postgresql.Driver",
                                    "jdbc:postgresql://localhost:5432/postgres",
                                    ["admin", "admin"],
                                    "/home/mateusz/Dev/Db/drivers/postgresql/postgresql-42.2.19.jar")

    def tearDown(self) -> None:
        pass
        # self.con.close()

    def test_create_jdbc_result_description_by_query_result(self):
        """Test fetching metadata from executed query, using cursor"""
        query = "select * from test1"
        cur = self.con.cursor()
        cur.execute(query)
        result_description = JDBCResultDescription(cur)
        desc = cur.description
        a = 1

    def test_create_jdbc_result_description_by_prepare_statement(self):
        """Test fetching metadata without query execution"""
        query = "select * from test1"
        cur = self.con.cursor()
        result_description = JDBCResultDescription(cur, query)
        a = 1

    def test_con(self):
        query = "select * from test1"
        cur = self.con.cursor()
        jconn = cur._connection.jconn
        db_meta = jconn.getMetaData()
        d = {
            'product_name': db_meta.getDatabaseProductName(),
            'product_version': db_meta.getDatabaseProductVersion(),
            'driver_name': db_meta.getDriverName(),
            'driver_version': db_meta.getDriverVersion(),
        }
        a = 1


class TestDriverErrors(unittest.TestCase):
    def test_wrong_class_name(self):
        try:
            jdbc_api.connect("org.postgresql.Drivere",
                             "jdbc:postgresql://localhost:5432/postgres",
                             ["admin", "admin"],
                             "/home/mateusz/Dev/Db/drivers/postgresql/postgresql-42.2.19.jar")
        except Exception as ex:
            a = 1

    def test_wrong_url(self):
        try:
            jdbc_api.connect("org.postgresql.Driver",
                             "jdbc:postgresql://localhost_bad:5432/postgres",
                             ["admin", "admin"],
                             "/home/mateusz/Dev/Db/drivers/postgresql/postgresql-42.2.19.jar")
        except Exception as ex:
            a = 1

    def test_wrong_patameters(self):
        try:
            jdbc_api.connect("org.postgresql.Driver",
                             "jdbc:postgresql://localhost:5432/postgres",
                             ["admin2", "admin2"],
                             "/home/mateusz/Dev/Db/drivers/postgresql/postgresql-42.2.19.jar")
        except Exception as ex:
            a = 1

    def test_wrong_jdbc_path(self):
        try:
            jdbc_api.connect("org.postgresql.Driver",
                             "jdbc:postgresql://localhost_bad:5432/postgres",
                             ["admin", "admin"],
                             "/home/mateusz/Dev/Db/drivers/postgresqlee/postgresql-42.2.19.jar")
        except Exception as ex:
            print(ex)
            a = 1





