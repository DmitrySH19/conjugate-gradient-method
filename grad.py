import numpy as np
from numpy import linalg as LA

def is_pos_def(x):
    """check if a matrix is symmetric positive definite"""
    return np.all(np.linalg.eigvals(x) > 0)

A = np.array([[4, -61, -30, -63, 24],
              [-61, -63, -73, -23, -5],
              [-30, -73, -53, -48, -33],
              [-63, -23, -48, 49, 57],
              [24, -5, -33, 57, -57],])
print(is_pos_def(A))
print(is_pos_def((A.T).dot(A)))
b = np.array([95, -9, -22, 95, 0])
x = np.array([1.52794,-1.58395, -0.190674,0.894288,1.78696])

print(A.dot(x))





a = A
A = (A.T).dot(A)
b = (a.T).dot(b)
print(A)
print(b)
print(A.dot(x))