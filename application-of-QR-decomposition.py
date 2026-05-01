import numpy as np

# Gram-Schmidt QR
# cái hàm này là để chạy  dùng trong 2 cái ứng dụng ở dưới (*)
def gram_schmidt_qr(A):
    A = A.astype(float)
    m, n = A.shape

    Q = np.zeros((m, n))
    R = np.zeros((n, n)) 

    for j in range(n):
        v = A[:, j]

        for i in range(j):
            R[i, j] = np.dot(Q[:, i], A[:, j])
            v = v - R[i, j] * Q[:, i]

        R[j, j] = np.linalg.norm(v)

        if R[j, j] == 0:
            raise ValueError("Matrix has linearly dependent columns")

        Q[:, j] = v / R[j, j]

    return Q, R

# Solve linear system Ax=b

def solve_qr(A, b):
    Q, R = gram_schmidt_qr(A)                      #(*)

    # Compute Q^T b
    y = np.dot(Q.T, b)

    # Back substitution for Rx = y
    n = R.shape[0]
    x = np.zeros(n)

    for i in reversed(range(n)):
        x[i] = (y[i] - np.dot(R[i, i+1:], x[i+1:])) / R[i, i]

    return x

# QR Iteration for eigenvalues

def qr_eigenvalues(A, max_iters=100, tol=1e-8):
    A_k = A.astype(float)

    for _ in range(max_iters):
        Q, R = gram_schmidt_qr(A_k)
        A_k = R @ Q

        # Check convergence (off-diagonal small)
        off_diag = A_k - np.diag(np.diag(A_k))
        if np.linalg.norm(off_diag) < tol:
            break

    return np.diag(A_k)
