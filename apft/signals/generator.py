import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def float_gcd(a, b, rtol = 1e-05, atol = 1e-08):
    t = min(abs(a), abs(b))
    while abs(b) > rtol * t + atol:
        a, b = b, a % b
    return a

def lowest_common_multiple(list_of_numbers):

    if len(list_of_numbers) > 1:
        for x in list_of_numbers:

    else:
        print("Need at least two numbers!")




freqs = np.array([913.585, 5333.333333333, 1.01])
freqs = np.array([1, 1.5]) ## -> lcm=3
amps = [1.0, 0.5, 0.1]
phases = [0, 0, 0]

fmin = freqs.min()
fbase = fmin

for i, f in enumerate(freqs):
    a = fbase
    b = f
    gcd = float_gcd(a, b)
    lcm = abs(a * b) / gcd
    fbase = min(fbase, gcd)
    fbase = min(fbase, gcd)
    
    print(f"check for f={f}hz -> gcd({a}, {b})= {gcd}, lcm = {lcm}")

fmax = freqs.max()

samples_for_highest_freq = 10
fs = fmax * samples_for_highest_freq
periods = 1
dt = 1 / fs

t = np.arange(0, 1/fmin * periods, dt)

x = t * 0

for i, f in enumerate(freqs):
    x += np.real(amps[i] * np.exp(2j * f * np.pi * t))

# print(f"dt={dt:.3e}, fs={fs}hz, periods={periods}, samples={len(t)}")
# plt.plot(t, x, '.-')
# plt.show()



