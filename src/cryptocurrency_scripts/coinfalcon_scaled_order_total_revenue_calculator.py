import itertools
import operator


def calculate(order: str) -> float:
    """ 
    >>> calculate('1
    >>> 200.00000
    >>> 1500.0000
    >>> 2
    >>> 200.00000
    >>> 1375.0000
    >>> 3
    >>> 200.00000
    >>> 1250.0000
    >>> 4
    >>> 200.00000
    >>> 1125.0000
    >>> 5
    >>> 200.00000
    >>> 1000.0000') """

    return sum(itertools.starmap(operator.mul, zip(*[iter(map(float, (el for i, el in enumerate(order.split('\n')) if i % 3)))] * 2)))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--order', type=str)
    
    print(f'Total Revenue: {calculate(parser.parse_args().order)}€')
