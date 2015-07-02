import lpd
import random
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import f


"""
Defines the distribution of duration of a process
"""
def app_time(x, dfn, dfd, a, b):
    mean = 0.0
    dist = np.divide(f.pdf(x, dfn, dfd), (f.cdf(b, dfn, dfd) - f.cdf(a, dfn, dfd))) # f-dist for duration, truncated from a to b
    dist = np.divide(dist, np.sum(dist)) # normalization

    for item in zip(x, dist): mean = mean + (item[0] * item[1]) # expectation of duration

    return dist, mean

"""
Defines the distribution of consumption rate
"""
def app_consumption(x, dfn, dfd, a, b):
    mean = 0.0
    dist = np.divide(f.pdf(x, dfn, dfd, scale=0.1), (f.cdf(b, dfn, dfd, scale=0.1) - f.cdf(a, dfn, dfd, scale=0.1))) # f-dist for duration, truncated from a to b
    dist = np.divide(dist, np.sum(dist)) # normalization

    for item in zip(x, dist): mean = mean + (item[0] * item[1]) # expectation of consumption

    return dist, mean

"""
Reads a standard load profile and resize it to the desired length
"""
def read_slp(t, file):
    original_signal = np.genfromtxt(file ,delimiter=',')
    original_signal = original_signal[np.arange(0, len(original_signal))]
    new_signal = np.zeros(len(t))
    new_signal = lpd.upsample(original_signal, new_signal)
    return new_signal


"""
Main function of test python module
"""
def main():
    random.seed(os.urandom(967)) # initialize random generator
    t = np.linspace(0.0, 24.0, 96.0) # define the time axis of a day, here we use 96 values every quarter of an hour
    #standard load profile -- input
    q = 0.01 * np.ones(len(t)) + read_slp(t, 'sample_slp.csv') # read the sample standard load profile, can be any length, can be resized given a low/high resolution time axis
    q = q / np.sum(q) # normalization of standard load profile
    # process duration
    duration_axis = np.linspace(0.0, 24.0, 96.0)
    (p_d, E_p) = app_time(duration_axis, 10, 2, 0.0, 24.0) # function that define the pdf of duration of a process
    # process consumption
    consumption_axis = np.linspace(0.0, 3.5, 96.0)
    (p_k, E_k) = app_consumption(consumption_axis, 10, 2, 0.0, 3.5) # function that define the pdf of duration of a process
    # pdf of starting time
    p_t_0 = lpd.infer_t_0(q, p_d, E_k) # computes the pdf of starting time of processes
    p_t_0 = p_t_0 / np.sum(p_t_0) # normalization of the pdf to sum up to zero

    """
    1st Approach, starting time of processes is a discrete propapibility density function
    """
    # synthetic profile of D processes
    D = 2000
    synthetic_profile = lpd.synthetic_profile(D, t, p_d, consumption_axis, p_k, p_t_0)
    # expected value of D processes
    q_e_e = lpd.infer_q_e(t, p_t_0, p_d, E_k, D)
    # plot
    plt.step(t, synthetic_profile, "g-")
    plt.step(t, q_e_e, "b--")

    """
    2nd Approach, starting time of processes is a discrete propapibility density function
    """
    # synthetic profile of D processes
    ts, cs = lpd.continous_synthetic_profile(D, t, p_d, consumption_axis, p_k, p_t_0)
    plt.step(ts/len(t)*t[-1], cs, where='post', c='r')
    plt.xlim(0,24.0)
    plt.legend(["synthetic","expected", "continuous"],loc=0)
    plt.show()

    """
    Time discretization
    """
    n_intervals = 8
    discrete_timeaxis = np.linspace(0.0, 24.0, n_intervals+1)
    discrete_consumption = lpd.signal_discretization(discrete_timeaxis, t, ts, cs)
    plt.step(ts/len(t)*t[-1], cs, where='post', c='r')
    plt.step(discrete_timeaxis, discrete_consumption, where='post', c='k', ls='--',lw=2)
    plt.legend(["continuous", "discretized"],loc=0)
    plt.show()


if __name__ == "__main__":
    main()
