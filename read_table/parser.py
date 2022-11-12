import typing

from bs4.element import Tag

from .consts import MAX_COLSPAN, MAX_ROWSPAN, MAX_SPAN, Attribute, Element
from .elements import (
    Table,
    TableBody,
    TableCell,
    TableCol,
    TableFooter,
    TableHeader,
    TableRow,
    TableSection,
)


@typing.no_type_check
def parse_span(value: str | None, max_value: int | None = None) -> int:
    if value is None:
        return 1

    try:
        value = int(value)
    except ValueError:
        return 1

    if value < 0:
        return 1

    if value > max_value:
        return max_value

    return value


def parse_row(element_row) -> TableRow:
    row = TableRow()

    for element in element_row.find_all([Element.TD, Element.TH]):
        row_span = parse_span(element.get(Attribute.ROWSPAN), MAX_ROWSPAN)
        col_span = parse_span(element.get(Attribute.COLSPAN), MAX_COLSPAN)

        row.append(TableCell(element.get_text(" ", strip=True), row_span, col_span))

    return row


def parse_cols(element_col, group: int | None) -> list[TableCol]:
    cols: list[TableCol] = []

    for _ in range(parse_span(element_col.get(Attribute.SPAN), MAX_SPAN)):
        cols.append(TableCol(group))

    return cols


def parse_table(element_table) -> Table:
    table = Table()
    section: TableSection = TableBody()

    for element in element_table.children:
        match element.name:
            case Element.TR:
                section.append(parse_row(element))

            case Element.THEAD | Element.TBODY | Element.TFOOT:
                if len(section):
                    table.sections.append(section)

                match element.name:
                    case Element.THEAD:
                        section = TableHeader()
                    case Element.TFOOT:
                        section = TableFooter()
                    case _:
                        section = TableBody()

                for element_row in element.find_all(Element.TR):
                    section.append(parse_row(element_row))

                table.sections.append(section)
                section = TableBody()

            case Element.COL:
                table.columns += parse_cols(element, None)

            case Element.COLGROUP:
                table.column_group += 1

                if span_attr := element.get(Attribute.SPAN):
                    span = parse_span(span_attr, MAX_SPAN)
                else:
                    span = 0

                cols = element.find_all(Element.COL)

                if span and len(cols) == 0:
                    cols = [element]

                for col in cols:
                    table.columns += parse_cols(col, table.column_group)

    if len(section):
        table.sections.append(section)

    def sort_section(section_: TableSection) -> int:
        return {TableHeader: 0, TableBody: 1, TableFooter: 2}.get(section_.__class__, 3)

    table.sections.sort(key=sort_section)

    return table


def parse_tables(root: Tag, attrs: dict[str, str] | None) -> list[Table]:
    tables: list[Table] = []

    params = {}

    if attrs is not None:
        params["attrs"] = attrs

    for element in root.find_all(Element.TABLE, recursive=True, **params):  # type: ignore[arg-type]
        tables.append(parse_table(element))

    return tables
