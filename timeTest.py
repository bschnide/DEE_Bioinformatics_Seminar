#!/home/boris/anaconda3/bin/python3
# -*- coding: utf-8 -*-

"""
Compares a CPU-bound process running time with a for loop, with multiprocessing
and with multithreading. Then compares the same CPU-bound process running time
with a different number of processes running in parallel. Subsequently, the running
time of an I/O-bound process (requesting data from a website) is compared when
using a for loop, multiple processes, multiple threads and multiple threads in
multiple processes. Finally, different number of threads are used for the same
I/O-bound process. At the end of each execution, a barplot is generated with the
running times.

Note that if you want to run this program quickly, you should reduce
the number of simulations here and also change the division factor accordingly:
e.g.: "...number=100)/100" => "number=10)/10"

Note also that before running this code, you should change the number of cores
the program should use according to the number of cores you computer has:
in ProcessorBoundProcess.py, change "nbCores=8" value is the easiest way to do so.
Then you should also specify in this script the maximum number of cores you want
to give in the part of the code that tries different numbers of processes (2nd part
which goes from 1 to 8 here (range(1,9)) ).

In case you do not want to change the number of cores and that the programs asks
for more cores than available, the process may just be slower than expected or
make your computer freeze.

Created on Wed Apr 18 11:11:11 2018

@author: boris
"""

import timeit
import os
from matplotlib import pyplot as plt
import math

#WORKING DIRECTORY TO BE CHANGED IF YOU WANT THE PROGRAM TO WORK
os.chdir("/home/boris/Documents/DEESeminar")
#COMMENT THE LINE ABOVE AND UNCOMMENT THE LINES BELOW IF YOU WANT TO SPECIFY THE
#PATH IN THE TERMINAL
#import sys
#os.chdir(sys.argv[0])

# ################################################################################
#Test CPU-bound process speed

loop2 = timeit.timeit("randFileGen = makeHugeRandomFiles(); randFileGen.SimpleCycle()", setup="from ProcessorBoundProcess import makeHugeRandomFiles", number=100)/100
Pro2 = timeit.timeit("randFileGen = makeHugeRandomFiles(); randFileGen.MultiProcessingProcess()", setup="from ProcessorBoundProcess import makeHugeRandomFiles", number=100)/100
Thread2 = timeit.timeit("randFileGen = makeHugeRandomFiles(); randFileGen.MultithreadForDummy(nbThreads=12)", setup="from ProcessorBoundProcess import makeHugeRandomFiles", number=100)/100

print("""Time to generate the random sequence files with:\n\
    for loop: {}\n\
    Multiprocessing: {}\n\
    Multithreading: {}""".format(loop2, Pro2, Thread2))

listProcesses = [loop2, Pro2, Thread2]
processNames = ["Loop", "Multiprocessing", "Multithreading"]
x_pos = range((len(listProcesses)))#This will be to keep the bar order, we replace
#the names by values

col1 = (23/255, 190/255, 207/255)

fig, ax = plt.subplots(1, 1)
ax.set_facecolor((220/255, 230/255, 230/255)) # set background color

ax.bar(x_pos, listProcesses, color=col1, align='center', alpha=0.7)
plt.title('Speed of CPU-bound process run')
plt.ylabel('time (s)')

#values on the bars
for i, v in enumerate(listProcesses):
    ax.text(i-0.15, v+0.1, str(round(v, 2)), fontweight='bold')
plt.xticks(x_pos, processNames, fontsize=9) # we replace the values by tick names
plt.grid('on', linestyle='--')

plt.savefig('CPU-boundProcess.pdf')
plt.clf()

# ################################################################################
#Test CPU-bound process speed with different number of processes
Thread4 = []
processNames = []

for nbCores in range(1,9): # varying the nb of cores
    Thread4.append(timeit.timeit("randFileGen = makeHugeRandomFiles(); randFileGen.MultiProcessingProcess(nbCores={})".format(nbCores), setup="from ProcessorBoundProcess import makeHugeRandomFiles", number=100)/100)
    processNames.append("{}\nCore(s)".format(nbCores))

x_pos = range((len(Thread4)))#This will be to keep the bar order, we replace
#the names by values

col1 = (23/255, 190/255, 207/255)

fig, ax = plt.subplots(1, 1)
ax.set_facecolor((220/255, 230/255, 230/255)) # set background color

ax.bar(x_pos, Thread4, color=col1, align='center', alpha=0.7)
plt.title('Speed of CPU-bound process run with different numbers of processes')
plt.ylabel('time (s)')

#values on the bars
for i, v in enumerate(Thread4):
    ax.text(i-0.3, v+0.1, str(round(v, 2)), fontweight='bold')
plt.xticks(x_pos, processNames, fontsize=9) # we replace the values by tick names
plt.grid('on', linestyle='--')

plt.savefig('VaryingCores.pdf')
plt.clf()

################################################################################
#Test I/O-bound process speed

loop = timeit.timeit("URLGet = urlGetDifferentProcesses(); URLGet.loopGet(urls)", setup="from urllibGetFiles import urlGetDifferentProcesses, urls", number=100)/100
Pro = timeit.timeit("URLGet = urlGetDifferentProcesses(); URLGet.prepareList(urls); URLGet.multiProcessingGet()", setup="from urllibGetFiles import urlGetDifferentProcesses, urls", number=100)/100
Thread = timeit.timeit("URLGet = urlGetDifferentProcesses(20); URLGet.prepareList(urls); URLGet.threadingGet()", setup="from urllibGetFiles import urlGetDifferentProcesses, urls", number=100)/100
ProThread = timeit.timeit("URLGet = urlGetDifferentProcesses(5); URLGet.prepareList(urls); URLGet.make2ElemLists(); URLGet.multiProcessingAndThreading()", setup="from urllibGetFiles import urlGetDifferentProcesses, urls", number=100)/100

print("""Time to get 20 web pages with:\n\
    for loop: {}\n\
    Multiprocessing: {}\n\
    Multithreading: {}\n\
    Multithreading nested in multiprocessing: {}""".format(loop, Pro, Thread, ProThread))

listProcesses = [loop, Pro, Thread, ProThread]
processNames = ["Loop", "Multiprocessing", "Multithreading", "Multiprocessing\n&\nMultithreading"]
x_pos = range((len(listProcesses)))#This will be to keep the bar order, we replace
#the names by values

col1 = (23/255, 190/255, 207/255)

fig, ax = plt.subplots(1, 1)
ax.set_facecolor((220/255, 230/255, 230/255)) # set background color

ax.bar(x_pos, listProcesses, color=col1, align='center', alpha=0.7)
plt.title('Speed of I/O-bound process run')
plt.ylabel('time (s)')

#values on the bars
for i, v in enumerate(listProcesses):
    ax.text(i-0.15, v+0.1, str(round(v, 2)), fontweight='bold')
plt.xticks(x_pos, processNames, fontsize=9)#we replace the values by tick names
plt.grid('on', linestyle='--')

plt.savefig('URLGet.pdf')
plt.clf()

################################################################################
#Test I/O-bound process speed with different number of threads
loop3 = timeit.timeit("URLGet = urlGetDifferentProcesses(); URLGet.loopGet(urls)", setup="from urllibGetFiles import urlGetDifferentProcesses, urls", number=100)/100
Thread3 = []
processNames = [""]

for nbThreads in range(1,50): # varying the nb of threads
    Thread3.append(timeit.timeit("URLGet = urlGetDifferentProcesses({}); URLGet.prepareList(urls); URLGet.threadingGet()".format(nbThreads), setup="from urllibGetFiles import urlGetDifferentProcesses, urls", number=100)/100)
    if nbThreads%5 == 0 or nbThreads%10 == 0 or nbThreads == 1:
        processNames.append("{}".format(nbThreads))
    else:
        processNames.append("") # number every 5 numbers
Thread3.insert(0, loop3) # insert the loop at the beginning

x_pos = range((len(Thread3)))#This will be to keep the bar order, we replace
#the names by values

col1 = (23/255, 190/255, 207/255)

fig, ax = plt.subplots(1, 1)
ax.set_facecolor((220/255, 230/255, 230/255)) # set background color

barlist1 = ax.bar(x_pos[0], Thread3[0], align='center', color=(255/255, 127/255, 14/255) , label="Simple loop")
barlist2 = ax.bar(x_pos[1:], Thread3[1:], align='center', color=col1 , label="Threading")


plt.title('Speed of I/O-bound process run with different numbers of threads')
plt.xlabel('Number of Threads')
plt.ylabel('time (s)')
plt.legend()

#values on the bars
plt.xticks(x_pos, processNames, fontsize=9) # we replace the values by tick names
plt.grid('on', linestyle='--')

plt.savefig('VaryingThreads.pdf')
plt.clf()
#POTENTIALLY ROTATE ONLY "LOOP"
