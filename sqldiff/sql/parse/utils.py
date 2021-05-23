from typing import Callable, Optional, NamedTuple

"""
Util object used in sql parsing.
"""


class QueryRange(NamedTuple):
    query: str
    q_range: range


Sub = Callable[[str, Optional[range]], QueryRange]


class SqlParseException(Exception):
    pass


class SingleSqlStatementExpectedException(SqlParseException):
    pass


def ranges_overlap(r1: range, r2: range) -> bool:
    """
    Checks if provided ranges are overlapping
    :param r1: first range
    :param r2: second range
    :return: True if ranges overlap
    """
    return r1.start in r2 or r1.stop in r2 or r2.start in r1 or r2.stop in r1


def extend_range(r: range, extend_by) -> range:
    """
    Extends range by provided value on both sides.
    :param r: range
    :param extend_by: value to extend range at start and stop
    :return: extended range
    """
    r_start = max(r.start - extend_by, 0)
    r_stop = r.stop + extend_by
    return range(r_start, r_stop)


def find_nth_substring(string, substring, n, offset=0):
    """
    Finds nth substring occurrence in string, and returns it's position;
    :param string: string
    :param substring: substring to search
    :param n: number of occurrence to check
    :param offset: position from which to start to searching in parent string
    :return: position of nth substring occurrence in parent string, or None if not found
    """
    start = string.find(substring)
    while start >= 0 and n > 1:
        start = string.find(substring, start + len(substring) + offset)
        n -= 1
    if start == -1:
        return None
    return start


def find_nth_new_line(s: str, n, start_pos=0, backwards=False):
    """
    Finds nth new line character occurrence in parent string s.
    Can search forwards or backwards, starting from start_pos of parent string.
    :param s: parent string to search
    :param n: number of occurrence to check
    :param start_pos: position from which to start to searching in parent string
    :param backwards: Backwards flag. If True, searches for new line in backwards direction. Default False.
    :return: position of nth new line character occurrence in parent string, or None if not found
    """
    s_range = range(start_pos - 1, -1, -1) if backwards else range(start_pos, len(s), 1)
    for i in s_range:
        if s[i] == '\n':
            n -= 1
        if n <= 0:
            return i
    return None


def extend_string_range_by_line_numbers(s: str, r: range, n: int):
    """
    Extends "r" range positions in string "s" by "n" lines up and down.
    :param s: string
    :param r: input string start and stop range to start search next new lines characters
    :param n: how many newline characters needs to be found to extend range
    :return: string range positions extended by newline characters positions searched forwards and backwards.
    """
    r_start = find_nth_new_line(s, n, r.start, backwards=True) or 0
    r_stop = find_nth_new_line(s, n, r.stop, backwards=False) or len(s)
    return range(r_start, r_stop)
