#!/home/boris/anaconda3/bin/python3
# -*- coding: utf-8 -*-

"""
DEE bioinformatics seminar presentation code.

Created on Wed Apr 18 11:11:11 2018

@author: boris
"""
import random
import itertools
from multiprocessing import Pool
import threading
from queue import Queue
from multiprocessing.dummy import Pool as ThreadPool
import time


class makeHugeRandomFiles:
    """
    Class that contains a method allowing to generate 12 files with randomly
    generated sequences, selected to be similar.
    """
    def __init__(self):
        self.seqLength = 0
        self.alphabet = []
        self.nbSeq = 0
        self.q = None

    def makeRandomSeq(self, seqLength=10, alphabet=['A', 'C', 'G', 'T'], nbSeq=50000):
        """
        Method that generates 50'000 sequences randomly generated but with enough
        similarity to make a decent alignment. The first argument is the length
        of the sequence to be randomly generated and is of 10 by default. The
        second argument is the alphabet from which are composed the sequences,
        which is by default a list of the DNA bases. The third argument is the
        number of sequences to be randomly generated.
        """
        self.seqLength = seqLength
        self.alphabet = alphabet
        self.nbSeq = nbSeq

        #generate all possible sequences of a certain length
        tmpComb = list(itertools.product(''.join(self.alphabet), repeat=self.seqLength))
        allComb = [''.join(list(tuples)) for tuples in tmpComb]

        #Make some motifs more represented for the alignment to be coherent by
        #using scores for certain bases: let's make a score for each position generated randomly
        #which will represent the ideal motif
        scores = {i:self.randProb4() for i in range(self.seqLength)}

        #Now a dictionary with the representation of each sequence based on its
        #likelihood based on the the probabilities for each position randomly
        #generated will be generated
        seqScores = dict()
        for seq in allComb:
            totalSeqScore = 0
            for i in range(self.seqLength):
                if seq[i] == "A":
                    totalSeqScore += scores[i][0]
                elif seq[i] == "C":
                    totalSeqScore += scores[i][1]
                elif seq[i] == "G":
                    totalSeqScore += scores[i][2]
                elif seq[i] == "T":
                    totalSeqScore += scores[i][3]
            seqScores[seq] = int(totalSeqScore*10)

        #Now remove 99% less represented motifs
        #So make list of representations and seq and keep 1% highest values
        allRepresentations = sorted([(value, key) for key,value in seqScores.items()], reverse=True)
        allRepresentations = allRepresentations[0:int(len(allRepresentations)*0.01)]
        allCombRepr = [key for value,key in allRepresentations]

        #Now take n sequences randomly
        self.finalSeq = [random.choice(allCombRepr) for i in range(self.nbSeq)]

    def randProb4(self):
        """
        Method that generates 4 random probabilities, whose sum equals 1.
        """
        listProb = []
        total = 10
        val = 0
        for i in range(4):
            if i == 3:
                listProb.append(total/10) # remaining % to be added directly
            else:
                val = random.choice(range(total))
                listProb.append(val/10)
                total -= val

        return listProb

    def writeSequencesToFile(self, filename="RandomSequences.fasta"):
        """
        Method that writes the previously generated sequences to a file.
        """
        randomSeq = open(filename, "w")
        for i, seq in enumerate(self.finalSeq):
            randomSeq.write(">Sequence{}\n{}\n".format(i, seq))
        randomSeq.close()

    def SimpleCycle(self, nbCycles=12, seqLength=10):
        """
        Method that makes 12 files (by default) of the n randomly generated
        sequences with a for loop creating the files one after the other.
        """
        for i in range(nbCycles):
            self.makeRandomSeq(seqLength)
            self.writeSequencesToFile("RandomSequences{}.fasta".format(i))

    def MultiProcessingProcess(self, nbCycles=12, seqLength=10, nbCores=8):
        """
        Method that makes 12 files of the n randomly generated sequences with a
        pool of processes creating the files in parallel.
        """
        pool = Pool(processes=nbCores) # specify a value according to the number
        #of cores on your computer
        pool.map(self.MultiProcessCycle, range(nbCycles))
        pool.close()
        pool.join()

    def MultiProcessCycle(self, fileNb, seqLength=10):
        """
        Method used by the processes to generate the random sequences and the
        files.
        """
        self.makeRandomSeq(seqLength)
        self.writeSequencesToFile("RandomSequences{}.fasta".format(fileNb))

    def MultiThreadProcess(self, nbCycles=12, seqLength=10, nbThreads=8):
        """
        Method that makes 12 files of the n randomly generated sequences with
        threads creating the files. Note that this method uses a queue.
        """
        self.q = Queue()

        for x in range(nbThreads):#nb threads
             t = threading.Thread(target=self.threader)

             # classifying as a daemon, so they will die when the main dies
             t.daemon = True

             # begins, must come after daemon definition
             t.start()



        # len(allFiles) jobs assigned.
        for files in range(nbCycles):
            self.q.put(files) #put to the queue

        # wait until the thread terminates.
        self.q.join()

    def threader(self):# The threader thread pulls a worker from the queue and processes it
        """
        Method that takes the arguments from the queue to give them to the function
        to be executed by the threads.
        """
        while True:
                # gets a worker from the queue
            worker = self.q.get()

            # Run the example job with the avail worker in queue (thread)
            self.MultiProcessCycle(worker)

            # completed with the job
            self.q.task_done()

    def MultithreadForDummy(self, nbCycles=12, nbThreads=8):
        """
        Method that makes 12 files of the n randomly generated sequences with a
        pool of threads.
        """
        pool = ThreadPool(nbThreads)
        pool.map(self.MultiProcessCycle, range(nbCycles))

    ############################################################################
    #This part has not been used in the presentation
    def WriteHugeFileSimple(self, nbCycles):
        """
        Method that generates huge files composed of a repeated sequence with a
        for loop. It aims at creating a resource demanding process.
        """
        hugeFile = open("HugeFile.txt", "w")
        for i in range(nbCycles):
            hugeFile.write("This process seems anticonstitutionally anticonstitutional\n")
        hugeFile.close()

    def WriteHugeFileMultiProcessing(self, nbCycles, nbCores=8): #Not working need lock or 1 writing process
        """
        Method that generates huge files composed of a repeated sequence with
        multiple processes running in parallel. It aims at creating resource
        demanding processes.
        """
        self.hugeFile = open("HugeFile.txt", "w")
        pool = Pool(processes=nbCores)
        pool.map(self.WriteHugeFile, range(nbCycles))
        pool.close()
        pool.join()
        self.hugeFile.close()

    def WriteHugeFileMultiThreading(self, nbCycles, nbThreads=8):
        """
        Method that generates huge files composed of a repeated sequence with
        multiple threads. It aims at creating resource demanding processes.
        """
        self.hugeFile = open("HugeFile.txt", "w")
        pool = ThreadPool(nbThreads)
        results = pool.map(self.WriteHugeFile, range(nbCycles))
        self.hugeFile.close()

    def WriteHugeFile(self, nbCycles):#don't use the argument, just required to use map
        """
        Method that is used by multiprocessing and multithreading methods to
        generate the huge file.
        """
        self.hugeFile.write("This process seems anticonstitutionally anticonstitutional\n")

################################################################################
#The code below is to execute separated parts. Note that it was made to test
#the classes and methods.

#if __name__ == "__main__":
    #import os
    #import subprocess

    #os.chdir("/home/boris/Documents/DEESeminar")

    #randFileGen = makeHugeRandomFiles()
    #randFileGen.MultiProcessingProcess()
    #randFileGen.MultithreadForDummy(nbThreads=12)
    #randFileGen.SimpleCycle()
    #randFileGen.MultiThreadProcess(nbThreads=12)

    #randFileGen.WriteHugeFileSimple(10000000)
    #randFileGen.WriteHugeFileMultiProcessing(10000000)
    #randFileGen.WriteHugeFileMultiThreading(10000000)
    #subprocess.call("mafft RandomSequences.fasta 1> RandomSequences.afa 2> trash", shell=True)

#Make the first part as the text processing step and the msa as the tool use. So make 12 for files
#in the first part to be able to work them in parallel
