import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import matplotlib.patches as mpatches
import csv
from matplotlib import rcParams
sns.set_style("ticks")

rcParams['axes.labelsize'] = 22
rcParams['axes.titlesize'] = 22
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
rcParams['legend.fontsize'] = 22
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Computer Modern Roman']
rcParams['text.usetex'] = True
rcParams['figure.figsize'] = 6.8, 5.0


### model parameters
startyear = 2014
startmonth = 3
startday = 2
days = 1

### import data from files
periodlength = 365
dataIB = np.genfromtxt('export.csv', delimiter = ',');

###Times array
t_start = datetime.datetime(startyear, startmonth, startday)
t_end = t_start + datetime.timedelta(minutes=(60*24*days))
t = np.array([t_start + datetime.timedelta(minutes=i) for i in xrange(60*24*periodlength)])

### Plot prices in selected time window


#ramp up imbalance volumes
dataAPX = np.genfromtxt('pricesold.txt', delimiter = ' ');
dataAPX = np.repeat(dataAPX,60)
apx = plt.plot(t[60*24*(31+28+3):60*24*(31+28+4)], dataAPX[(60*24*3):60*24*4], lw=2.0)
RDv = plt.plot(t[60*24*(31+28+3):60*24*(31+28+4)], dataIB[(60*24*(31+28+3)):60*24*(31+28+4),4]+dataIB[(60*24*(31+28+3)):60*24*(31+28+4),6], c='r', lw=2.0)
sns.despine()
plt.ylabel('Euro / MWh')
plt.xlabel('Time (Hours:Min:Sec)')
plt.legend(['APX', 'Imbalance'])
# plt.gca().set_xticks(range(0,1440,60))
# a = time_leg[0:97:8]
# a.append('24:00')
# plt.gca().set_xticklabels(a)
plt.setp( plt.gca().xaxis.get_majorticklabels(), rotation=70)
plt.savefig('foo.pdf', bbox_inches='tight')
plt.show()
