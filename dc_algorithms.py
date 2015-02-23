# -*- coding: utf-8 -*-
from numpy import *  # analysis:ignore
import numpy

'''
    Divide and conquer algorithms on arrays and matrices.
    Basic operations done on a matrix as well as strassens for
    square matrix multiplication.
    @author Bailey Ammons
'''


# STOCK_PRICES  = [100,113,110,85,105,102,86,63,81,101,94,106,101,79,94,90,97]
STOCK_PRICE_CHANGES = [13, -3, -25, 20, -3, -16, -23, 18, 20,
                       -7, 12, -5, -22, 15, -4, 7]
TEST_MATRIX = matrix([[1, 2, 3, 5, 1, 3, 98, 47],
                      [4, 5, 2, 1, 2, 7, 51, 63],
                      [4, 5, 2, 1, 9, 19, 29, 17],
                      [4, 5, 2, 1, 21, 1, 33, 12],
                      [12, 1, 4, 8, 9, 3, 19, 21],
                      [4, 5, 21, 31, 9, 8, 42, 33],
                      [21, 4, 7, 12, 33, 21, 12, 15],
                      [1, 3, 4, 5, 7, 9, 1, 5]])
TEST_S_MATRIX = matrix([[2, 2], [4, 4]])


def find_maximum_subarray_brute(A, low=0, high=-1):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Implement the brute force method from chapter 4
    time complexity = O(n^2)

    >>> (find_maximum_subarray_brute(STOCK_PRICE_CHANGES))
    (7, 10)

    >>> (find_maximum_subarray_brute(STOCK_PRICE_CHANGES, 2, 9))
    (7, 8)

    >>> (find_maximum_subarray_brute(STOCK_PRICE_CHANGES, 1, 1))
    (1, 1)
    """
    max_left = low
    max_right = low
    total = A[low]
    temp_total = 0
    set_total = 0

    if high == -1:
        high = len(A) - 1

    for i in range(low, high):
        temp_right = i
        temp_total = A[i]
        set_total = A[i]
        for j in range(i + 1, high):
            set_total += A[j]
            if temp_total <= set_total:
                temp_right = j
                temp_total = set_total
        if temp_total >= total:
            max_left = i
            max_right = temp_right
            total = temp_total
    return (max_left, max_right)


def find_maximum_crossing_subarray(A, low, mid, high):
    """
    Find the maximum subarray that crosses mid
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    """
    left_sum = A[mid]
    total_sum = 0
    max_left = mid
    max_right = mid + 1

    for i in range(mid, low, -1):
        total_sum += A[i]
        if total_sum > left_sum:
            left_sum = total_sum
            max_left = i

    right_sum = A[high]
    total_sum = 0

    for j in range(mid + 1, high):
        total_sum += A[j]
        if total_sum > right_sum:
            right_sum = total_sum
            max_right = j

    total_sum = right_sum + left_sum  # we need this
    return (max_left, max_right, total_sum)


def find_maximum_subarray_recursive(A, low=0, high=-1):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Recursive method from chapter 4

    >>> (find_maximum_subarray_recursive(STOCK_PRICE_CHANGES))
    (7, 10, 43)
    >>> (find_maximum_subarray_recursive(STOCK_PRICE_CHANGES, 2, 9))
    (7, 8, 38)
    >>> (find_maximum_subarray_recursive(STOCK_PRICE_CHANGES, 1, 1))
    (1, 1, -3)
    """
    if high == low:
        return (low, high, A[low])
    else:
        if high == -1:
            high = len(A) - 1
        mid = int(math.floor((low + high) / 2))
        left_sub = find_maximum_subarray_recursive(A, low, mid)
        right_sub = find_maximum_subarray_recursive(A, mid + 1, high)
        cross_sub = find_maximum_crossing_subarray(A, low, mid, high)

        if left_sub[2] >= right_sub[2] and left_sub[2] >= cross_sub[2]:
            return left_sub
        elif right_sub[2] >= left_sub[2] and right_sub[2] >= cross_sub[2]:
            return right_sub
        else:
            return cross_sub


def find_maximum_subarray_iterative(A, low=0, high=-1):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Do problem 4.1-5 from the book.

    >>> (find_maximum_subarray_iterative(STOCK_PRICE_CHANGES))
    (7, 10)

    >>> (find_maximum_subarray_iterative(STOCK_PRICE_CHANGES, 2, 9))
    (7, 8)

    >>> (find_maximum_subarray_iterative(STOCK_PRICE_CHANGES, 1, 1))
    (1, 1)
    """
    cur_max = A[low]
    total_max = A[low]
    best_left = low
    best_right = low

    if high == -1:
        high = len(A) - 1

    if high == low:
        return (low, high)
    else:
        for i in range(low + 1, high):
            if cur_max < 0:
                cur_max = A[i]
                best_left_temp = i
            else:
                cur_max += A[i]

            if cur_max >= total_max:
                total_max = cur_max
                best_left = best_left_temp
                best_right = i

        return (best_left, best_right)


def square_matrix_multiply(A, B):
    """
    Return the product AB of matrix multiplication.

    >>> (square_matrix_multiply(TEST_MATRIX, TEST_MATRIX))
    matrix([[2170,  601,  964, 1527, 3736, 2587, 1820, 2109],
            [1222,  478,  792, 1188, 2258, 1786, 1745, 1902],
            [ 846,  319,  734, 1122, 1381, 1027, 2072, 1885],
            [ 997,  242,  412,  683, 1424,  958, 1587, 1578],
            [ 604,  252,  378,  571, 1100,  766, 2153, 1469],
            [1287,  609,  756, 1066, 2624, 1747, 3323, 2480],
            [ 860,  388,  826, 1262, 1331,  890, 4529, 3143],
            [ 195,  133,  271,  389,  360,  264, 1060,  848]])

    >>> (square_matrix_multiply(TEST_S_MATRIX, TEST_S_MATRIX))
    matrix([[12, 12],
            [24, 24]])
    """
    A = asarray(A)
    B = asarray(B)
    assert A.shape == B.shape
    assert A.shape == A.T.shape

    rows = len(A)
    C = zeros((rows, rows), dtype=int)
    for i in range(0, rows):
        for j in range(0, rows):
            C[i][j] = 0
            for k in range(0, rows):
                C[i][j] += A[i][k] * B[k][j]

    return matrix(C)


def square_matrix_multiply_strassens(A, B):
    """
    Return the product AB of matrix multiplication.
    Assume len(A) is a power of 2

    >>> (square_matrix_multiply_strassens(TEST_MATRIX, TEST_MATRIX))
    array([[2170,  601,  964, 1527, 3736, 2587, 1820, 2109],
           [1222,  478,  792, 1188, 2258, 1786, 1745, 1902],
           [ 846,  319,  734, 1122, 1381, 1027, 2072, 1885],
           [ 997,  242,  412,  683, 1424,  958, 1587, 1578],
           [ 604,  252,  378,  571, 1100,  766, 2153, 1469],
           [1287,  609,  756, 1066, 2624, 1747, 3323, 2480],
           [ 860,  388,  826, 1262, 1331,  890, 4529, 3143],
           [ 195,  133,  271,  389,  360,  264, 1060,  848]])

    >>> (square_matrix_multiply_strassens(TEST_S_MATRIX, TEST_S_MATRIX))
    array([[12, 12],
           [24, 24]])
    """
    A = asarray(A)
    B = asarray(B)
    assert A.shape == B.shape
    assert A.shape == A.T.shape
    assert (len(A) & (len(A) - 1)) == 0, "A is not a power of 2"

    rows = len(A)
    half = len(A) / 2

    if rows < 2:
        return square_matrix_multiply(matrix(A), matrix(B))

    a11 = zeros((half, half), dtype=int)
    a12 = zeros((half, half), dtype=int)
    a21 = zeros((half, half), dtype=int)
    a22 = zeros((half, half), dtype=int)

    b11 = zeros((half, half), dtype=int)
    b12 = zeros((half, half), dtype=int)
    b21 = zeros((half, half), dtype=int)
    b22 = zeros((half, half), dtype=int)

    result_a = zeros((half, half), dtype=int)
    result_b = zeros((half, half), dtype=int)

    for i in range(0, half):
        for j in range(0, half):
            a11[i][j] = A[i][j]
            a12[i][j] = A[i][j + half]
            a21[i][j] = A[i + half][j]
            a22[i][j] = A[i + half][j + half]

            b11[i][j] = B[i][j]
            b12[i][j] = B[i][j + half]
            b21[i][j] = B[i + half][j]
            b22[i][j] = B[i + half][j + half]

    # p1 = (a11+a22) * (b11+b22)
    result_a = add(a11, a22)
    result_b = add(b11, b22)
    p1 = square_matrix_multiply_strassens(matrix(result_a), matrix(result_b))

    # p2 = (a21+a22) * (b11)
    result_a = add(a21, a22)
    p2 = square_matrix_multiply_strassens(matrix(result_a), matrix(b11))

    # p3 = (a11) * (b12 - b22)
    result_b = subtract(b12, b22)
    p3 = square_matrix_multiply_strassens(matrix(a11), matrix(result_b))

    # p4 = (a22) * (b21 - b11)
    result_b = subtract(b21, b11)
    p4 = square_matrix_multiply_strassens(matrix(a22), matrix(result_b))

    # p5 = (a11+a12) * (b22)
    result_a = add(a11, a12)
    p5 = square_matrix_multiply_strassens(matrix(result_a), matrix(b22))

    # p6 = (a21-a11) * (b11+b12)
    result_a = subtract(a21, a11)
    result_b = add(b11, b12)
    p6 = square_matrix_multiply_strassens(matrix(result_a), matrix(result_b))

    # p7 = (a12-a22) * (b21+b22)
    result_a = subtract(a12, a22)
    result_b = add(b21, b22)
    p7 = square_matrix_multiply_strassens(matrix(result_a), matrix(result_b))

    # c12 = p3 + p5
    c12 = asarray(add(p3, p5))
    # c21 = p2 + p4
    c21 = asarray(add(p2, p4))

    # c11 = p1 + p4 - p5 + p7
    result_a = add(p1, p4)
    result_b = add(result_a, p7)
    c11 = asarray(subtract(result_b, p5))

    # c22 = p1 + p3 - p2 + p6
    result_a = add(p1, p3)
    result_b = add(result_a, p6)
    c22 = asarray(subtract(result_b, p2))

    C = zeros((rows, rows), dtype=int)

    for i in range(0, half):
        for j in range(0, half):
            C[i][j] = c11[i][j]
            C[i][j + half] = c12[i][j]
            C[i + half][j] = c21[i][j]
            C[i + half][j + half] = c22[i][j]
    return C


def test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    test()
