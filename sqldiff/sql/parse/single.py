from typing import Tuple, Optional

import sqlparse

from sqldiff.sql.parse.exceptions import SingleSqlStatementExpectedException, QueryRangeTuple


# def _chain_subs(subs):


def parse_single_sql(sql: str):
    parsed = sqlparse.parse(sql)
    if len(parsed) != 1:
        raise SingleSqlStatementExpectedException(f"Expected 1 SQL statement. Got {len(parsed)} instead.")
    return parsed[0]


def _sub_identity(sql: str, r: Optional[range] = None) -> QueryRangeTuple:
    sql_range = r or range(0, len(str(sql)))
    return sql, sql_range


def _sub_strip(sql: str, r: Optional[range] = None) -> QueryRangeTuple:
    sql_range = r or range(0, len(str(sql)))
    query_str = str(sql)
    query_len = len(query_str)
    s_start = query_len - len(query_str.lstrip())
    s_stop = len(query_str.rstrip())
    r_start = sql_range.start + s_start
    r_stop = sql_range.stop - (query_len - s_stop)
    return sql[s_start:s_stop], range(r_start, r_stop)


def _sub_strip_comments_before_statement(sql: str, r: Optional[range] = None) -> QueryRangeTuple:
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
    return sql[s_start:s_stop], range(r_start, r_stop)


def _sub_strip_whitespaces_and_comments(sql: str, r: Optional[range] = None) -> QueryRangeTuple:
    return _sub_strip_comments_before_statement(*_sub_strip(sql, r))
