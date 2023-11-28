import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


freqs = [5, 10, 15, 20]
fbase = 5
samples = 100
fs = fbase * samples
dt = 1 / fs

time = np.arange(0, 1/fbase, dt)

### create matrix A dim m x n
m = len(time)
n = len(freqs)

first_column = np.full(shape=m, fill_value=1)

A = first_column
# A = np.c_[A, first_column * 0]
# print(A)

for f in freqs:
    real = np.cos(2 * np.pi * f * time)
    imag = np.sin(2 * np.pi * f * time)
    A = np.c_[A, real, imag]

# A = A[:,1:]

condition = np.linalg.cond(A)
print(f"A.shape: {A.shape}")
print(f"condition: {condition:.4f}")



#### Complex matrix
freqs = np.asarray([freqs])
# freqs = np.append(0, freqs)
time = np.asarray([time]).transpose()
A = np.exp(-2j * np.pi * freqs * time)

condition = np.linalg.cond(A)
print(f"A.shape: {A.shape}")
print(f"condition: {condition:.4f}")
