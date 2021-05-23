import os
import unittest
from timeit import timeit

from sqldiff.sql.parse.compound import _split_no_strip, _get_queries_positions, get_queries_positions_strip, \
    get_queries_to_highlight, _get_query_at_index_full_search, _get_query_at_index_expand_search, get_query_at_index
from sqldiff.sql.parse.utils import find_nth_new_line, extend_string_range_by_line_numbers, find_nth_substring

TEST_DATA_FILEPATH = os.path.join(os.path.dirname(__file__), 'test_queries/multiple_generic.sql')
TEST_DATA_BIG_FILEPATH = os.path.join(os.path.dirname(__file__), 'test_queries/multiple_generic_big.sql')
test_sql_file = open(TEST_DATA_FILEPATH).read()
test_sql_file_big = open(TEST_DATA_BIG_FILEPATH).read()


class TestCompoundSqlParsers(unittest.TestCase):
    """
    Test compounds parsers functions
    """

    def test_split_no_strip(self):
        """Test splitting multiple sql statements without stripping comments and whitespaces."""
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


class TestGetQueryAtIndexParser(unittest.TestCase):
    """
    Test get query at index function.
    """

    def test_get_query_at_index_full_search(self):
        """Test if query at cursor position is properly found using full parse search function"""

        # timeit
        exec_time = timeit('_get_query_at_index_full_search(test_sql_file_big, 104585)', number=1, globals=globals())
        print(f"'_get_query_at_index_full_search' execution time: {exec_time}")

        query_at_index = _get_query_at_index_full_search(test_sql_file_big, 104585)
        expected_query = "\n\n\n\nselect 1 from oneliner_query;"
        expected_range = range(104578, 104611)
        self.assertEqual(query_at_index, (expected_query, expected_range))

    def test_get_query_at_index_expand_search_small_set(self):
        """Test if query at cursor position is properly found using expanding query range function."""
        query_at_index = _get_query_at_index_expand_search(test_sql_file, 468, range(468 - 10, 468 + 10))
        expected_query = \
            "\n\n\n\n" \
            "insert into employee values(2005, \'James\', \'Madison\', \'M\', \'Sodtware developer\', 1, 55000);"
        expected_range = range(463, 558)
        self.assertEqual(query_at_index, (expected_query, expected_range))

    def test_get_query_at_index_expand_search(self):
        """
        Test if query at cursor position is properly found using expanding query range function.
        Test on a large dataset.
        """

        # timeit
        exec_time = timeit(
            '_get_query_at_index_expand_search(test_sql_file_big, 104585, range(104585-100, 104585+100))', number=1,
            globals=globals())
        print(f"'_get_query_at_index_expand_search' execution time: {exec_time}")

        query_at_index = _get_query_at_index_expand_search(test_sql_file_big, 104585, range(104585 - 100, 104585 + 100))
        expected_query = "\n\n\n\nselect 1 from oneliner_query;"
        expected_range = range(104578, 104611)
        self.assertEqual(query_at_index, (expected_query, expected_range))

    def test_get_query_at_index(self):
        """Test public get_query_at_index function."""
        query_at_index = get_query_at_index(test_sql_file, 468)
        expected_query = \
            "insert into employee values(2005, \'James\', \'Madison\', \'M\', \'Sodtware developer\', 1, 55000);"
        expected_range = range(467, 558)
        self.assertEqual(query_at_index, (expected_query, expected_range))

    def test_get_query_at_index_when_there_is_no_query(self):
        """Test if query not found if index position is outside any query."""
        query_at_index = get_query_at_index(test_sql_file, 755)
        self.assertIsNone(query_at_index)

    def test_get_query_at_index_when_there_is_no_query_big_sql(self):
        """Test if query not found in big sql string. Measure and print execution time."""
        # timeit
        exec_time = timeit(
            'get_query_at_index(test_sql_file_big, 105730)', number=1,
            globals=globals())
        print(f"'get_query_at_index with big sql statement and no query under index' execution time: {exec_time}")

        query_at_index = get_query_at_index(test_sql_file_big, 105730)
        self.assertIsNone(query_at_index)

    def test_get_query_when_index_at_first(self):
        """Test if sql statement is found properly if index points first query in sql string."""
        query_at_index = get_query_at_index(test_sql_file, 30)
        expected_query = ("create table employee\n"
                          "(\n"
                          "	employee_id int primary key,\n"
                          "	first_name varchar(50),\n"
                          "	last_name varchar(100),\n"
                          "	gender varchar(1),\n"
                          "	position varchar(50),\n"
                          "	department_id int,\n"
                          "	salary numeric(9,2)\n"
                          ");")
        expected_range = range(25, 215)
        self.assertEqual(query_at_index, (expected_query, expected_range))

    def test_get_query_when_index_at_last(self):
        """Test if sql statement is found properly if index points last query in sql string."""
        query_at_index = get_query_at_index(test_sql_file, 1500)
        expected_query = ("select\n"
                          "ranked_salary.salary\n"
                          "from\n"
                          "(\n"
                          "	select\n"
                          "	e.salary,\n"
                          "	e.first_name,\n"
                          "	dense_rank() over (order by e.salary desc) as salary_rank\n"
                          "	from employee e\n"
                          ") ranked_salary\n"
                          "where ranked_salary.salary_rank = 2\n"
                          ";")
        expected_range = range(1306, 1504)
        self.assertEqual(query_at_index, (expected_query, expected_range))

    def test_get_query_at_index_edge_positions(self):
        """Test searching single query with edge case index positions."""
        comment_line = "\n-- query longer than 10 lines\n\n"
        sql = ("select\n"
               "ranked_salary.salary\n"
               "from\n"
               "(\n"
               "	select\n"
               "	e.salary,\n"
               "	e.first_name,\n"
               "	dense_rank() over (order by e.salary desc) as salary_rank\n"
               "	from employee e\n"
               ") ranked_salary\n"
               "where ranked_salary.salary_rank = 2\n"
               "and 1=1\n"
               "and 2=2\n"
               "and 3=3;")
        whitespaces_after_sql = "\n\n\n"

        test_sql = comment_line + sql + whitespaces_after_sql

        expected_query = sql

        query_at_index, query_range = get_query_at_index(test_sql, 33)
        self.assertEqual(query_at_index, expected_query)

        query_at_index, query_range = get_query_at_index(test_sql, 245)
        self.assertEqual(query_at_index, expected_query)

        query_range = get_query_at_index(test_sql, 0)
        self.assertIsNone(query_range)

        # out of range
        query_range = get_query_at_index(test_sql, 9999999)
        self.assertIsNone(query_range)

        query_range = get_query_at_index(test_sql, 255)
        self.assertIsNone(query_range)


class TestParserStringUtilFunctions(unittest.TestCase):

    def test_find_nth(self):
        test_string = "aa1aa1aa1aa1aa"
        self.assertEqual(find_nth_substring(test_string, '1', 2, 4), 8)
        self.assertEqual(find_nth_substring(test_string, '1', 2), 5)
        self.assertIsNone(find_nth_substring(test_string, '1', 5))

    def test_find_nth_new_line(self):
        test_string = 'aa\naa\naa\naa\naa'
        self.assertEqual(find_nth_new_line(test_string, 2, 7), 11)
        self.assertEqual(find_nth_new_line(test_string, 2), 5)
        self.assertEqual(find_nth_new_line(test_string, 2, 7, backwards=True), 2)
        self.assertIsNone(find_nth_new_line(test_string, 2, 120))
        self.assertIsNone(find_nth_new_line(test_string, 3, 7, backwards=True))

    def test_extend_string_range_by_line_numbers(self):
        test_string = 'aa\naa\nmiddle\naa\naa'
        r1 = extend_string_range_by_line_numbers(test_string, range(8, 9), 1)
        r2 = extend_string_range_by_line_numbers(test_string, range(8, 9), 2)
        r3 = extend_string_range_by_line_numbers(test_string, range(8, 9), 20)
        r4 = extend_string_range_by_line_numbers(test_string, range(9, 8), 2)
        self.assertEqual(test_string[r1.start:r1.stop], '\nmiddle')
        self.assertEqual(test_string[r2.start:r2.stop], '\naa\nmiddle\naa')
        self.assertEqual(test_string[r3.start:r3.stop], test_string)
        self.assertEqual(test_string[r4.start:r4.stop], '\naa\nmiddle\naa')
