from typing import Tuple, Callable, Optional

QueryRangeTuple = Tuple[str, range]
Sub = Callable[[str, Optional[range]], QueryRangeTuple]


class SqlParseException(Exception):
    pass


class SingleSqlStatementExpectedException(SqlParseException):
    pass


