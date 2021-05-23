from typing import Optional

import sqlparse

from sqldiff.sql.parse.utils import SingleSqlStatementExpectedException, QueryRange

"""
This module provides functions for parsing sql statements.
It assumes that provided sql string contains only 1 sql statement.

Subs:
every function starting with _sub* is function processing single sql statement.
Second sub argument is sql range which provides information about start and end of provided sql string in parent
(for example when root sql string consist of many sql statements, 
or sql have been already processed by sub removing whitespaces.
It returns processed sql statement, and its position within provided sql.
Subs are used to setup additional processing for single or compound sql parsers.
"""


def parse_single_sql(sql: str):
    """
    Trying to parse sql statement.
    Raises SingleSqlStatementExpectedException when sql string contains more than 1 or 0 statements.
    :param sql: SQL string
    :return: parsed SQL
    """
    parsed = sqlparse.parse(sql)
    if len(parsed) != 1:
        raise SingleSqlStatementExpectedException(f"Expected 1 SQL statement. Got {len(parsed)} instead.")
    return parsed[0]


def _sub_identity(sql: str, r: Optional[range] = None) -> QueryRange:
    """
    Identity sub, returns input.
    :param sql: SQL string
    :param r: SQL range
    :return: returns input.
    """
    sql_range = r or range(0, len(str(sql)))
    return QueryRange(sql, sql_range)


def _sub_strip(sql: str, r: Optional[range] = None) -> QueryRange:
    """
    Stripping leading and trailing whitespaces from provided sql string.
    :param sql: SQL string
    :param r: Position of sql string in parent
    :return: Stripped SQL, and new start and end positions of new stripped sql string.
    """
    sql_range = r or range(0, len(str(sql)))
    query_str = str(sql)
    query_len = len(query_str)
    s_start = query_len - len(query_str.lstrip())
    s_stop = len(query_str.rstrip())
    r_start = sql_range.start + s_start
    r_stop = sql_range.stop - (query_len - s_stop)
    return QueryRange(sql[s_start:s_stop], range(r_start, r_stop))


def _sub_strip_comments_before_statement(sql: str, r: Optional[range] = None) -> QueryRange:
    """
    Stripping comments leading sql statement.
    :param sql: SQL string
    :param r: Position of sql string in parent
    :return: SQL string with stripped leading comments, and new start and end positions of new stripped sql string.
    """
    sql_range = r or range(0, len(str(sql)))
    parsed = parse_single_sql(sql)
    len_accu = 0
    for i, token in enumerate(parsed):
        if not (token.ttype in sqlparse.tokens.Whitespace or isinstance(token, sqlparse.sql.Comment)):
            break
        len_accu += len(str(token))
    s_start = len_accu
    s_stop = len(sql)
    r_start = sql_range.start + s_start
    r_stop = sql_range.stop
    return QueryRange(sql[s_start:s_stop], range(r_start, r_stop))


def _sub_strip_whitespaces_and_comments(sql: str, r: Optional[range] = None) -> QueryRange:
    """
    Combines subs. Strips leading and trailing whitespaces, strips leading sql comments.
    :param sql: SQL string.
    :param r: Position of sql string in parent.
    :return: SQL string with stripped whitespaces and comments.
    """
    return QueryRange(_sub_strip_comments_before_statement(*_sub_strip(sql, r)))
