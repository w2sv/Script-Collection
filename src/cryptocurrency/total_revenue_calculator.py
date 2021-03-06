from typing import List, Sequence, Any, Iterator, Tuple

import itertools
import operator
import enum


def scaled_order_preview_revenue(order: str) -> float:
    """
        Args:
            order: flattened, \n split rows of order data adhering to column structure of
                #
                Size (MIOT)
                Price (EUR)

    >>> order = '''1\500.00000\10.0000\n2\n500.00000\n5.0000'''
    >>> scaled_order_preview_revenue(order)
    7500 """

    return _calculate(order, relevant_column_indices=[1, 2], total_columns=3)


def closed_order_revenue(order: str) -> float:
    """ Args:
            order: flattened, \n split rows of order data adhering to column structure of
                Size (MIOT)
                Filled
                Price (EUR)
                Time
                Type
                Status

    >>> order = '''226.90799\n226.90799\n1.2000\n21-02-15 - 14:18:46\nSell\nFilled\n453.81599\n453.81599\n1.3000\n21-02-15 - 14:18:46\nSell\nFilled'''
    >>> closed_order_revenue(order)
    862.250375 """

    return _calculate(order, relevant_column_indices=[0, 2], total_columns=6)


def _calculate(order: str, relevant_column_indices: List[int], total_columns: int) -> float:
    selectors = [i in relevant_column_indices for i in range(total_columns)]

    return sum(itertools.starmap(operator.mul, map(lambda row: map(float, itertools.compress(row, selectors=selectors)), _chunk_iterator(order.split('\n'), chunk_size=total_columns))))


def _chunk_iterator(sequence: Sequence[Any], chunk_size: int) -> Iterator[Tuple[Any]]:
    return zip(*[iter(sequence)] * chunk_size)


if __name__ == '__main__':
    """ Execution steps:
            - Replace order variable value by your order
            - determine OrderOrigin
            - run """


    class OrderOrigin(enum.Enum):
        ScaledOrderPreview = 0
        OrderOverview = 1


    # parameters to be modified
    oder_origin = OrderOrigin.OrderOverview
    order = """ 1
            500.00000
            10.0000
            2
            500.00000
            5.0000 """

    print(f'Total Revenue: {[scaled_order_preview_revenue, closed_order_revenue][oder_origin.value()](order=order)}€')
