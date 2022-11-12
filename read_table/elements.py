from typing import Any, NamedTuple


class TableCol(NamedTuple):
    group: int | None = None


class TableCell(NamedTuple):
    data: Any
    row_span: int
    col_span: int


class TableRow(list[TableCell]):
    pass


class TableSection(list[TableRow]):
    pass


class TableHeader(TableSection):
    pass


class TableBody(TableSection):
    pass


class TableFooter(TableSection):
    pass


class Table:
    def __init__(self) -> None:
        self.column_group = 0
        self.columns: list[TableCol] = []
        self.sections: list[TableSection] = []

    def columns_in_group(self, column: int) -> int:
        if column >= len(self.columns):
            return -1

        group = self.columns[column].group
        if group is None:
            return -1

        return len([i for i in self.columns if i.group == group])
