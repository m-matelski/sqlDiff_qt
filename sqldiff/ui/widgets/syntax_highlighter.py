import re
from collections import namedtuple
from enum import Enum
from typing import List

import sqlparse
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QSyntaxHighlighter, QColor, QTextCharFormat, QFont, QTextCursor

from sqldiff.sql.functions import ANSI_FUNCTIONS
from sqldiff.sql.keywords import SQL_2016_STANDARD_KEYWORDS

SyntaxHighlighter = QSyntaxHighlighter


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


text_format = QTextCharFormat()

keyword_format = QTextCharFormat()
keyword_format.setForeground(QColor(0, 102, 204))
keyword_format.setFontWeight(QFont.Bold)

string_literal_format = QTextCharFormat()
string_literal_format.setForeground(QColor(85, 170, 51))

number_format = QTextCharFormat()
number_format.setForeground(QColor(0, 179, 179))

comment_format = QTextCharFormat()
comment_format.setForeground(QColor(170, 170, 170))
comment_format.setFontItalic(True)

function_format = QTextCharFormat()
function_format.setForeground(QColor(184, 92, 46))

tag_format = {
    TokenHighlightTypeTag.KEYWORD: keyword_format,
    TokenHighlightTypeTag.STRING_LITERAL: string_literal_format,
    TokenHighlightTypeTag.TEXT: text_format,
    TokenHighlightTypeTag.NUMBER: number_format,
    TokenHighlightTypeTag.COMMENT: comment_format,
    TokenHighlightTypeTag.FUNCTION: function_format,
}


def extract_sql_syntax_highlighting_recursive_idx(tokens, idx):
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
            if token.ttype is sqlparse.tokens.Keyword or token.ttype is sqlparse.tokens.DML:
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
                yield from extract_sql_syntax_highlighting_recursive_idx(token.tokens[1:], start_pos + func_current_len)
            # No children, return token as plain text, end recursion
            elif not hasattr(token, 'tokens'):
                yield TokenHighlightTag(TokenHighlightTypeTag.TEXT, token, start_pos, end_pos)
            # Recursive search of children kens
            else:
                yield from extract_sql_syntax_highlighting_recursive_idx(token.tokens, idx + current_len)
            current_len += token_len
    except TypeError:
        # handling situation when tokens is not Iterable (it is a leaf) - do nothing
        pass


def extract_sql_syntax_highlighting(tokens):
    yield from extract_sql_syntax_highlighting_recursive_idx(tokens, 0)


class GenericSqlParserHighlighter(SyntaxHighlighter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # default formatting
        self.keyword_format = keyword_format
        self.function_format = function_format
        self.string_literal_format = string_literal_format
        self.number_format = number_format
        self.comment_format = comment_format
        self.function_format = function_format

    def highlightBlock(self, text: str):
        parsed = sqlparse.parse(text)
        syntax_highlight = extract_sql_syntax_highlighting(parsed)
        for tag in syntax_highlight:
            self.setFormat(tag.start_pos, tag.end_pos - tag.start_pos, tag_format[tag.tag])


class HighlightingRule:
    def __init__(self, pattern, pattern_format):
        self.pattern = pattern
        self.pattern_format = pattern_format


class GenericKeywordSqlHighlighter(SyntaxHighlighter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # default formatting
        self.keyword_format = keyword_format
        self.function_format = function_format
        self.string_literal_format = string_literal_format
        self.number_format = number_format
        self.comment_format = comment_format
        self.function_format = function_format
        #
        self.highlighting_rules = []

        for keyword in SQL_2016_STANDARD_KEYWORDS:
            keyword_regexp = f'\\b{re.escape(keyword)}\\b'
            pattern = re.compile(keyword_regexp, re.IGNORECASE)
            self.highlighting_rules.append(HighlightingRule(pattern, self.keyword_format))

        for func in ANSI_FUNCTIONS:
            pattern = re.compile(re.escape(func), re.IGNORECASE)
            self.highlighting_rules.append(HighlightingRule(pattern, self.function_format))

        string_literal_pattern = re.compile("\'.*\'")
        self.highlighting_rules.append(HighlightingRule(string_literal_pattern, self.string_literal_format))

        single_comment_pattern = re.compile("--[^\n]*")
        self.highlighting_rules.append(HighlightingRule(single_comment_pattern, self.comment_format))

        self.comment_start_pattern = re.compile("/\\*")
        self.comment_end_pattern = re.compile("\\*/")

    def highlightBlock(self, text):
        # for rule in self.highlighting_rules:
        #     match_iterator = rule.pattern.globalMatch(text)
        #     while match_iterator.hasNext():
        #         match = match_iterator.next()
        #         print(f'match: start {match.capturedStart()} length {match.capturedLength()}')
        #         self.setFormat(match.capturedStart(), match.capturedLength(), rule.pattern_format)

        # pythonic way
        for rule in self.highlighting_rules:
            for match in re.finditer(rule.pattern, text):
                self.setFormat(match.start(), match.end() - match.start(), rule.pattern_format)


class GenericSqlHighlighter(SyntaxHighlighter):
    class BlockCommentState:
        COMMENT = 1
        NOT_COMMENT = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # default formatting
        self.keyword_format = keyword_format
        self.function_format = function_format
        self.string_literal_format = string_literal_format
        self.number_format = number_format
        self.comment_format = comment_format
        self.function_format = function_format
        #
        self.highlighting_rules = []

        for keyword in SQL_2016_STANDARD_KEYWORDS:
            keyword_regexp = f'\\b{re.escape(keyword)}\\b'
            pattern = re.compile(keyword_regexp, re.IGNORECASE)
            self.highlighting_rules.append(HighlightingRule(pattern, self.keyword_format))

        # for func in ANSI_FUNCTIONS:
        #     pattern = re.compile(re.escape(func), re.IGNORECASE)
        #     self.highlighting_rules.append(HighlightingRule(pattern, self.function_format))
        #
        # string_literal_pattern = re.compile("\'.*\'")
        # self.highlighting_rules.append(HighlightingRule(string_literal_pattern, self.string_literal_format))
        #
        # single_comment_pattern = re.compile("--[^\n]*")
        # self.highlighting_rules.append(HighlightingRule(single_comment_pattern, self.comment_format))

        self.comment_start_pattern = re.compile(re.escape("/*"))
        # self.comment_end_pattern = re.compile(re.escape("*/"))
        self.comment_end_pattern = re.compile("\\*/")

    def highlight_keywords(self, text):
        for rule in self.highlighting_rules:
            for match in re.finditer(rule.pattern, text):
                self.setFormat(match.start(), match.end() - match.start(), rule.pattern_format)

    def highlight_parsed_items(self, text):
        parsed = sqlparse.parse(text)
        syntax_highlight = (t for t in extract_sql_syntax_highlighting(parsed)
                            if t.tag not in (TokenHighlightTypeTag.TEXT,))
        for tag in syntax_highlight:
            self.setFormat(tag.start_pos, tag.end_pos - tag.start_pos, tag_format[tag.tag])

    def highlight_block_comment(self, text):
        # https://doc.qt.io/qt-5/qtwidgets-richtext-syntaxhighlighter-example.html
        self.setCurrentBlockState(self.BlockCommentState.NOT_COMMENT)
        start_index = 0
        if self.previousBlockState() != self.BlockCommentState.COMMENT:
            match = re.search(self.comment_start_pattern, text)
            start_index = match.start() if match else -1
        while start_index >= 0:
            match = self.comment_end_pattern.search(text, start_index)
            end_index = match.start() if match else -1
            captured_length = match.end() - match.start() if match else 0
            if end_index == -1:
                self.setCurrentBlockState(self.BlockCommentState.COMMENT)
                comment_length = len(text) - start_index
            else:
                comment_length = end_index - start_index + captured_length
            self.setFormat(start_index, comment_length, self.comment_format)
            match = re.search(self.comment_start_pattern, text[start_index + comment_length:])
            start_index = match.start() if match else -1

    def highlightBlock(self, text):
        self.highlight_keywords(text)
        self.highlight_parsed_items(text)
        self.highlight_block_comment(text)
