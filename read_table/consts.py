import enum


class Element(str, enum.Enum):
    COL = "col"
    COLGROUP = "colgroup"
    TABLE = "table"
    TBODY = "tbody"
    TD = "td"
    TFOOT = "tfoot"
    TH = "th"
    THEAD = "thead"
    TR = "tr"


class Attribute(str, enum.Enum):
    COLSPAN = "colspan"
    ROWSPAN = "rowspan"
    SPAN = "span"


MAX_SPAN = 1000

MAX_COLSPAN = 1000

MAX_ROWSPAN = 65534
