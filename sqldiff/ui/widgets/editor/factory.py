from abc import ABC, abstractmethod

from PyQt5.QtGui import QTextCharFormat, QColor

from sqldiff.ui.widgets.editor.area_highlighter import EditorType, FormattingManager, CurrentLineFormatter, \
    CurrentSqlStatementHighlighter, SqlAtCursorFinder
from sqldiff.ui.widgets.editor.sql_editor import SqlTextEdit
from sqldiff.ui.widgets.editor.syntax_highlighter import GenericSqlHighlighter

# Sql editor default highlight formats
current_sql_format = QTextCharFormat()
current_sql_format.setBackground(QColor(150, 110, 190, 50))

current_line_format = QTextCharFormat()
current_line_format.setBackground(QColor(150, 200, 250, 50))

sql_background_format = QTextCharFormat()
sql_background_format.setBackground(QColor(230, 100, 100, 150))


class SqlEditorFactory(ABC):
    """Factory method interface for creating SqlEditor instance."""

    @abstractmethod
    def create_editor(self) -> EditorType:
        pass


class BaseSqlEditorFactory(SqlEditorFactory):
    """Factory class for SqlEditor class instance."""

    def create_editor(self) -> EditorType:
        editor = SqlTextEdit()

        syntax_highlighter = GenericSqlHighlighter(editor.document())

        sql_at_cursor_finder = SqlAtCursorFinder(editor)

        formatting_manager = FormattingManager(editor)
        formatting_manager.append(CurrentLineFormatter(editor, current_line_format))
        formatting_manager.append(CurrentSqlStatementHighlighter(editor, sql_at_cursor_finder, current_sql_format))

        editor.syntax_highlighter = syntax_highlighter
        editor.formatting_manager = formatting_manager
        editor.sql_at_cursor_finder = sql_at_cursor_finder

        return editor
