import unittest

import sqlparse

from sqldiff.sql.parse.highlighting import extract_sql_syntax_highlighting, TokenHighlightTag, TokenHighlightTypeTag


class TestSqlParseHighlightingTags(unittest.TestCase):

    def test_create_statement_keywords(self):
        test_sql = ("create table employee\n"
                    "(\n"
                    "	employee_id int primary key,\n"
                    "	first_name varchar(50)\n"
                    ");")

        parsed = sqlparse.parse(test_sql)
        highlighting_tags = list(extract_sql_syntax_highlighting(parsed))
        # convert to simple tuple with string instead of token, for easier assertion
        keyword_strings = [(tag, str(token), start_pos, end_pos)
                           for tag, token, start_pos, end_pos in highlighting_tags
                           if tag == TokenHighlightTypeTag.KEYWORD]

        self.assertTrue((TokenHighlightTypeTag.KEYWORD, 'create', 0, 6) in keyword_strings)
        self.assertTrue((TokenHighlightTypeTag.KEYWORD, 'table', 7, 12) in keyword_strings)
        self.assertTrue((TokenHighlightTypeTag.KEYWORD, 'primary', 41, 48) in keyword_strings)
        self.assertTrue((TokenHighlightTypeTag.KEYWORD, 'key', 49, 52) in keyword_strings)
