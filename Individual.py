import sys
import os
import numpy as np
import random

class Individual():
    def __init__(self, path, inp, hidden):
        self.path = path
        self.inp = inp
        self.hidden = hidden
        self.out = 4

    def breed(self, parents):
        if self.hidden == 0:
            #Input to Out
            path = self.path + "ItoO\\"
            os.mkdir(path)
            for x in range(4):
                node = open(path + "Neuron" + str(x) + ".txt", "w+")
                bias = parents[random.randint(0, 1)].inpbiases[x]
                if random.randint(0, 9) == 0:
                    bias += random.normalvariate(0, 0.2)
                weights = [str(bias) + "\n"]
                for y in range(self.inp * self.inp):
                    weight = parents[random.randint(0, 1)].inpweights[x][y]
                    if random.randint(0, 9) == 0:
                        weight += random.normalvariate(0, 0.35)
                    weights.append(str(weight) + "\n")
                node.writelines(weights)
                node.close()
            return

        #Input to Hidden
        path = self.path + "ItoH\\"
        os.mkdir(path)
        for x in range(self.hidden):
            node = open(path + "Neuron" + str(x) + ".txt", "w+")
            bias = parents[random.randint(0, 1)].inpbiases[x]
            if random.randint(0, 9) == 0:
                bias += random.normalvariate(0, 0.2)
            weights = [str(bias) + "\n"]
            for y in range(self.inp * self.inp):
                weight = parents[random.randint(0, 1)].inpweights[x][y]
                if random.randint(0, 9) == 0:
                    weight += random.normalvariate(0, 0.35)
                weights.append(str(weight) + "\n")
            node.writelines(weights)
            node.close()

        #Hidden to Out
        path = self.path + "HtoO\\"
        os.mkdir(path)
        for x in range(self.out):
            node = open(path + "Neuron" + str(x) + ".txt", "w+")
            bias = parents[random.randint(0, 1)].hiddenbiases[x]
            if random.randint(0, 4) == 0:
                bias += random.normalvariate(0, 0.1)
            weights = [str(bias) + "\n"]
            for y in range(self.hidden):
                weight = parents[random.randint(0, 1)].inpweights[x][y]
                if random.randint(0, 4) == 0:
                    weight += random.normalvariate(0, 0.25)
                weights.append(str(weight) + "\n")
            node.writelines(weights)
            node.close()

    def new(self):
        if self.hidden == 0:
            #Input to Out
            path = self.path + "ItoO\\"
            os.mkdir(path)
            for x in range(4):
                node = open(path + "Neuron" + str(x) + ".txt", "w+")
                bias = random.random() * -3 + 1
                weights = [str(bias) + "\n"]
                for y in range(self.inp * self.inp):
                    weight = random.random() * 8 - 4
                    weights.append(str(weight) + "\n")
                node.writelines(weights)
                node.close()
            return

        #Input to Hidden
        path = self.path + "ItoH\\"
        os.mkdir(path)
        for x in range(self.hidden):
            node = open(path + "Neuron" + str(x) + ".txt", "w+")
            bias = random.random() * -3 + 1
            weights = [str(bias) + "\n"]
            for y in range(self.inp * self.inp):
                weight = random.random() * 8 - 4
                weights.append(str(weight) + "\n")
            node.writelines(weights)
            node.close()

        #Hidden to Out
        path = self.path + "HtoO\\"
        os.mkdir(path)
        for x in range(self.out):
            node = open(path + "Neuron" + str(x) + ".txt", "w+")
            bias = random.random() * -3 + 1
            weights = [str(bias) + "\n"]
            for y in range(self.hidden):
                weight = random.random() * 8 - 4
                weights.append(str(weight) + "\n")
            node.writelines(weights)
            node.close()
                