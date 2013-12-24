arrpl
=====

Array processing library for Python inspired by APL

Basically you can work in Python and use APL-like monadic and diadic functions and operators to work on pythons lists. Like this:

    A = [[1,2],[3,4]]
    B = [7,8]
    C = [2,1]
    
    assert B -PLUS- 1 == [7, 8]
    assert B -PLUS- C == [9, 9]
    
Python doesn't have operator overloading except for a predefined set, so in order to implement new words, I had to borrow an idea from Ferdinand Jamitzky. You shoud better check the code, it is better than any possible explanation. Long story short, functions (as in APL) ought to be surrounded by '-' signs, and operators (as in APL) - to be bounded with functions by '+' sign:

    assert -PLUS+REDUCE- B == 15            # +/ B
    assert (B -PLUS+INNER+MUL- C) == 22     # B +.× C 
    assert (A -PLUS+INNER+MUL- A) == [[7, 10],[15,22]]  # A +.× A


The order of execution is left to right, as in Python, not like in APL:

    assert ((-MINUS- 1) -PLUS- 2 -MUL- 3 -PLUS- [1, 2, 3]) == [4, 5, 6]


Generally, as you might wittness, it is not APL. It is Python with the some new syntax sweets.


So far I have implemented several functions:

    PLUS
    MINUS
    MUL
    DIV
    MOD
    POW

    RANK      # ⍴
    INDEX     # ⍳
    MIRROR    # ⌽
    WIRROR    # ⊖
    TRANSPOSE # ⍉


    NOT
    AND
    OR
    LT
    LE
    EQ
    GT
    GE
    NE
    SELECT


And a few operators:

    MAP
    REDUCE
    INNER
    OUTER

