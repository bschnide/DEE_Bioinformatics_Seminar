#!/home/boris/anaconda3/bin/python3
# -*- coding: utf-8 -*-

"""
DEE bioinformatics seminar presentation code.

Created on Wed Apr 18 11:11:11 2018

@author: boris
"""

import urllib.request
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool
import os

class urlGetDifferentProcesses:
    """
    Class that contains methods to get the html text of a page with a user-specified
    URL.
    """
    def __init__(self, nbThreads=20):
        """
        When initiating the class, one has to specify the number of threads to be
        used if using multithreading.
        """
        self.nbThreads = nbThreads
        self.listOfListOfTuples = []
        self.urlIndex = None

    def prepareList(self, listUrls):
        """
        Method that makes tuples with the URLs and their indexes, to be able to
        name the file generated differently. It has to be executed with the list
        of URLs as input (except if using loopGet method).
        """
        self.urlIndex = [(elem, i) for i, elem in enumerate(listUrls)]

    def getPages(self, urlIndex):
        """
        Method that takes a tuple (URL, index), gets the html text from the URL
        and store it in a file containing the index in its name.
        """
        urls, index = urlIndex
        page = urllib.request.urlopen(urls)
        WritePage = page.read()
        file1 = open("urlPage{}.txt".format(index), 'w')
        file1.write(str(WritePage))
        file1.close()

    def loopGet(self, listUrls):
        """
        Method using a loop that takes all the html texts from a list of URLs
        and save them in different files distinguished by their indexes. Takes
        the list of URLs as argument.
        """
        for i, elem in enumerate(listUrls):
            page = urllib.request.urlopen(elem)
            WritePage = page.read()
            file1 = open("urlPage{}.txt".format(i), 'w')
            file1.write(str(WritePage))
            file1.close()

    def threadingGet(self, urlIndex=""):
        """
        Method that takes all the html texts from a list of URLs and save them in
        different files, using a pool of threads and map function.
        """
        if urlIndex: # when using multithreading nested in multiprocessing
            pool = ThreadPool(self.nbThreads) # 10 threads
            pool.map(self.getPages, urlIndex)

            pool.close()
            pool.join()

        else: #when using it separately
            pool = ThreadPool(self.nbThreads) # n threads
            pool.map(self.getPages, self.urlIndex)

            pool.close()
            pool.join()

    def multiProcessingGet(self):
        """
        Method that takes all the html texts from a list of URLs and save them in
        different files, using a pool of processes and map function.
        """
        pool = Pool()
        pool.map(self.getPages, self.urlIndex)
        pool.close()
        pool.join()

    def multiProcessingAndThreading(self):
        """
        Method that takes all the html texts from a list of URLs and save them in
        different files, using a pool of threads in a pool of processes and map
        functions.
        """
        pool = Pool(4)
        pool.map(self.threadingGet, self.listOfListOfTuples)
        pool.close()
        pool.join()

    def make2ElemLists(self):
        """
        Make a list of lists with 2 tuples url, index to give to pools.
        """
        tmpList = []
        for tuples in self.urlIndex:
            tmpList.append(tuples)
            if len(tmpList) == 5:
                self.listOfListOfTuples.append(tmpList)
                tmpList = []


################################################################################
#20 links from the website of the youtuber sentdex (who makes Python tutorials).
#Using his website since he's making urllib tutorials so probably has not set
#restriction for requesting.
urls = [
'https://pythonprogramming.net',
'https://pythonprogramming.net/data-analysis-tutorials/',
'https://pythonprogramming.net/robotics-tutorials/',
'https://pythonprogramming.net/web-development-tutorials/',
'https://pythonprogramming.net/game-development-tutorials/',
'https://pythonprogramming.net/python-fundamental-tutorials/',
'https://pythonprogramming.net/introduction-to-python-programming/',
'https://pythonprogramming.net/introduction-intermediate-python-tutorial/',
'https://pythonprogramming.net/gui-development-tutorials/',
'https://pythonprogramming.net/basic-gui-pyqt-tutorial/',
'https://pythonprogramming.net/tkinter-depth-tutorial-making-actual-program/',
'https://pythonprogramming.net/kivy-application-development-tutorial/',
'https://pythonprogramming.net/go/introduction-go-language-programming-tutorial/',
'https://pythonprogramming.net/machine-learning-tutorials/',
'https://pythonprogramming.net/data-analysis-python-pandas-tutorial-introduction/',
'https://pythonprogramming.net/data-visualization-application-dash-python-tutorial-introduction/',
'https://pythonprogramming.net/matplotlib-intro-tutorial/',
'https://pythonprogramming.net/finance-tutorials/',
'https://pythonprogramming.net/virtual-machine-google-cloud-tutorial/',
'https://pythonprogramming.net/loading-images-python-opencv-tutorial/'
]
