import numpy as np

# 给定实对称矩阵 A
A = np.array([[0, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 0]])
B = np.array([[0, 1, 1, 1], [1, 0, 1, 0], [1, 1, 0, 1], [1, 0, 1, 0]])


# 计算 A 的特征值和特征向量
def create_Q(A):

    eigenvalues, eigenvectors = np.linalg.eig(A)
    # n = 4
    print(eigenvalues)
    # # 输出特征向量
    # print("\n特征向量:")
    # for i in range(n):
    #     print(f"特征值 {eigenvalues[i]} 对应的特征向量:")
    #     # 第 i 个特征向量
    #     eigenvector = eigenvectors[:, i]
    #     print(eigenvector)
    #     print(np.dot(A, eigenvector.T))
    #     print(eigenvalues[i] * eigenvectors[:, i])
    #     print()  # 空行分隔每个特征向量

    # 构建对角矩阵
    E = np.diag(eigenvalues)

    # 构建正交矩阵 Q
    Q = eigenvectors
    return Q


Q1 = create_Q(A)
Q2 = create_Q(B)
Q1_inv = np.linalg.inv(Q1)
Q = np.dot(Q2, Q1_inv)
print(Q)
