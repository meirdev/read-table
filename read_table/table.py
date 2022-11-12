import itertools
from typing import Any

from bs4 import BeautifulSoup

from .matrix import Matrix
from .parser import parse_tables


def convert_table_to_data(table):
    matrix = Matrix[Any]()

    row_i = 0

    for section in table.sections:
        for row in section:
            col_i = 0

            for cell in row:
                if cell.row_span == 0:
                    row_span = len(section)
                else:
                    row_span = min(len(section), cell.row_span)

                cols_in_group = table.columns_in_group(col_i)

                if cols_in_group != -1:
                    if cell.col_span == 0:
                        col_span = cols_in_group
                    else:
                        col_span = min(cols_in_group, cell.col_span)
                else:
                    col_span = cell.col_span

                for i in range(row_span):
                    while matrix[row_i + i, col_i] is not None:
                        col_i += 1

                    for j in range(col_span):
                        matrix[row_i + i, col_i + j] = cell.data

                col_i += col_span

            row_i += 1

    return matrix.data


def read_table(
    markup: str | bytes, attrs: dict[str, str] | None = None, **bs_options: Any
):
    soup = BeautifulSoup(markup, features=bs_options.pop("features", "html.parser"))

    tables = []

    for table in parse_tables(soup, attrs):
        tables.append(convert_table_to_data(table))

    return tables


def to_dict(
    table: list[list[Any]], header: list[str] | None = None
) -> list[dict[str, Any]]:
    if len(table) == 0:
        return []

    if header is None:
        header = table[0]
        table = table[1:]
    else:
        header: list[str | None] = header.copy()  # type: ignore[no-redef]

        if len(header) < len(table[0]):
            header += [None] * (len(table[0]) - len(header))  # type: ignore[list-item]

    if len(table) == 0:
        return []

    for i in range(len(header)):
        if header[i] is None:
            header[i] = f"{i}"

    data: list[dict[str, Any]] = []

    for row in table:
        data.append(dict(itertools.zip_longest(header, row)))

    return data
