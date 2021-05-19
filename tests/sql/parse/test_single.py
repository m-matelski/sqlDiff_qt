import os
import unittest

import sqlparse

from sqldiff.sql.parse.single import _sub_strip, \
    _sub_strip_comments_before_statement
from sqldiff.ui.widgets.editor.syntax_highlighter import extract_sql_syntax_highlighting_recursive_idx

TEST_DATA_FILEPATH = os.path.join(os.path.dirname(__file__), 'test_queries/multiple_generic.sql')
TEST_DATA_BIG_FILEPATH = os.path.join(os.path.dirname(__file__), 'test_queries/multiple_generic_big.sql')
test_sql_file = open(TEST_DATA_FILEPATH).read()
test_sql_file_big = open(TEST_DATA_BIG_FILEPATH).read()


class TestSubSqlParsers(unittest.TestCase):

    def test_sub_strip(self):
        test_sql = "   \n   SELECT 1 FROM TABLE1   \n   "
        expected_sql = "SELECT 1 FROM TABLE1"
        sub_query, sub_range = _sub_strip(test_sql)

        self.assertEqual(sub_query, expected_sql)
        self.assertEqual(sub_range, range(7, 27))

    def test_sub_strip_with_range(self):
        test_sql = "   \n   SELECT 1 FROM TABLE1   \n   "
        expected_sql = "SELECT 1 FROM TABLE1"
        # Adding 100 comparing to previus test - pretending that sub is performing in range context
        sub_query, sub_range = _sub_strip(test_sql, range(100, 134))

        self.assertEqual(sub_query, expected_sql)
        self.assertEqual(sub_range, range(107, 127))

    def test_sub_strip_leading_comments(self):
        test_sql = ("\n"
                    "\n"
                    "-- comment1\n"
                    "-- comment2\n"
                    "\n"
                    "\n"
                    "/********\n"
                    "  some block comment\n"
                    " */\n"
                    "\n"
                    "select\n"
                    "max(e_max.salary) as highest_salary\n"
                    "from employee e_max  \n--where 1=1\n"
                    "  \n ")

        expected_sql = ("select\n"
                        "max(e_max.salary) as highest_salary\n"
                        "from employee e_max  \n--where 1=1\n"
                        "  \n ")

        sub_query, sub_range = _sub_strip_comments_before_statement(test_sql)

        self.assertEqual(sub_query, expected_sql)
        self.assertEqual(sub_range, range(64, 145))


    def test_sub_strip_leading_comments_and_whitespaces(self):
        test_sql = ("\n"
                    "\n"
                    "-- comment1\n"
                    "-- comment2\n"
                    "\n"
                    "\n"
                    "/********\n"
                    "  some block comment\n"
                    " */\n"
                    "\n"
                    "select\n"
                    "max(e_max.salary) as highest_salary\n"
                    "from employee e_max  \n--where 1=1\n"
                    "  \n ")

        expected_sql = ("select\n"
                        "max(e_max.salary) as highest_salary\n"
                        "from employee e_max  \n--where 1=1")

        # composing multiple subs
        sub_query, sub_range = _sub_strip_comments_before_statement(*_sub_strip(test_sql))

        self.assertEqual(sub_query, expected_sql)
        self.assertEqual(sub_range, range(64, 140))



    # TODO move tests to other file?
    def test_syntax_highlighter_extractor(self):
        test_sql = (" \n  select\n"
                    "d.department_name,\n"
                    "max(e.salary) highest_salary,\n"
                    "round(12) highest_salary,\n"
                    "from employee e\n"
                    "left join department d\n"
                    "on e.department_id = d.department_id\n"
                    "group by d.department_name;  \n  ")
        parsed = sqlparse.parse(test_sql)
        tags = list(extract_sql_syntax_highlighting_recursive_idx(parsed, 0))

        # check all positions
        for tag in tags:
            token_str = str(tag.token)
            query_part_at_pos = test_sql[tag.start_pos:tag.end_pos]
            self.assertEqual(token_str, query_part_at_pos)

    def test_syntax_highlighter_extractor_ddl(self):
        test_sql = ("create table employee\n"
                    "(\n"
                    "	employee_id int primary key,\n"
                    "	first_name varchar(50),\n"
                    "	last_name varchar(100),\n"
                    "	gender varchar(1),\n"
                    "	position varchar(50),\n"
                    "	department_id int,\n"
                    "	salary numeric(9,2)	\n"
                    ");")

        parsed = sqlparse.parse(test_sql)
        tags = list(extract_sql_syntax_highlighting_recursive_idx(parsed, 0))

        # check all positions
        for tag in tags:
            token_str = str(tag.token)
            query_part_at_pos = test_sql[tag.start_pos:tag.end_pos]
            self.assertEqual(token_str, query_part_at_pos)




