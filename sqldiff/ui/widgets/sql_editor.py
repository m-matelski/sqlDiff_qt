from PyQt5 import QtGui
from PyQt5.QtCore import QSize, QRect, Qt
from PyQt5.QtGui import QColor, QTextFormat, QPaintEvent, QPainter, QTextBlock, QSyntaxHighlighter, QTextCursor, \
    QTextCharFormat
from PyQt5.QtWidgets import QTextEdit, QPlainTextEdit, QWidget, QVBoxLayout

from sqldiff.sql.parse import MultiSqlParser
from sqldiff.ui.widgets.syntax_highlighter import GenericSqlParserHighlighter, GenericKeywordSqlHighlighter, \
    GenericSqlHighlighter


class CodeTextEdit(QPlainTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        self.highlight_current_line()

        doc = self.document()
        font = doc.defaultFont()
        font.setFamily("Courier New")
        doc.setDefaultFont(font)

    def line_number_area_width(self):
        digits = 1
        m = max(1, self.blockCount())
        while m >= 10:
            m //= 10
            digits += 1

        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits  # QLatin1Char
        return space

    def update_line_number_area_width(self, newBlockCount):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect: QRect, dy: int):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        super().resizeEvent(e)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def highlight_current_line(self):
        extra_selections = list()

        if not self.isReadOnly():
            line_color = QColor(150, 200, 250, 50)
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            # selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def line_number_area_paint_event(self, event: QPaintEvent):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), self.fontMetrics().height(), Qt.AlignRight,
                                 number)
            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1


class LineNumberArea(QWidget):
    def __init__(self, editor: CodeTextEdit, *args, **kwargs):
        super().__init__(editor, *args, **kwargs)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        self.editor.line_number_area_paint_event(event)


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
        extra_selections.append(selection)
        self.editor.setExtraSelections(extra_selections)


class SqlBackgroundHighlighter:
    def __init__(self, editor):
        self.editor = editor
        self.color = QColor(130, 130, 225, 30)
        self.format = QTextCharFormat()
        self.format.setBackground(self.color)
        self.area_highlighter = TextEditorAreaFormatter(editor)

    def highlight(self):
        plain_text = self.editor.document().toPlainText()
        parsed = MultiSqlParser(plain_text)
        queries_positions = parsed.get_queries_positions()

        for q_range, query in queries_positions:
            self.area_highlighter.format_area(q_range.start, q_range.stop, self.format)



class SqlTextEdit(CodeTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sql_background_highlighter = SqlBackgroundHighlighter(self)

        # self.syntax_highlighter = GenericSqlParserHighlighter(self.document())
        self.syntax_highlighter = GenericSqlHighlighter(self.document())
        # self.syntax_highlighter = GenericSqlHighlighter(self.document())

        self.cursorPositionChanged.connect(self.highlight_sql_statements)

    def highlight_sql_statements(self):
        self.sql_background_highlighter.highlight()
        pass


class SqlEditorWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sql_text_editor = SqlTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.sql_text_editor)
        self.setLayout(layout)
