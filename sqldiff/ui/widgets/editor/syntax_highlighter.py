import re

import sqlparse
from PyQt5.QtGui import QSyntaxHighlighter, QColor, QTextCharFormat, QFont

from sqldiff.sql.parse.highlighting import TokenHighlightTypeTag, extract_sql_syntax_highlighting

"""
Syntax highlighters for QPlainTextEdit components.

QSyntaxHighlighter class allows to overwrite highlightBlock method to handle formatting for changed text.
This method provides text parameter with only portion of text from text editor 
which have been changed and needs to define it's syntax highlighting.

"""

SyntaxHighlighter = QSyntaxHighlighter

# Default highlight formatting
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


class GenericSqlHighlighter(SyntaxHighlighter):
    """
    Syntax Highlighter for Qt TextEdit components to use.
    No specific SQL dialect.
    """

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

        self.comment_start_pattern = re.compile(re.escape("/*"))
        self.comment_end_pattern = re.compile(re.escape("*/"))

    def highlight_parsed_items(self, text):
        """
        Determine tagged sql tokens to highlight.
        Handles: keywords, functions, numbers, quoted strings, line comments.
        :param text: text changed
        """
        parsed = sqlparse.parse(text)
        syntax_highlight = (t for t in extract_sql_syntax_highlighting(parsed)
                            if t.tag not in (TokenHighlightTypeTag.TEXT,))
        for tag in syntax_highlight:
            self.setFormat(tag.start_pos, tag.end_pos - tag.start_pos, tag_format[tag.tag])

    def highlight_block_comment(self, text):
        """
        Finds and set highlighting for SQL block comment.
        Method goes out of provided changed text parameter and search for closing comment token in next text blocks.
        It's much faster than parsing whole text editor content for finding multiline comments.
        :param text: changed text
        """
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
        """Highlight block event called."""
        self.highlight_parsed_items(text)
        self.highlight_block_comment(text)
