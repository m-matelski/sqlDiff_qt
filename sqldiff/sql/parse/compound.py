from typing import Iterable, Optional

from sqlparse import engine

from sqldiff.sql.parse.utils import QueryRange, Sub, ranges_overlap, extend_range, \
    extend_string_range_by_line_numbers
from sqldiff.sql.parse.single import _sub_identity, _sub_strip_whitespaces_and_comments, \
    _sub_strip_comments_before_statement

"""
This module provides functions for parsing sql statements.
It assumes that provided sql string contains more than 1 sql statements.
"""


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


def _get_queries_positions(sql: str, sub: Sub = _sub_identity) -> Iterable[QueryRange]:
    """
    Extracts list of sql statements and their positions form provided sql
    :param sql: SQL statement
    :param sub: sub parse function - identity by default
    :return: Iterable of sql str and range position in provided sql
    """
    len_accu = 0
    for query in _split_no_strip(sql):
        query_len = len(str(query))
        yield sub(query, range(len_accu, len_accu + query_len))
        len_accu += query_len


def _get_queries_in_range(sql: str, range_index: range, sub: Sub = _sub_identity) -> Iterable[QueryRange]:
    """
    Returns all sql statements and their positions in provided range
    :param sql: SQL statement
    :param range_index: range index to search (similar to text selection in sqleditor)
    :param sub: sub parse function - identity by default
    :return: Iterable of sql str and range position in provided sql
    """
    for query, query_range in _get_queries_positions(sql):
        if ranges_overlap(query_range, range_index):
            yield sub(query, query_range)
    return None


def _get_query_at_index_full_search(sql: str, index: int, sub: Sub = _sub_identity) -> Optional[QueryRange]:
    """
    Returns query at index. Parses full sql statement (inefficient for big sql statements)
    :param sql: SQL statement
    :param index: index position in provided sql string
    :param sub: sub parse function - identity by default
    :return: Sql statement at cursor position or None
    """
    for query, query_range in _get_queries_positions(sql):
        if index in query_range:
            return sub(query, query_range)
    return None


def _get_query_at_index_expand_search(sql: str, index: int, r: range, sub: Sub = _sub_identity) \
        -> Optional[QueryRange]:
    """
    Returns query at index. Parse statement form cursor position and extend sql piece,
    until there are some valid queries before and after statement.
    :param sql: SQL statement
    :param index: index position in provided sql string
    :param r: range of sql to start search in
    :param sub: sub parse function - identity by default
    :return: Sql statement at cursor position or None
    """
    query_index_range_offset = 2
    sql_len = len(sql)
    lines_to_expand = 10
    current_range = extend_string_range_by_line_numbers(sql, r, lines_to_expand)
    while True:
        sql_ranged = sql[current_range.start:current_range.stop]
        queries_positions = list(_get_queries_positions(sql_ranged, sub))
        for i, (query, query_range) in enumerate(queries_positions):
            global_query_range = range(query_range.start + current_range.start, query_range.stop + current_range.start)
            if index in global_query_range:
                if (
                        query_index_range_offset <= i < (len(queries_positions) - query_index_range_offset) or
                        (current_range.start == 0 and i < (len(queries_positions) - query_index_range_offset)) or
                        (query_index_range_offset <= i and current_range.stop == sql_len) or
                        (current_range.start == 0 and current_range.stop == sql_len)
                ):
                    return QueryRange(query, global_query_range)
                else:
                    break
            if index < global_query_range.start:
                # No query after in position
                return None
        if current_range.start == 0 and current_range.stop == sql_len:
            break
        lines_to_expand *= 2
        current_range = extend_string_range_by_line_numbers(sql, current_range, lines_to_expand)
    return None


def get_queries_positions_strip(sql: str) -> Iterable[QueryRange]:
    """
    Generate list of queries positions.
    Remove leading and trailing comments and whitespaces from returned range position.
    :param sql:
    :return: List of sql statements and their positions in provided sql string.
    Removes Whitespaces and leading comments.
    """
    for query, query_range in _get_queries_positions(sql):
        yield _sub_strip_whitespaces_and_comments(query, query_range)


def get_queries_to_highlight(sql: str, range_index: range):
    """
    Generate list of queries positions within range.
    Remove leading and trailing comments and whitespaces from returned range position.
    :param sql: SQL statement
    :param range_index: range index to search (similar to text selection in sqleditor)
    :return: List of sql statements and their positions in provided sql string, within range.
    Removes Whitespaces and leading comments.
    """
    for query, query_range in _get_queries_in_range(sql, range_index):
        yield _sub_strip_whitespaces_and_comments(query, query_range)


def get_query_at_index(sql: str, index: int) -> Optional[QueryRange]:
    """
    Finds and returns single sql statement at index.
    :param sql: SQL string (may contain many SQL statements)
    :param index: Index (cursor position) to determine full sql statement.
    :return: Returns single SQL statement at index (position) with its start and end position as range.
    Returns none if no SQL statement available at string index (whitespaces or comments before statement).
    """
    if index not in range(0, len(sql)):
        return None
    r = range(index, index)
    query_range = _get_query_at_index_expand_search(sql, index, r, _sub_strip_comments_before_statement)
    if query_range:
        return QueryRange(*query_range)
    return None
