import os
import unittest
from timeit import timeit

import sqlparse

from sqldiff.sql.parse import MultiSqlParser, SingleSqlParser
from sqldiff.ui.widgets.syntax_highlighter import extract_sql_syntax_highlighting_recursive_idx, \
    extract_sql_syntax_highlighting

TEST_DATA_FILEPATH = os.path.join(os.path.dirname(__file__), 'test_queries/multiple_generic.sql')
TEST_DATA_BIG_FILEPATH = os.path.join(os.path.dirname(__file__), 'test_queries/multiple_generic_big.sql')
test_sql_file = open(TEST_DATA_FILEPATH).read()
test_sql_file_big = open(TEST_DATA_BIG_FILEPATH).read()


class TestGetQueryAtPosition(unittest.TestCase):

    def test_get_queries_positions_no_comments(self):
        """Test if queries positions are properly determined if there are whitespaces."""
        test_sql = '          SELECT 1;          SELECT 2;          SELECT 3;'
        parsed = MultiSqlParser(test_sql)
        queries_positions = parsed.get_queries_positions()
        pos2 = list(MultiSqlParser._split_no_strip(test_sql))
        self.assertEqual(queries_positions[0], (range(10, 19), 'SELECT 1;'))
        self.assertEqual(queries_positions[1], (range(29, 38), 'SELECT 2;'))
        self.assertEqual(queries_positions[2], (range(48, 57), 'SELECT 3;'))

    def test_get_query_at_position_with_spaces(self):
        test_sql = '          SELECT 1;          SELECT 2;          SELECT 3;'

        parsed = MultiSqlParser(test_sql)
        self.assertEqual(parsed.get_query_at_position(-100), None)
        self.assertEqual(parsed.get_query_at_position(0), None)
        self.assertEqual(parsed.get_query_at_position(9), None)
        self.assertEqual(parsed.get_query_at_position(10), 'SELECT 1;')
        self.assertEqual(parsed.get_query_at_position(18), 'SELECT 1;')
        self.assertEqual(parsed.get_query_at_position(30), 'SELECT 2;')
        self.assertEqual(parsed.get_query_at_position(55), 'SELECT 3;')
        self.assertEqual(parsed.get_query_at_position(999999), None)


class TestSingleSqlParser(unittest.TestCase):

    def test_object_creation(self):
        """Test object creation"""
        test_sql = \
            "\n" \
            "-- comment 1 \n" \
            "\n" \
            "SELECT 1 FROM TABLE1;"
        ob1 = SingleSqlParser(test_sql)

        parsed_sql = sqlparse.parse(test_sql)[0]
        ob2 = SingleSqlParser(parsed_sql)

        token_list_sql_generator = (t for t in parsed_sql)
        ob3 = SingleSqlParser(token_list_sql_generator)

        self.assertEqual(ob1.sql, ob2.sql)
        self.assertEqual(ob3.sql, ob2.sql)
        self.assertTrue(ob1 == ob2 == ob3)

    def test_get_comments_before_sql(self):
        """Test if comments above query are returned properly"""
        sql_comments = \
            "\n" \
            "\n" \
            "-- comment 1 \n" \
            "\n" \
            "/**********\n" \
            "** some block \n" \
            "**************/\n" \
            "\n" \
            "-- comment \n" \
            "\n" \
            "\n"
        query = "SELECT 1;"
        test_sql = sql_comments + query

        parsed = SingleSqlParser(test_sql)

        self.assertEqual(''.join(str(s) for s in parsed._get_comments_and_whitespaces_before_sql()), sql_comments)

    def test_replace_comments_with_whitespaces_one_line(self):
        sql_comments = \
            "\n" \
            "-- comment to out   \n" \
            "   \n" \
            "\t   \n" \
            "-- in comment1\n" \
            "-- in comment2\n"

        query = "SELECT 1;"
        test_sql = sql_comments + query

        parsed = SingleSqlParser(test_sql)
        com = parsed.replace_comments_above_query_with_spaces(1)

        self.assertEqual(len(com), len(test_sql))

    def test_replace_comments_with_whitespaces_one_line_many_comments(self):
        sql_comments = \
            "\n" \
            "\n" \
            "-- comment 1 \n" \
            "\n" \
            "/**********\n" \
            "** some block \n" \
            "**************/\n" \
            "       \n " \
            "-- out comment\n" \
            "  \n  " \
            "-- in comment1\n" \
            "-- in comment2\n"

        query = "SELECT 1;"
        test_sql = sql_comments + query

        parsed = SingleSqlParser(test_sql)
        com = parsed.replace_comments_above_query_with_spaces(1)

        self.assertEqual(len(com), len(test_sql))

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

    def test_valid_query(self):
        # parsed = sqlparse.parse(test_sql_file_big)
        # parsed[0].
        # flat = parsed[
        # sqlparse.sql.TokenList
        # parsed_query = parsed[11]
        # parsed_query_flat = list(parsed_query.flatten())
        a = 1
        # MultiSqlParser.get_query_at_position(50)
        spl = list(MultiSqlParser._split_no_strip(test_sql_file))
        query = MultiSqlParser._get_query_at_position(test_sql_file, 293)
        a = 1
        # print(timeit('MultiSqlParser(test_sql_file_big).get_query_at_position(50000)', number=1, globals=globals()))
        # print(timeit('MultiSqlParser._get_query_at_position(test_sql_file_big, 50000)', number = 1, globals=globals()))

        spl = list(MultiSqlParser._split_no_strip(test_sql_file))
        query = MultiSqlParser._get_query_at_position(test_sql_file, 293)
        tags = list(extract_sql_syntax_highlighting(sqlparse.parse(test_sql_file_big)))
        print(timeit('sqlparse.parse(test_sql_file_big)', number=1, globals=globals()))
        print(timeit('MultiSqlParser._split_no_strip(test_sql_file_big)', number=1, globals=globals()))
        print(timeit('MultiSqlParser._get_query_at_position(test_sql_file_big, 29300)', number=1, globals=globals()))
        print(timeit('list(extract_sql_syntax_highlighting(sqlparse.parse(test_sql_file_big)))', number=1, globals=globals()))



        a = 1
