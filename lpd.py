import numpy as np
import random

"""
Linear interpolation upsampling
"""
def random_sample(distribution, size = 1):
    cdf = np.cumsum(distribution)
    random_ = np.random.uniform(size=size)
    samples = [np.where(cdf >= ran)[0][0] for ran in random_]
    return samples

"""
Linear interpolation upsampling
"""
def upsample(singal, new_signal):
    for i in range(len(singal)):
        new_pos = int(round((i)*(float(len(new_signal)-1) / float(len(singal) -1))))
        new_signal[new_pos] = singal[i]
        if (i > 0):
            prev_pos = int(round((i-1)*(float(len(new_signal)-1) / float(len(singal) -1))))
            for j in range(1, new_pos-prev_pos):
                new_prop = float(j) / (new_pos - prev_pos)
                prev_prop = 1.0 - new_prop
                new_signal[prev_pos + j] = (new_prop * new_signal[new_pos]) + (prev_prop * new_signal[prev_pos])
    return new_signal


"""
Linear interpolation upsampling
"""
def infer_q_e(t, p_t_0, p_d, E_k = 1.0, D = 1.0):

    P_bar_d = np.zeros(len(p_d)) # cumulative complementary distribution function
    for i in range(len(p_d)):
        P_bar_d[i] = np.sum(p_d[i:])

    q_e = np.zeros(len(t))
    for i in range(len(t)):
        sum_td = 0.0
        for j in range(len(t)):
            sum_td = sum_td + (p_t_0[j] * P_bar_d[i-j])
        q_e[i] = float(D) * E_k * sum_td
    return q_e

"""
Infers the starting time probability density function of a process

Solves the linear system of equation A x t_0 = B

A[0,0] = probability of starting process at timestep zero and have more than zero duration
A[0,1] = probability of starting process at timestep zero and have more than one duration
...
A[1,0] = probability of starting process at timestep one and have more than n duration
A[1,1] = probability of starting process at timestep zero and have more than zero duration

t_0 = pdf of starting time of process

B = standard load profile
"""
def infer_t_0(q, p_d, E_k):

    P_bar_d = np.zeros(len(p_d)) # cumulative complementary distribution function
    for i in range(len(p_d)):
        P_bar_d[i] = np.sum(p_d[i:])
        
    A = np.array([])
    B = np.ones(len(q))
    for i in range(len(q)):
        row = np.ones(len(q))
        for j in range(len(q)):
            row[j] = P_bar_d[i-j]
        if len(A) != 0:A = np.vstack((A,row))
        else:A = row
        B[i] = q[i]
    t_0 = np.linalg.solve(A, B)
    return t_0

"""
Linear interpolation upsampling
"""
def synthetic_profile(D, t, d, consumption, k, t_0):
    ds = random_sample(d, D)
    ks = random_sample(k, D)
    t_0s = random_sample(t_0, D)

    slp = np.zeros(len(t))
    for d in zip(ds, consumption[ks], t_0s):
        for time in range(d[2], d[2]+d[0]+1): # +1 because range(0,0) = ~, range(0,1) = 0
            if (time >= len(t)):
                slp[time - len(t)] = slp[time - len(t)] + d[1]
            else:
                slp[time] = slp[time] + d[1]
    return slp