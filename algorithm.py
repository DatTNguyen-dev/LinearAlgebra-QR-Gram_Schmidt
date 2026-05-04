import numpy as np
import pandas as pd

def qr_demcomposition(A):
    m, n = A.shape
    Q = np.zeros((m, n))
    R = np.zeros((n, n))

    for j in range(n):
        v = A[:, j]
        for i in range(j):
            R[i, j] = np.dot(Q[:, i], A[:, j])
            v = v - R[i, j] * Q[:, i]
        R[j, j] = np.linalg.norm(v)
        Q[:, j] = v / R[j, j]

    return Q, R

def solve_linear_system(Q, R, b):
    y = np.dot(Q.T, b)
    n = R.shape[0]
    x = np.zeros(n)

    for i in reversed(range(n)):
        x[i] = (y[i] - np.dot(R[i, i+1:], x[i+1:])) / R[i, i]

    return x

def eigenvalues(A, iterations = 100, tolerance=1e-10):
    A_k = A.astype(float)

    for _ in range(iterations):
        Q, R = qr_demcomposition(A_k)
        A_k = R @ Q

        off_diag = A_k - np.diag(np.diag(A_k))
        if np.linalg.norm(off_diag) < tolerance:
            break

    return np.diag(A_k)