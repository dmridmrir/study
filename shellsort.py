import numpy as np
a = 10 * np.random.rand(10)
a =  a.astype(int)

def insertionsort(L):
    n = len(L)
    for i in range(1,n-1):
        key = L[i]
        for j in range(i + 1):
            if key < L[i]:
                L[j+1:i+2] = L[j:i+1]
                L[j] = key
                break
    return L
def shellsort(L):
    n = len(L)
    gap = n//2
    while gap >=1: 
        for i in range(gap):
            t = L[i:n:gap]
            insertionsort(t)
    gap = gap//2
    return L