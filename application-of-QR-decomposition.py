import sympy as sp
def eigenvalues_compute(A):
    lam = sp.symbols('lambda')
    A = sp.Matrix(A)
    I = sp.eye(A.shape[0])
    equation = (A - lam*I).det()
    eigenvalues = sp.solve(equation, lam)
    return eigenvalues

