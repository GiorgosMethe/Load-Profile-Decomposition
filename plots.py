import lpd
import extra
import random
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import matplotlib.patches as mpatches
import csv
sns.set_style("ticks")

time_hour = [str(i).zfill(2)  for i in range(0,24)]
time_mini = [str(i).zfill(2)  for i in range(0,60,15)]
time_leg = [hour + ":" + mini for hour in time_hour for mini in time_mini]

rcParams['axes.labelsize'] = 22
rcParams['axes.titlesize'] = 22
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
rcParams['legend.fontsize'] = 22
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Computer Modern Roman']
rcParams['text.usetex'] = True
rcParams['figure.figsize'] = 6.8, 5.0

"""
Main function of test python module
"""
def main():
    random.seed(os.urandom(967)) # initialize random generator
    t = np.linspace(0.0, 24.0, 96.0) # define the time axis of a day, here we use 96 values every quarter of an hour
    #standard load profile -- input
    q = extra.read_slp(t, 'Profielen-Elektriciteit-2015-versie-1.00 Folder/profielen Elektriciteit 2015 versie 1.00.csv') # read the sample standard load profile, can be any length, can be resized given a low/high resolution time axis
    q = q / np.sum(q) # normalization of standard load profile
    # process duration
    duration_axis = np.linspace(0.0, 24.0, 96.0)
    (p_d, E_p) = extra.app_time(duration_axis, 10, 2, 0.0, 24.0) # function that define the pdf of duration of a process
    # process consumption
    consumption_axis = np.linspace(0.0, 3.5, 96.0)
    (p_k, E_k) = extra.app_consumption(consumption_axis, 10, 2, 0.0, 3.5) # function that define the pdf of duration of a process
    # pdf of starting time
    p_t_0 = lpd.infer_t_0(q, p_d, E_k) # computes the pdf of starting time of processes
    p_t_0 = p_t_0 / np.sum(p_t_0) # normalization of the pdf to sum up to zero

    """
    1st Approach, starting time of processes is a discrete propapibility density function
    """
    # synthetic profile of D processes
    D = 1
    slp = lpd.synthetic_profile(0, t, p_d, consumption_axis, p_k, p_t_0)
    for k in range(0,7):
        D = 10**k
        slp = lpd.synthetic_profile(D, t, p_d, consumption_axis, p_k, p_t_0)
        # expected value of D processes
        q_e_e = lpd.infer_q_e(t, p_t_0, p_d, E_k, D)
        # plot
        plt.figure()
        # legends = []
        # plt.fill_between(t, slp, q_e_e, where=slp>=q_e_e, facecolor=sns.color_palette()[2], interpolate=True)
        # plt.fill_between(t, slp, q_e_e, where=slp<q_e_e, facecolor=sns.color_palette()[0], interpolate=True)
        # legends.append(mpatches.Patch(edgecolor='k',facecolor=sns.color_palette()[2], label='Shortage'))
        # legends.append(mpatches.Patch(edgecolor='k',facecolor=sns.color_palette()[0], label='Excess'))
        # plt.legend(handles=legends, loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.4))
        plt.title('D = ' + str(D))
        plt.plot(t, q_e_e, color='k', ls='--', lw=1)
        plt.plot(t, slp, lw=2)
        plt.gca().set_xticks(range(0,25,8))
        sns.despine()
        plt.ylabel('Load (kW)')
        plt.xlabel('Time (Hours:Min)')
        plt.xlim(0.0, 24.0)
        plt.gca().set_xticks(range(0,25,2))
        a = time_leg[0:97:8]
        a.append('24:00')
        plt.gca().set_xticklabels(a)
        plt.setp( plt.gca().xaxis.get_majorticklabels(), rotation=70)
        plt.savefig('foo_'+str(D).zfill(4)+".png", bbox_inches='tight')
        plt.close()
        # plt.savefig('slp_shortage.pdf', bbox_inches = 'tight', pad_inches = 0)
        # plt.show()


if __name__ == "__main__":
    main()
