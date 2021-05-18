from typing import Iterable, Tuple, Optional

from sqlparse import engine

from sqldiff.sql.parse.exceptions import QueryRangeTuple, Sub
from sqldiff.sql.parse.single import _sub_identity, _sub_strip_whitespaces_and_comments


def ranges_overlap(r1: range, r2: range):
    return r1.start in r2 or r1.stop in r2 or r2.start in r1 or r2.stop in r1


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


def _get_queries_positions(sql: str, sub: Sub = _sub_identity) -> Iterable[QueryRangeTuple]:
    len_accu = 0
    for query in _split_no_strip(sql):
        query_len = len(str(query))
        yield sub(query, range(len_accu, len_accu + query_len))
        len_accu += query_len


def _get_queries_in_range(sql: str, range_index: range, sub: Sub = _sub_identity) -> Optional[QueryRangeTuple]:
    for query, query_range in _get_queries_positions(sql):
        if ranges_overlap(query_range, range_index):
            yield sub(query, query_range)
    return None


def _get_query_at_index(sql: str, index: int, sub: Sub = _sub_identity) -> Optional[QueryRangeTuple]:
    for query, query_range in _get_queries_positions(sql):
        if index in query_range:
            return sub(query, query_range)
    return None


def get_queries_positions_strip(sql: str) -> Iterable[QueryRangeTuple]:
    for query, query_range in _get_queries_positions(sql):
        yield _sub_strip_whitespaces_and_comments(query, query_range)


def get_queries_to_highlight(sql: str, range_index: range):
    for query, query_range in _get_queries_in_range(sql, range_index):
        yield _sub_strip_whitespaces_and_comments(query, query_range)
