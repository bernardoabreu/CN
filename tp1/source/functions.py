import math
import sys


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    return 0 if b == 0 else a / b


def log(x):
    try:
        return math.log(x)
    except ValueError:
        return 0


def sqrt(x):
    return 0 if x < 0 else math.sqrt(x)


def power(x, y):
    try:
        return math.pow(x, y)
    except ValueError:
        return 0
    except OverflowError:
        return 0


UNARY = (log, math.cos, math.sin, sqrt)


OP_DICT = {
    add: '+',
    sub: '-',
    mul: '*',
    div: '/',
    log: 'log',
    math.sin: 'sin',
    math.cos: 'cos',
    sqrt: 'sqrt',
    power: 'pow'
}
