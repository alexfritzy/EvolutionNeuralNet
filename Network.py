import sys
import os
import numpy as np
import random

class Network:
    def __init__(self, path, inp, hidden):
        self.inp = inp
        self.hidden = hidden
        self.inpbiases = []
        self.inpweights = []
        self.hiddenbiases = []
        self.hiddenweights = []

        if self.hidden == 0:
            temp = path + "ItoO\\"
            for x in range(4):
                f = open(temp + "Neuron" + str(x) + ".txt", "r")
                weights = f.readlines()
                self.inpbiases.append(float(weights[0]))
                tl = []
                for weight in weights[1:]:
                    tl.append(float(weight))
                self.inpweights.append(tl)
                f.close()    
            return        

        temp = path + "ItoH\\"
        for x in range(hidden):
            f = open(temp + "Neuron" + str(x) + ".txt", "r")
            weights = f.readlines()
            self.inpbiases.append(float(weights[0]))
            tl = []
            for weight in weights[1:]:
                tl.append(float(weight))
            self.inpweights.append(tl)
            f.close()
        temp = path + "HtoO\\"
        for x in range(4):
            f = open(temp + "Neuron" + str(x) + ".txt", "r")
            weights = f.readlines()
            self.hiddenbiases.append(float(weights[0]))
            tl = []
            for weight in weights[1:]:
                tl.append(float(weight))
            self.hiddenweights.append(tl)
            f.close()

    def getOutput(self, a):
        output = []
        if self.hidden == 0:
            for b, w in zip(self.inpbiases, self.inpweights):
                output.append(max(0, np.dot(w, a) + b))
            return output
            
        hidden = []       
        for b, w in zip(self.inpbiases, self.inpweights):
            hidden.append(max(0, np.dot(w, a) + b))
        for b, w in zip(self.hiddenbiases, self.hiddenweights):
            output.append(max(0, np.dot(w, hidden) + b))
        return output