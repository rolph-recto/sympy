from sympy.core.sympify import _sympify
from sympy.core import S, Basic

from sympy.matrices.expressions.matexpr import ShapeError
from sympy.matrices.expressions.matpow import MatPow


class Inverse(MatPow):
    """
    The multiplicative inverse of a matrix expression

    This is a symbolic object that simply stores its argument without
    evaluating it. To actually compute the inverse, use the ``.inverse()``
    method of matrices.

    Examples
    ========

    >>> from sympy import MatrixSymbol, Inverse
    >>> A = MatrixSymbol('A', 3, 3)
    >>> B = MatrixSymbol('B', 3, 3)
    >>> Inverse(A)
    A^-1
    >>> A.inverse() == Inverse(A)
    True
    >>> (A*B).inverse()
    B^-1*A^-1
    >>> Inverse(A*B)
    (A*B)^-1

    """
    is_Inverse = True
    exp = S(-1)

    def __new__(cls, mat):
        mat = _sympify(mat)
        assert mat.is_Matrix
        if not mat.is_square:
            raise ShapeError("Inverse of non-square matrix %s" % mat)
        return Basic.__new__(cls, mat)

    @property
    def arg(self):
        return self.args[0]

    @property
    def shape(self):
        return self.arg.shape

    def _eval_inverse(self):
        return self.arg

    def _eval_determinant(self):
        from sympy.matrices.expressions.determinant import det
        return 1/det(self.arg)

    def doit(self, **hints):
        if hints.get('deep', True):
            return self.arg.doit(**hints).inverse()
        else:
            return self.arg.inverse()
