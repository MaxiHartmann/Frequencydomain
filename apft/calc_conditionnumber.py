import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calc_conditionnumber(time, freqs):
    m = len(time)
    n = len(freqs)

    # only real part for 0th harmonic
    first_column = np.full(shape=m, fill_value=1)

    A = first_column
    # append columns for real and imag part
    for f in freqs:
        real = np.cos(2 * np.pi * f * time)
        imag = np.sin(2 * np.pi * f * time)
        print(f)
        print(time)
        A = np.c_[A, real, imag]

    print(A)
    return np.linalg.cond(A)

def calc_conditionnumber_complex(time, freqs):
    #### Complex matrix
    freqs = np.asarray([freqs])
    time = np.asarray([time]).transpose()
    A = np.exp(-2j * np.pi * freqs * time)

    return np.linalg.cond(A)


def find_timevector_for_acceptable_condition(freqs):
    kappa_max = 2
    samples = 3
    freqs = np.asarray(freqs)
    fbase = np.min(freqs[np.nonzero(freqs)])

    fs = fbase * samples
    time = np.arange(0, 1 / fbase, 1 / fs)
    kappa = calc_conditionnumber(time, freqs)

    print(f"fbase={fbase}, samples={samples} --> condition = {kappa:.4f}")
    while kappa > kappa_max:
        samples += 1

        fs = fbase * samples
        dt = 1 / fs
        time = np.arange(0, 1 / fbase, dt)
        kappa = calc_conditionnumber(time, freqs)
        print(f"fbase={fbase}, samples={samples} --> condition = {kappa:.4f}")

    return time

def simple_example():
    freqs = [np.pi, 2]
    samples = 100
    fbase = 2
    fs = fbase * samples
    dt = 1 / fs

    time = np.arange(0, 1/fbase, dt)
    
    c = calc_conditionnumber(time, freqs)
    print(f"condition: {c:.4f}")

    c = calc_conditionnumber_complex(time, freqs)
    print(f"condition: {c:.4f}")

    return 0


def main():
    freqs = [0, 913.585, 419.78]
    t = find_timevector_for_acceptable_condition(freqs)
    print(t)
    time_fine = np.linspace(0, 1 / 419.78, 1000)

    for f in freqs:
        plt.plot(time_fine, np.sin(f * 2 * np.pi * time_fine), label=f"f={f}")
    # simple_example()

    plt.plot(t, np.sin(f * 2 * np.pi * t),  linestyle='None', marker='.', label='samples')
    plt.legend()

    plt.show()


if __name__ == "__main__":
    main()

