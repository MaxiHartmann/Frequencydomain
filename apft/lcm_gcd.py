import numpy as np



def lcm_float(a, b, precision=10):
    a = round(a, precision)
    b = round(b, precision)
    return np.lcm(int(a * 10**precision), int(b * 10**precision)) / 10**precision


def lcm_of_list(x):
    lcm = lcm_float(x[0], x[1])

    if len(x) > 2:
        for v in x:
            lcm = lcm_float(v, lcm)
            
    return lcm

def gcd_float(a, b, precision=10):
    a = round(a, precision)
    b = round(b, precision)
    return np.gcd(int(a * 10**precision), int(b * 10**precision)) / 10**precision

def gcd_of_list(x):
    gcd = gcd_float(x[0], x[1])

    if len(x) > 2:
        for v in x:
            gcd = gcd_float(v, gcd)
            
    return gcd

A = np.array([1, 2, 1.5, 10])
A = np.array([913.585, 20000/60 * 16])

print(f"   A = {A}")
print(f" lcm = {lcm_of_list(A):.8e}")
print(f" gcd = {gcd_of_list(A):.8e}")
