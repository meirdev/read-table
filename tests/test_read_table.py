from read_table import read_table, to_dict


def test_read_table_rowspan():
    html = """
<table>
    <tr>
        <td>1</td>
        <td rowspan="2">2</td>
        <td>3</td>
    </tr>
    <tr>
        <td>4</td>
        <td>6</td>
    </tr>
    <tr>
        <td>7</td>
        <td>8</td>
        <td>9</td>
    </tr>
</table>
"""
    table = read_table(html)

    assert table == [[
        ["1", "2", "3"],
        ["4", "2", "6"],
        ["7", "8", "9"],
    ]]


def test_read_table_colspan():
    html = """
<table>
<tr>
    <td>1</td>
    <td>2</td>
    <td>3</td>
</tr>
<tr>
    <td colspan="2">4</td>
    <td>6</td>
</tr>
<tr>
    <td>7</td>
    <td>8</td>
    <td>9</td>
</tr>
</table>
"""

    table = read_table(html)

    assert table == [[
        ["1", "2", "3"],
        ["4", "4", "6"],
        ["7", "8", "9"],
    ]]


def test_read_table_colspan_and_rowspan_overlapping():
    html = """
<table>
    <tr>
        <td>1</td>
        <td>2</td>
        <td>3</td>
    </tr>
    <tr>
        <td>4</td>
        <td rowspan="2">5</td>
        <td>6</td>
    </tr>
    <tr>
        <td colspan="2">7</td>
        <td>9</td>
    </tr>
</table>
"""

    table = read_table(html)

    assert table == [[
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "7", "9"],
    ]]


def test_read_table_sections_order():
    html = """
<table>
    <tr>
        <td>4</td>
        <td>5</td>
        <td>6</td>
    </tr>
    <tbody>
        <tr>
            <td>7</td>
            <td>8</td>
            <td>9</td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <td>10</td>
            <td>11</td>
            <td>12</td>
        </tr>
    </tfoot>
    <thead>
        <tr>
            <td>1</td>
            <td>2</td>
            <td>3</td>
        </tr>
    </thead>
</table>
"""

    table = read_table(html)

    assert table == [[
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
        ["10", "11", "12"],
    ]]


def test_read_table_rowspan_and_sections():
    html = """
<table>
    <tbody>
        <tr>
            <td>1</td>
            <td rowspan="4">2</td>
            <td>3</td>
        </tr>
        <tr>
            <td>4</td>
            <td>6</td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <td>7</td>
            <td>8</td>
            <td>9</td>
        </tr>
    </tfoot>
</table>
    """

    table = read_table(html)

    assert table == [[
        ["1", "2", "3"],
        ["4", "2", "6"],
        ["7", "8", "9"],
    ]]


def test_read_table_colspan_and_colgroup():
    html = """
<table>
    <colgroup>
        <col span="2">
        <col>
    </colgroup>
    <tr>
        <td>1</td>
        <td>2</td>
        <td>3</td>
    </tr>
    <tr>
        <td colspan="4">4</td>
    </tr>
    <tr>
        <td>7</td>
        <td>8</td>
        <td>9</td>
    </tr>
</table>
"""

    table = read_table(html)

    assert table == [[
        ["1", "2", "3"],
        ["4", "4", "4",],
        ["7", "8", "9"],
    ]]


def test_read_table_cols():
    html = """
<table>
    <col>
    <col span="2">
    <col>
    <tr>
        <td>1</td>
        <td>2</td>
        <td>3</td>
        <td>4</td>
    </tr>
    <tr>
        <td>5</td>
        <td>6</td>
        <td>7</td>
        <td>8</td>
    </tr>
</table>
"""

    table = read_table(html)

    assert table == [[
        ["1", "2", "3", "4"],
        ["5", "6", "7", "8"],
    ]]


def test_read_table_illegal_span_value():
    html = """
<table>
    <tr>
        <td>1</td>
        <td colspan="2a">2</td>
        <td>3</td>
    </tr>
    <tr>
        <td>4</td>
        <td>5</td>
        <td>6</td>
    </tr>
</table>
"""

    table = read_table(html)

    assert table == [[
        ["1", "2", "3"],
        ["4", "5", "6"],
    ]]


def test_read_table_negative_span_value():
    html = """
<table>
    <tr>
        <td>1</td>
        <td colspan="-2">2</td>
        <td>3</td>
    </tr>
    <tr>
        <td>4</td>
        <td>5</td>
        <td>6</td>
    </tr>
</table>
"""

    table = read_table(html)

    assert table == [[
        ["1", "2", "3"],
        ["4", "5", "6"],
    ]]


def test_read_table_max_span_value():
    html = """
<table>
    <tr>
        <td>1</td>
        <td colspan="10001">2</td>
        <td>3</td>
    </tr>
    <tr>
        <td>4</td>
        <td>5</td>
        <td>6</td>
    </tr>
</table>
"""

    table = read_table(html)

    arr_2 = ["2"] * 1000
    arr_none = [None] * 999

    assert table == [[
        ["1", *arr_2, "3"],
        ["4", "5", "6", *arr_none],
    ]]


def test_read_table_colgroup_with_span_and_cols():
    html = """
<table>
    <colgroup span="2">
        <col>
        <col>
        <col>
    </colgroup>
    <tr>
        <td colspan="4">1</td>
        <td>2</td>
        <td>3</td>
    </tr>
</table>
"""

    table = read_table(html)

    assert table == [[
        ["1", "1", "1", "2", "3"],
    ]]


def test_read_table_colgroup_with_span():
    html = """
<table>
    <col />
    <colgroup span="2" />
    <tr>
        <td>1</td>
        <td colspan="3">2</td>
        <td>3</td>
    </tr>
</table>
"""

    table = read_table(html)

    assert table == [[
        ["1", "2", "2", "3"],
    ]]


def test_read_table_find_table_by_id():
    html = """
<table id="table1">
    <tr>
        <td>1</td>
        <td>2</td>
        <td>3</td>
    </tr>
</table>
<table id="table2">
    <tr>
        <td>4</td>
        <td>5</td>
        <td>6</td>
    </tr>
</table>
"""

    table = read_table(html, attrs={"id": "table2"})

    assert table == [[
        ["4", "5", "6"],
    ]]


def test_read_table_rowspan_zero():
    html = """
<table>
    <tbody>
        <tr>
            <td>1</td>
            <td rowspan="0">2</td>
            <td>3</td>
        </tr>
        <tr>
            <td>4</td>
            <td>5</td>
            <td>6</td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <td>7</td>
            <td>8</td>
            <td>9</td>
        </tr>
    </tfoot>
</table>
"""

    table = read_table(html)

    assert table == [[
        ["1", "2", "3", None],
        ["4", "2", "5", "6"],
        ["7", "8", "9", None],
    ]]


def test_read_table_colspan_zero():
    html = """
<table>
    <colgroup>
        <col>
        <col>
    </colgroup>
    <colgroup span="1" />
    <tr>
        <td colspan="0">1</td>
        <td>2</td>
        <td>3</td>
    </tr>
    <tr>
        <td>4</td>
        <td>5</td>
        <td>6</td>
    </tr>
</table>
"""

    table = read_table(html)

    assert table == [[
        ["1", "1", "2", "3"],
        ["4", "5", "6", None],
    ]]


def test_to_dict():
    html = """
<table>
    <tr>
        <th>name</th>
        <th>age</th>
    </tr>
    <tr>
        <td>John</td>
        <td>20</td>
    </tr>
    <tr>
        <td>Mike</td>
        <td>30</td>
    </tr>
</table>
"""

    table = read_table(html)

    assert to_dict(table[0]) == [
        {"name": "John", "age": "20"},
        {"name": "Mike", "age": "30"},
    ]


def test_to_dict_with_header():
    html = """
<table>
    <tr>
        <td>John</td>
        <td>20</td>
    </tr>
    <tr>
        <td>Mike</td>
        <td>30</td>
    </tr>
</table>
"""

    table = read_table(html)

    assert to_dict(table[0], header=["name", "age"]) == [
        {"name": "John", "age": "20"},
        {"name": "Mike", "age": "30"},
    ]


def test_to_dict_with_short_header():
    html = """
<table>
    <tr>
        <td>John</td>
        <td>Smith</td>
    </tr>
    <tr>
        <td>Mike</td>
        <td>Johnson</td>
    </tr>
</table>
"""

    table = read_table(html)

    assert to_dict(table[0], header=["name"]) == [
        {"name": "John", "1": "Smith"},
        {"name": "Mike", "1": "Johnson"},
    ]


def test_to_dict_with_long_header():
    html = """
<table>
    <tr>
        <td>John</td>
        <td>20</td>
    </tr>
    <tr>
        <td>Mike</td>
        <td>30</td>
    </tr>
</table>
"""

    table = read_table(html)

    assert to_dict(table[0], header=["name", "age", "address"]) == [
        {"name": "John", "age": "20", "address": None},
        {"name": "Mike", "age": "30", "address": None},
    ]


def test_to_dict_empty_table():
    html = """
<table>
</table>
    """

    table = read_table(html)

    print(table)

    assert to_dict(table[0]) == []


def test_to_dict_empty_table_without_header():
    html = """
<table>
    <thead>
        <tr>
            <th>name</th>
            <th>age</th>
        </tr>
    </thead>
</table>
    """

    table = read_table(html)

    assert to_dict(table[0]) == []
