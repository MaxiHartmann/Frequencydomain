import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


mean = 1000
amps = [150, 100, 75, 10, 1]
freqs = [745, 11920, 15205, 11175, 12067]

periods = 3
basefreq = 745
dt = 1 / (basefreq * 885)
time = np.arange(0, periods / basefreq, dt)

pressure = mean
for idx, a in enumerate(amps):
    pressure += a * np.sin(2 * np.pi * freqs[idx] * time)


fig, (ax1, ax2) = plt.subplots(2)

ax1.plot(time, pressure)


ax2.plot(freqs, amps, linestyle='None', marker='.')
N = len(pressure)
x = np.fft.rfftfreq(N, d=dt)
y = np.abs(np.fft.rfft(pressure) / N * 2)
ax2.plot(x, y)
ax2.set_xlim(0, 20000)
ax2.set_ylim(0, 150)


plt.show()
