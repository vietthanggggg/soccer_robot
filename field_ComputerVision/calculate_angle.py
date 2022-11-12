import math

A=(100,100)
B = (200,200)
C = [200,200]
lenAB = math.sqrt(math.pow(A[0]-B[0],2.0)+math.pow(A[1]-B[1],2.0))

C[0] = int(A[0]+(A[0]-B[0])/lenAB*50)
C[1] = int(A[1]+(A[1]-B[1])/lenAB*50)
print(C[0])
print(C[1])