from abc import ABC, abstractmethod

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat, QTextFormat
from PyQt5.QtWidgets import QTextEdit

from sqldiff.sql.parse.compound import get_queries_to_highlight


def selections_equal(s1, s2):
    return s1.format == s2.format and s1.cursor == s2.cursor


def get_document_viewport_range(editor):
    cursor = editor.cursorForPosition(QPoint(0, 0))
    start_pos = cursor.position()
    bottom_right = QPoint(editor.viewport().width(), editor.viewport().height())
    end_pos = editor.cursorForPosition(bottom_right).position()
    return range(start_pos, end_pos)


def move_cursor_by_lines(editor, cursor_pos: int, move_operation, n):
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


def extend_range_by_lines(editor, e_range, lines_up, lines_down):
    r_start = move_cursor_by_lines(editor, e_range.start, QTextCursor.Up, lines_up)
    r_stop = move_cursor_by_lines(editor, e_range.stop, QTextCursor.Down, lines_down)
    return range(r_start, r_stop)


class TextEditorAreaFormatter:
    def __init__(self, editor):
        self.editor = editor

    def format_area(self, start_pos, end_pos, area_format):
        extra_selections = self.editor.extraSelections()
        selection = QTextEdit.ExtraSelection()
        selection.format = area_format
        selection.cursor = self.editor.textCursor()
        selection.cursor.setPosition(start_pos)
        selection.cursor.setPosition(end_pos, QTextCursor.KeepAnchor)

        # for i in extra_selections:
        #     if selections_equal(i, selection):
        #         return
        extra_selections.append(selection)
        self.editor.setExtraSelections(extra_selections)


class TextEditorCurrentLineFormatter:
    def __init__(self, editor):
        self.editor = editor

    def format_line(self, line_format):
        extra_selections = self.editor.extraSelections()
        selection = QTextEdit.ExtraSelection()
        selection.format = line_format
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = self.editor.textCursor()
        extra_selections.append(selection)
        self.editor.setExtraSelections(extra_selections)


class TextEditorHighlighterBase(ABC):

    def __init__(self, editor):
        self.editor = editor
        self.setup_highlight_events()

    def _call_highlight(self):
        self.highlight()

    def setup_highlight_events(self):
        pass

    @abstractmethod
    def highlight(self):
        pass


class UpdateRequestTextEditorHighlighter(TextEditorHighlighterBase):

    def __init__(self, editor):
        super().__init__(editor)
        # semaphore
        self.highlighting = False

    def _call_highlight(self):
        if not self.highlighting:
            self.highlighting = True
            self.highlight()
            self.highlighting = False

    def setup_highlight_events(self):
        # self.editor.cursorPositionChanged.connect(self.highlight)
        self.editor.updateRequest.connect(self._call_highlight)

    @abstractmethod
    def highlight(self):
        pass


class SqlStatementsBackgroundHighlighter(TextEditorHighlighterBase):
    """
    Highlights
    """

    def __init__(self, editor):
        super().__init__(editor)

        self.color = QColor(130, 130, 225, 30)
        self.format = QTextCharFormat()
        self.format.setBackground(self.color)
        self.area_highlighter = TextEditorAreaFormatter(editor)

    def highlight(self):
        plain_text = self.editor.document().toPlainText()
        queries_positions = get_queries_to_highlight(plain_text, get_document_viewport_range(self.editor))
        # TODO: some colors depends on sql type (SELECT / INSERT / DELETE etc)

        for query, query_range in queries_positions:
            self.area_highlighter.format_area(query_range.start, query_range.stop, self.format)


class SqlStatementsBackgroundHighlighterRanged(SqlStatementsBackgroundHighlighter):
    """
    Sql statement background highlighter optimized for highlighting only statements in visible editor's viewport.
    """

    def __init__(self, editor):
        super().__init__(editor)
        self.selected_color = QColor(230, 100, 100, 150)
        self.selected_format = QTextCharFormat()
        self.selected_format.setBackground(self.selected_color)

    def highlight(self):
        print('highlight called')
        plain_text = self.editor.document().toPlainText()
        document_range = get_document_viewport_range(self.editor)
        document_range = extend_range_by_lines(self.editor, document_range, 3, 3)
        range_text = plain_text[document_range.start:document_range.stop]
        queries_positions = get_queries_to_highlight(range_text, range(0, len(range_text)))
        # TODO: some colors depends on sql type (SELECT / INSERT / DELETE etc)
        a = 1
        cursor_pos = self.editor.textCursor().position()
        print(f'{cursor_pos=}')
        for query, query_range in queries_positions:
            print(f'{query_range=}')
            r_start = document_range.start + query_range.start
            r_stop = document_range.start + query_range.stop
            bg_format = self.format
            if self.editor.textCursor().position() in range(r_start, r_stop):
                print(f'query selected {query}')
                # bg_format = self.selected_format
            self.area_highlighter.format_area(r_start, r_stop, bg_format)


class CurrentLineHighlighter(TextEditorHighlighterBase):
    def __init__(self, editor):
        super().__init__(editor)
        self.line_color = QColor(150, 200, 250, 50)
        self.format = QTextCharFormat()
        self.format.setBackground(self.line_color)
        self.line_highlighter = TextEditorCurrentLineFormatter(self.editor)

    def highlight(self):
        self.line_highlighter.format_line(self.format)


class CompositeEditorHighlighter(UpdateRequestTextEditorHighlighter):
    def __init__(self, editor):
        super().__init__(editor)
        self.highlighters = [
            CurrentLineHighlighter(editor),
            SqlStatementsBackgroundHighlighterRanged(editor)
        ]

    def highlight(self):
        self.editor.setExtraSelections([])
        for i in self.highlighters:
            i.highlight()
