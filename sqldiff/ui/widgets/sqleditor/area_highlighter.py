from abc import ABC, abstractmethod
from itertools import chain
from typing import Type, List, Optional, Iterable

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat, QTextFormat
from PyQt5.QtWidgets import QTextEdit, QPlainTextEdit

from sqldiff.sql.parse.compound import get_queries_to_highlight, get_query_at_index
from sqldiff.sql.parse.utils import QueryRange

EditorType = QPlainTextEdit


def selections_equal(s1, s2):
    return s1.format == s2.format and s1.cursor == s2.cursor


def get_document_viewport_range(editor: EditorType):
    """
    Finds start and end cursor positions of visible viewport of QTextEditor
    :param editor: sqleditor instance
    :return: range of start and end positions of visible vieport of sqleditor.
    """
    cursor = editor.cursorForPosition(QPoint(0, 0))
    start_pos = cursor.position()
    bottom_right = QPoint(editor.viewport().width(), editor.viewport().height())
    end_pos = editor.cursorForPosition(bottom_right).position()
    return range(start_pos, end_pos)


def move_cursor_by_lines(editor: EditorType, cursor_pos: int, move_operation, n: int) -> int:
    """
    :param editor: TextEdit instance
    :param cursor_pos: integer cursor position to start from
    :param move_operation:
    :param n: MoveOperation option, for example QTextCursor.Up
    :return: cursor position moved by move operation <n> times
    """
    cursor = editor.textCursor()
    cursor.setPosition(cursor_pos)
    for i in range(n):
        cursor.movePosition(move_operation)
    return cursor.position()


def extend_range_by_lines(editor: EditorType, e_range: range, lines_up: int, lines_down: int) -> range:
    """
    Extends e_range start position up by lines_up in sqleditor. Extends e_range end position up by lines_down in sqleditor.
    :param editor: sqleditor instance
    :param e_range: range start and end positions to start extending.
    :param lines_up: number of lines towards top of document to extend.
    :param lines_down: number of lines towards end of document to extend.
    :return: range extended by cursor positions needed to reach additional lines_up and lines_down.
    """
    r_start = move_cursor_by_lines(editor, e_range.start, QTextCursor.Up, lines_up)
    r_stop = move_cursor_by_lines(editor, e_range.stop, QTextCursor.Down, lines_down)
    return range(r_start, r_stop)


class TextEditorAreaFormatter:
    """
    Defines a way to create format for selected text range in sqleditor
    """

    def __init__(self, editor: EditorType):
        self.editor = editor
        self.selection = None

    def format_area(self, start_pos: int, end_pos: int, area_format: QTextCharFormat):
        selection = QTextEdit.ExtraSelection()
        selection.format = area_format
        selection.cursor = self.editor.textCursor()
        selection.cursor.setPosition(start_pos)
        selection.cursor.setPosition(end_pos, QTextCursor.KeepAnchor)
        self.selection = selection
        return selection


class TextEditorCurrentLineFormatter:
    """
    Defines a way to create format for full text sqleditor line for current cursor position
    """

    def __init__(self, editor: EditorType):
        self.editor = editor
        self.selection = None

    def format_line(self, line_format: QTextCharFormat) -> QTextEdit.ExtraSelection:
        selection = QTextEdit.ExtraSelection()
        selection.format = line_format
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = self.editor.textCursor()
        self.selection = selection
        return selection


class TextEditorFormatterBase(ABC):
    """
    Defines interface for classes generating selection formatting for provided Text Editor instance.
    """

    def __init__(self, editor: EditorType):
        """
        :param editor: SqlTextEdit type sqleditor
        (cannot use typing due to QtWidgets are unavailable until app initialization)
        """
        self.editor = editor

    @abstractmethod
    def highlight(self) -> Iterable[QTextEdit.ExtraSelection]:
        """
        Generates formatting data for specified text sqleditor.
        :return: Iterable of ExtraSelection (may return multiple formatting selections)
        """
        pass


class SqlStatementsBackgroundFormatterRanged(TextEditorFormatterBase):
    """
    Defines formatting for multiple sql statements in sqleditor, without leading whitespaces and comments.
    """

    def __init__(self, editor: EditorType, h_format: QTextCharFormat):
        super().__init__(editor)
        self.format = h_format
        self.area_highlighter = TextEditorAreaFormatter(self.editor)

    def highlight(self) -> Iterable[QTextEdit.ExtraSelection]:
        plain_text = self.editor.document().toPlainText()
        document_range = get_document_viewport_range(self.editor)
        extend_lines_up = 5
        extend_lines_down = 5
        document_extended_range = extend_range_by_lines(self.editor, document_range, extend_lines_up, extend_lines_down)
        range_text = plain_text[document_extended_range.start:document_extended_range.stop]
        queries_positions = get_queries_to_highlight(range_text, range(0, len(range_text)))
        # TODO: some colors depends on sql type (SELECT / INSERT / DELETE etc)
        for query, query_range in queries_positions:
            r_start = document_extended_range.start + query_range.start
            r_stop = document_extended_range.start + query_range.stop
            yield self.area_highlighter.format_area(r_start, r_stop, self.format)


class CurrentLineFormatter(TextEditorFormatterBase):
    """
    Defines formatting for text sqleditor line on current cursor position
    """

    def __init__(self, editor: EditorType, h_format: QTextCharFormat):
        super().__init__(editor)
        self.format = h_format
        self.line_highlighter = TextEditorCurrentLineFormatter(self.editor)

    def highlight(self) -> Iterable[QTextEdit.ExtraSelection]:
        yield self.line_highlighter.format_line(self.format)


class SqlAtCursorFinder:
    """
    Finds sql statement at current cursor position in text sqleditor
    """

    def __init__(self, editor: EditorType):
        self.editor = editor
        self.query_range_at_cursor: Optional[QueryRange] = None

    def find_query_range_at_index(self, index=None):
        if not index:
            index = self.editor.textCursor().position()
        self.query_range_at_cursor = get_query_at_index(self.editor.toPlainText(), index)
        return self.query_range_at_cursor


class CurrentSqlStatementHighlighter(TextEditorFormatterBase):
    """
    Finds and defines formatting for sql statement at current cursor position in sqleditor.
    """

    def __init__(self, editor: EditorType, query_finder: SqlAtCursorFinder, h_format: QTextCharFormat):
        super().__init__(editor)
        self.query_finder = query_finder
        self.format = h_format
        self.area_highlighter = TextEditorAreaFormatter(editor)

    def highlight(self) -> Iterable[QTextEdit.ExtraSelection]:
        query = self.query_finder.query_range_at_cursor
        if query:
            yield self.area_highlighter.format_area(query.q_range.start, query.q_range.stop, self.format)


class FormattingManager:
    """
    Formatting manager groups multiple text sqleditor formatting data.
    Manager iterates through formatters and applies them onto sqleditor.
    Trigger condition for apply_formatting method should be defined in sqleditor class
    (depends on needs, formatter groups, etc).
    Formatters are applied in order of formatters list.
    """

    def __init__(self, editor: EditorType, formatters: List[TextEditorFormatterBase] = None):
        self.editor = editor
        self.formatters = formatters or []

    def apply_formatting(self):
        """
        Overwrites extra selections and applies formats from all formatters onto sqleditor.
        :return:
        """
        extra_selections = list(chain(h for f in self.formatters for h in f.highlight()))
        # Overwrite current extra selections with new
        self.editor.setExtraSelections(extra_selections)

    def append(self, highlighter):
        self.formatters.append(highlighter)
