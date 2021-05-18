import os
import unittest
from timeit import timeit

from sqldiff.sql.parse.compound import _split_no_strip, _get_queries_positions, get_queries_positions_strip, \
    get_queries_to_highlight

TEST_DATA_FILEPATH = os.path.join(os.path.dirname(__file__), 'test_queries/multiple_generic.sql')
TEST_DATA_FILEPATH2 = os.path.join(os.path.dirname(__file__), 'test_queries/multiple_generic2.sql')
TEST_DATA_BIG_FILEPATH = os.path.join(os.path.dirname(__file__), 'test_queries/multiple_generic_big.sql')
test_sql_file = open(TEST_DATA_FILEPATH).read()
test_sql_file2 = open(TEST_DATA_FILEPATH2).read()
test_sql_file_big = open(TEST_DATA_BIG_FILEPATH).read()


class TestSubSqlParsers(unittest.TestCase):

    def test_split_no_strip(self):
        test_sql = '          SELECT 1;          SELECT 2;          SELECT 3;'
        split_sql = list(_split_no_strip(test_sql))
        self.assertEqual(split_sql[0], '          SELECT 1;          ')
        self.assertEqual(split_sql[1], 'SELECT 2;          ')
        self.assertEqual(split_sql[2], 'SELECT 3;')

    def test_get_queries_positions(self):
        """Test if queries positions are properly determined if there are whitespaces."""
        test_sql = '          SELECT 1;          SELECT 2;          SELECT 3;'
        queries_positions = list(_get_queries_positions(test_sql))
        self.assertEqual(queries_positions[0], ('          SELECT 1;          ', range(0, 29)))
        self.assertEqual(queries_positions[1], ('SELECT 2;          ', range(29, 48)))
        self.assertEqual(queries_positions[2], ('SELECT 3;', range(48, 57)))

    def test_get_queries_positions_strip(self):
        queries = list(get_queries_positions_strip(test_sql_file))

        a = 1

    def test_get_queries_to_highlight(self):
        queries = list(get_queries_to_highlight(test_sql_file, range(1100, 1310)))
        a = 1


    def test_get_queries_to_highlight(self):
        queries = list(get_queries_positions_strip(test_sql_file2))
        queries_to_highlight = list(get_queries_to_highlight(test_sql_file2, range(4100, 4310)))
        a = 1


    def test_timeit(self):
        queries = list(get_queries_to_highlight(test_sql_file_big, range(101100, 101310)))
        print(timeit('list(get_queries_to_highlight(test_sql_file, range(101100, 101310)))', number=1, globals=globals()))
