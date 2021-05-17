import collections.abc
import itertools
from bisect import bisect
from itertools import accumulate
from typing import Tuple, List, Optional, Generator, Iterator, Union, Iterable

import sqlparse
import operator

from sqlparse import engine


class SingleSqlParserException(Exception):
    pass


class NotASingleSqlException(SingleSqlParserException):
    """Exception is raised when string with more than 1 query is passed, when expected is only 1 query."""
    pass


class SingleSqlParser:
    def __init__(self, sql: Union[str, sqlparse.sql.TokenList, Iterable[sqlparse.sql.Token]]):
        try:
            list_sql = [str(s) for s in sql]
            sql_str = ''.join(list_sql)
        except TypeError as e:
            sql_str = str(sql)

        self.sql = sql_str
        parsed = sqlparse.parse(self.sql)
        if len(parsed) > 1:
            raise NotASingleSqlException(f"Provided sql has more than one statement:\n{self.sql}")
        self.parsed = parsed[0]

    def __eq__(self, other):
        return self.sql == other.sql

    def split_comments_and_whitespaces_above_from_query(self):
        for i, token in enumerate(self.parsed):
            if not (isinstance(token, sqlparse.sql.Comment) or token.ttype in sqlparse.tokens.Whitespace):
                break

        comments_above = self.parsed[:i]
        query = self.parsed[i:]
        return comments_above, query

    def _get_comments_and_whitespaces_before_sql(self) -> Iterable[sqlparse.sql.Token]:
        """
        :return: Iterable generator of comment/whitespaces tokens present before query
        """
        comments_above, _ = self.split_comments_and_whitespaces_above_from_query()
        return comments_above

    @staticmethod
    def _find_first_comment_in_token_list(tokens: Iterable[sqlparse.sql.Token]) -> Optional[sqlparse.sql.Comment]:
        for token in tokens:
            if isinstance(token, sqlparse.sql.Comment):
                return token
        return None

    def replace_comments_above_query_with_spaces(self, lines_above_query: int = 0) -> str:
        """
        Replaces comments before sql statement with whitespaces if comment is "N" lines above.
        Number of characters in statement remains the same but only comments that met condition of
        lines_above_query will be remained as comments in statement.
        :param lines_above_query: if == 1 it'll remain sql comment directly above sql statement.
            If 0, no comments included.
        :return:
        """
        comments_above, query = self.split_comments_and_whitespaces_above_from_query()
        query_comments_gen = reversed([i for i in itertools.chain(*(token.flatten() for token in comments_above))])

        comments_to_keep = []
        new_lines = 0
        for token in query_comments_gen:
            comments_to_keep.insert(0, token)
            if new_lines >= lines_above_query:
                break
            if token.ttype is sqlparse.tokens.Newline:
                new_lines += 1

        comments_to_whitespace = list(reversed(list(query_comments_gen)))

        query_out = ''
        for i in comments_to_whitespace:
            query_out += ' ' * len(str(i))

        for i in itertools.chain(comments_to_keep, query):
            query_out += str(i)

        return query_out


class MultiSqlParser:
    def __init__(self, sql: str):
        self.sql = sql
        self.parsed = sqlparse.parse(sql)

    @staticmethod
    def _split_no_strip(sql: str, encoding=None):
        """
        sqlparse library implementation without strip

        Split *sql* into single statements.
        :param sql: A string containing one or more SQL statements.
        :param encoding: The encoding of the statement (optional).
        :returns: A list of strings.
        """
        stack = engine.FilterStack()
        return (str(stmt) for stmt in stack.run(sql, encoding))
        # return [str(stmt) for stmt in stack.run(sql, encoding)]

    @staticmethod
    def _get_query_at_position(sql: str, pos: int) -> Optional[str]:
        len_accu = 0
        for query in MultiSqlParser._split_no_strip(sql):
            query_len = len(str(query))
            if len_accu <= pos <= query_len + len_accu:
                return query
            len_accu += query_len
        return None

    # TODO: consider moving it to static functions, dont parse if text didnt change (??? where to control it ?? )
    def get_queries_positions(self, lines_above_query: int = 1) -> List[Tuple[range, str]]:
        """
        Find all sql statements in provided sql. Return queries and their positions in sql.
        :return: List of Tuples of position range and queries.
        """
        queries_positions = []
        sql_split = list(self._split_no_strip(self.sql))
        sql_split_clear_comments = \
            [SingleSqlParser(i).replace_comments_above_query_with_spaces(lines_above_query) for i in sql_split]

        sql_split_len = [len(i) for i in sql_split]
        sql_length_accu_list = [0] + list(accumulate(sql_split_len, operator.add))

        for i, sql in enumerate(sql_split_clear_comments):
            sql_len = len(sql)
            sql_lstrip_len = len(sql.lstrip())
            sql_rstrip_len = len(sql.rstrip())
            r_start = sql_length_accu_list[i] + (sql_len - sql_lstrip_len)
            r_stop = sql_length_accu_list[i + 1] - (sql_len - sql_rstrip_len)
            range_query = (range(r_start, r_stop), self.sql[r_start:r_stop])
            # append only valid queries
            if self.parsed[i].get_type() != 'UNKNOWN':
                queries_positions.append(range_query)

        return queries_positions

    def get_query_at_position(self, pos: int) -> str:
        """
        :param pos: position to check.
        :return: Returns query at position if exists. None otherwise.

        """
        queries_positions = self.get_queries_positions()
        for pos_range, query in queries_positions:
            if pos in pos_range:
                return query
        return None
