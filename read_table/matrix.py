from typing import Any, Generic, Optional, TypeVar

Index = tuple[int, int]

T = TypeVar("T")


class Matrix(Generic[T]):
    def __init__(self) -> None:
        self._data: dict[Index, Optional[T]] = {}

        self._d1 = 0
        self._d2 = 0

    def __getitem__(self, index: Index) -> Any:
        return self._data.get(index)

    def __setitem__(self, index: Index, value: Any) -> None:
        self._d1 = max(self._d1, index[0])
        self._d2 = max(self._d2, index[1])

        self._data[index] = value

    @property
    def data(self) -> list[list[Optional[T]]]:
        matrix: list[list[Optional[T]]] = []

        if len(self._data) == 0:
            return matrix

        for d1_i in range(self._d1 + 1):
            matrix.append([])

            for d2_i in range(self._d2 + 1):
                matrix[d1_i].append(self._data.get((d1_i, d2_i)))

        return matrix
