from collections import namedtuple
from enum import Enum
from typing import Iterable

import sqlparse

"""
Parse sql statement and tag certain parts of statement.
Tags are used in text sqleditor syntax highlighting.
"""


class TokenHighlightTypeTag(Enum):
    KEYWORD = 'KEYWORD'
    STRING_LITERAL = 'STRING_LITERAL'
    TEXT = 'TEXT'
    NUMBER = 'NUMBER'
    COMMENT = 'COMMENT'
    FUNCTION = 'FUNCTION'


TokenHighlightTagNamedTuple = namedtuple('TokenHighlightTag', 'tag token start_pos end_pos')


class TokenHighlightTag(TokenHighlightTagNamedTuple):
    def __repr__(self):
        return f'<{self.tag}>: "{str(self.token)}" ({self.start_pos}, {self.end_pos})'


def _extract_sql_syntax_highlighting_recursive_idx(tokens, idx: int) -> Iterable[TokenHighlightTag]:
    """
    Returns tagged tokens with tag related to syntax highlighting.
    Every tag is returned with its position (start, end) in parsed query string.
    :param tokens:
    :return: Tuples (tag, token)
    """
    # Type error
    try:
        current_len = 0
        for token in tokens:
            token_len = len(str(token))
            start_pos = idx + current_len
            end_pos = idx + current_len + token_len
            # Keywords
            if token.ttype in sqlparse.tokens.Keyword:
                yield TokenHighlightTag(TokenHighlightTypeTag.KEYWORD, token, start_pos, end_pos)
            # Numbers
            elif hasattr(token.ttype, 'parent') and token.ttype.parent is sqlparse.tokens.Literal.Number:
                yield TokenHighlightTag(TokenHighlightTypeTag.NUMBER, token, start_pos, end_pos)
            # Single quotes strings
            elif token.ttype is sqlparse.tokens.Literal.String.Single:
                yield TokenHighlightTag(TokenHighlightTypeTag.STRING_LITERAL, token, start_pos, end_pos)
            # Comment
            elif hasattr(token.ttype, 'parent') and token.ttype.parent is sqlparse.tokens.Comment:
                yield TokenHighlightTag(TokenHighlightTypeTag.COMMENT, token, start_pos, end_pos)
            # Function
            elif isinstance(token, sqlparse.sql.Function):
                func_current_len = len(str(token.tokens[0]))
                # return function Identifier token
                yield TokenHighlightTag(
                    TokenHighlightTypeTag.FUNCTION, token.tokens[0], start_pos, start_pos + func_current_len)
                # and analyze function params with parenthesis
                yield from _extract_sql_syntax_highlighting_recursive_idx(token.tokens[1:],
                                                                          start_pos + func_current_len)
            # No children, return token as plain text, end recursion
            elif not hasattr(token, 'tokens'):
                yield TokenHighlightTag(TokenHighlightTypeTag.TEXT, token, start_pos, end_pos)
            # Recursive search of children kens
            else:
                yield from _extract_sql_syntax_highlighting_recursive_idx(token.tokens, idx + current_len)
            current_len += token_len
    except TypeError:
        # handling situation when tokens is not Iterable (it is a leaf) - do nothing
        pass


def extract_sql_syntax_highlighting(tokens) -> Iterable[TokenHighlightTag]:
    yield from _extract_sql_syntax_highlighting_recursive_idx(tokens, 0)
