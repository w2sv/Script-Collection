from typing import List, Sequence, Any, Iterator, Tuple

import itertools
import operator


def scaled_order_revenue(order: str) -> float:
    return _calculate(order, relevant_column_indices=[1, 2], total_columns=3)


def closed_order_revenue(order: str) -> float:
    return _calculate(order, relevant_column_indices=[0, 2], total_columns=5)


def _calculate(order: str, relevant_column_indices: List[int], total_columns: int) -> float:
    r"""
    >>> _calculate(r'1\n200.00000\n1500.0000\n2\n200.00000\n1375.0000')
    575000.0 """

    selectors = [i in relevant_column_indices for i in range(total_columns)]

    return sum(itertools.starmap(operator.mul, map(lambda row: map(float, itertools.compress(row, selectors=selectors)), _chunk_iterator(order.split('\n'), chunk_size=total_columns))))


def _chunk_iterator(sequence: Sequence[Any], chunk_size: int) -> Iterator[Tuple[Any]]:
    return zip(*[iter(sequence)] * chunk_size)


if __name__ == '__main__':
    IS_CLOSED_ODER = False
    ORDER = """  """

    print(f'Total Revenue: {[scaled_order_revenue, closed_order_revenue][IS_CLOSED_ODER](order=ORDER)}€')
