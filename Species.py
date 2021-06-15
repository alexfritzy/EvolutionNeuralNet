import sys
import os
import numpy as np
import random
from Individual import Individual
from Network import Network

class Species:
    def __init__(self, path, name, inp, hidden):
        self.path = path + name + "\\"
        self.name = name
        self.inp = inp
        self.hidden = hidden
    
    def newpop(self, size): 
        os.mkdir(self.path)
        gen = open(self.path + "Gen.txt", "w+")
        gen.write("0")
        gen.close()
        gen = open(self.path + "Fitness.txt", "w+")
        gen.close()
        os.mkdir(self.path + "Gen0")
        for x in range(size):
            path = self.path + "Gen0\\" + str(x) + "\\"
            os.mkdir(path)   
            indv = Individual(path, self.inp, self.hidden)
            indv.new()

    def currentGen(self):
        f = open(self.path + "Gen.txt", "r")
        gen = f.read()
        f.close()
        return int(gen)

    def breed(self, survivors):
        gen = self.currentGen()
        parents = []
        for survivor in survivors:
            net = Network(self.path + "Gen" + str(gen) + "\\" + str(survivor) + "\\", self.inp, self.hidden)
            parents.append(net)
        random.shuffle(parents)
        for x in range(len(parents) - 1):
            parents.append(parents[x + 1])
        parents.append(parents[0])
        gen += 1
        os.mkdir(self.path + "Gen" + str(gen))
        for x in range(len(survivors)):
            path = self.path + "Gen" + str(gen) + "\\" + str(x) + "\\"
            os.mkdir(path)   
            indv = Individual(path, self.inp, self.hidden)
            indv.breed([parents[x], parents[x+10]])
            path = self.path + "Gen" + str(gen) + "\\" + str(x+10) + "\\"
            os.mkdir(path)   
            indv = Individual(path, self.inp, self.hidden)
            indv.breed([parents[x], parents[x+10]])
        f = open(self.path + "Gen.txt", "w+")
        f.write(str(gen))
        f.close()
