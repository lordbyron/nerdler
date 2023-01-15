#!/usr/bin/env python3

from collections import Counter
from pprint import pprint

START = 0x10000000
END = 0x9fffffff
SPACES = 8
SAMPLE = 1000000
DEBUG = False
FNAME = f"nerdle.{SPACES}.txt"

def debug(msg):
    if DEBUG:
        print(msg)

def toStr(n, s=SPACES):
    return hex(n)[2:].rjust(SPACES, '0')[0:s]
    #return "{0:0{1}x}".format(n, SPACES)

def display(n, s=SPACES):
    return toStr(n, s).translate("".maketrans("abcde","+-*/="))

n_valid = 0
def is_valid(n):
    if n % SAMPLE == 0:
        print(f"sample {n} {display(n)}")
    if hex(n).count('f') == 0:
        global n_valid
        n_valid += 1
        return True
    return False

def filter_answer_zero(n):
    a = toStr(n)
    i_eq = a.find('e')
    if i_eq != SPACES-2 or a[SPACES-1] != '0':
        return False
    return True

n_syntax = 0
def is_syntax(n):
    a = toStr(n)
    # only one =
    if a.count('e') != 1:
        return False
    # can't start/end with an operator
    if not a[0].isnumeric() or not a[-1].isnumeric():
        return False
    # can't start with a 0
    if a[0] == '0':
        return False
    i_eq = a.index('e')
    # can't have the = left of half
    if i_eq < SPACES/2:
        return False
    for i in range(SPACES-1):
        # no adjacent operators
        if not a[i].isnumeric() and not a[i+1].isnumeric():
            return False
        # no 0 after an op, unless the answer is 0
        if not a[i].isnumeric() and a[i+1] == '0':
            if i != i_eq:
                return False
        # no ops after =
        if not a[i].isnumeric() and i > i_eq:
            return False
    global n_syntax
    n_syntax += 1
    return True

def is_true(n):
    debug("")
    debug(n)
    a = toStr(n)
    debug(a)
    debug(display(n))
    i_eq = a.index('e')
    debug(i_eq)
    debug(toStr(n, i_eq))
    lhs = eval(display(n, i_eq))
    v = lhs == int(a[i_eq + 1:])
    if v:
        print(display(n))
    return v

def find_good_eqs():
    total = END - START
    print(f"With {SPACES} spaces, looping {total} times.")
    #mode = "a" if START > 0 else "w"
    mode = "w"
    f = open(FNAME, mode)
    n_good = 0
    for good in filter(is_true, filter(is_syntax, filter(filter_answer_zero, filter(is_valid, range(START, END))))):
        f.write(str(good) + "\n")
        n_good += 1
    f.close()

    print(f"With {SPACES} spaces, looping {total} times.")
    print(f"Considered {n_valid} equations.")
    print(f"Of those, {n_syntax} had good syntax.")
    print(f"Of those, {n_good} were valid nerdles.")

def load_good():
    f = open(FNAME, "r")
    good = []
    for l in f:
        good.append(int(l))
    f.close()
    return good

def analyze(ns):
    digits = {}
    ops = {}
    with_any = {}
    with_two = {}
    has_doubles = 0

    matrix = [ [ 0 for i in range(SPACES+1) ] for j in range(15) ]

    for n in ns:
        a = toStr(n)

        i_eq = a.index('e')

        p = 0
        for c in a:
            matrix[int(c, 16)][p] += 1
            matrix[int(c, 16)][SPACES] += 1
            p += 1


        digits[SPACES-i_eq-1] = digits.get(SPACES-i_eq-1, 0) + 1

        counter = Counter(a)

        n_ops = counter['a'] + counter['b'] + counter['c'] + counter['d']
        ops[n_ops] = ops.get(n_ops, 0) + 1

        for d in counter.keys():
            with_any[d] = with_any.get(d, 0) + 1
            if counter[d] > 1:
                with_two[d] = with_two.get(d, 0) + 1
                if d in '1234567890':
                    has_doubles += 1

    print("RHS has digits:")
    pprint(digits)
    print("EQ has number of operators:")
    pprint(ops)
    print("EQ has at least one of:")
    pprint(with_any)
    print("EQ has at least two of:")
    pprint(with_two)
    print("LHS has any digit double:")
    pprint(has_doubles)
    print("Total solutions:")
    pprint(len(ns))
    print("Matrix")
    print(*["      ", "  P1  ", "  P2  ", "  P3  ", "  P4  ", "  P5  ", "  P6  ", "  P7  ", "  P8  ", " TOTAL"])
    for d,row in enumerate(matrix):
        print(*["{:^6}".format(hex(d)[2:])]+list(map(lambda x: "{:^6}".format(x), row)))


def dump(ns):
    f = open(f"nerdle.{SPACES}.eqs.txt", "w")
    for n in ns:
        f.write(display(n))
        f.write("\n")
    f.close()

#find_good_eqs()
analyze(load_good())
dump(load_good())
