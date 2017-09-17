import math


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    return 1 if b == 0 else a / b


def log(x):
    try:
        return math.log(x)
    except ValueError:
        return 0


def sqrt(x):
    return 1 if x < 0 else math.sqrt(x)


def power(x):
    return x**2


UNARY = (log, math.cos, math.sin, sqrt, power)


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
