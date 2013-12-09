#!/usr/bin/python

## primitives (inspired by Ferdinand Jamitzky)

class Function:
    def __init__(self, monadic, diadic, fun = 0):
        self.monadic = monadic
        self.diadic = diadic
        self.fun = fun
    def __neg__(self):
        self.fun = self.monadic	
        return self
    def __rsub__(self, left):
        self.fun = lambda x: self.diadic(left, x)
        self.left = left
        return self
    def __sub__(self, right):
        return self.fun(right)
    def __call__(self, right):
        return self.fun(right)   

class Operator:
    def __init__(self, body, fun = 0):
        self.body = body
        self.fun = fun
    def __radd__(self, left):
        return Operator(self.body, left)
    def __add__(self, right):
        return Function(0, 0, lambda x: self.body(self.fun, right, x))
    def __sub__(self, right):
        return self.body(self.fun, right)
   

class DomainError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


## generic functions

def _D_(on_scalar, error_message):
    def _d_(A, B):
        if isinstance(A, list) and isinstance(B, list):
            if(len(A) != len(B)):
                raise DomainError("Domain error in " + error_message)
            else:
                return [_d_(a, b) for (a, b) in zip(A, B)]
        elif isinstance(A, list) and not isinstance(B, list):
            return [_d_(a, B) for a in A]
        elif not isinstance(A, list) and isinstance(B, list):
            return _d_(B, A)
        else:
            return on_scalar(A, B)
    return _d_

def _M_(on_list, on_scalar):
    def _m_(A):
        if isinstance(A, list):
            return on_list(A)
        else:
            return on_scalar(A)
    return _m_


## functions

_d_add = _D_(lambda A, B: A+B, "'ADD'")
_d_sub = _D_(lambda A, B: A-B, "'SUB'")
_d_mul = _D_(lambda A, B: A*B, "'MUL'")
_d_div = _D_(lambda A, B: A/B, "'DIV'")

_m_sub = _M_(lambda A: [_m_sub(a) for a in A], lambda A: -A)
_m_add = _M_(lambda A: reduce(_d_add, A), lambda A: A)
_m_div = _M_(lambda A: [_m_div(a) for a in A], lambda A: 1.0/A)
_m_mirror = _M_(lambda A: [_m_wirror(a) for a in A], lambda A: A)
_m_wirror = _M_(lambda A: A[::-1], lambda A: A)
_m_transpose = _M_(lambda A: [list(row) for row in zip(*A)], lambda A: A)
_m_not = _M_(lambda A: [_m_not(a) for a in A], lambda A: int(not A))
_m_rank = _M_(lambda A: [len(A)] + _m_rank(A[0]), lambda A: [])

        
## function exceptions (and hacks)        

def _d_rank(r, A):
    if not isinstance(A, list):
        return _d_rank(r, [A])
    n = reduce(lambda x,y: x*y, r)
    d = n / r[0]
    if len(A) != n:
        A = (A * (n / len(r) + 1) )[:n]
    if len(r) == 1:
        return A
    return [_d_rank(r[1:], A[i*d: (i+1)*d]) for i in range(r[0])]

def _m_index(r, rs=[]):
    if r==[]:
        return rs
    else:
        return [_m_index(r[1:], rs+[i]) for i in range(r[0])]

def _d_index(A, r):
    ixs = []
    for i in r:
        try:
            ixs += [A.index(i)]
        except ValueError:
            ixs += [-1]
    return ixs

def _d_select(A, B):
    if isinstance(A, list) and isinstance(B, list) and len(A) == len(B):
        return [a for (a, b) in zip(A, B) if b == 1]
    else:
        raise DomainError("Domain error in 'SELECT'")
  
def _do_inner(A, lf, rf, B):	# I don't like it
    if isinstance(A[0], list):
    	return [[reduce(lf, rf(a, b)) for a in _m_transpose(A)] for b in B] 
    else:
        return reduce(lf, rf(A, B))


## interface

ADD = Function(_m_add, _d_add)
SUB = Function(_m_sub, _d_sub)
MUL = Function(0, _d_mul)
DIV = Function(_m_div, _d_div)

RANK = Function(_m_rank, _d_rank)
INDEX = Function(_m_index, _d_index)
MIRROR = Function(_m_mirror, 0)
WIRROR = Function(_m_wirror, 0)
TRANSPOSE = Function(_m_transpose, 0)

NOT = Function(_m_not, 0)
AND = Function(0, _D_(lambda A, B: int(A and B), 'AND'))
OR = Function(0, _D_(lambda A, B: int(A or B), 'OR'))
LT = Function(0, _D_(lambda A, B: int(A < B), 'LT'))
LE = Function(0, _D_(lambda A, B: int(A <= B), 'LE'))
EQ = Function(0, _D_(lambda A, B: int(A == B), 'EQ'))
GT = Function(0, _D_(lambda A, B: int(A > B), 'GT'))
GE = Function(0, _D_(lambda A, B: int(A >= B), 'GE'))
NE = Function(0, _D_(lambda A, B: int(A != B), 'NE'))

SELECT = Function(0, _d_select)

MAP = Operator(lambda fun, xs: [fun(x) for x in xs])
REDUCE = Operator(lambda fun, xs: _reduce(fun.diadic ,xs))
INNER = Operator(lambda lf, rf, xs: _do_inner(lf.left, lf.diadic, rf.diadic, xs))
OUTER = Operator(lambda fun, xs: [[fun.diadic(x, y) for y in fun.left] for x in xs])


## test
if __name__ == '__main__':
    ''' testing and demonstration part '''
    A = [[1,2],[3,4]]
    B = [7,8]
    C = [2,1]

    assert (B -ADD+INNER+MUL- C) == 22
    assert (A -ADD+INNER+MUL- A) == [[7, 10],[15,22]]
    assert ((-SUB- 1) -ADD- 2 -MUL- 3 -ADD+MAP- [1, 2, 3]) == [4, 5, 6]

    S = []
    while True:
        S += [eval(raw_input("      "))]
        print S[-1]
    



