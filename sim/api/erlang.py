import numpy as np
import math

class Erlang(object):
    def __init__(self, mean, x):
        if mean == 0:
            self.rate = 100
            self.shape = 1
        else:
            self.rate = 1
            self.shape = mean
        self.x = x

    def get_pdf(self):
        return list(map(self.erlang_pdf, self.x))

    def erlang_pdf(self, x):
        return self.rate**self.shape*x**(self.shape - 1)*math.exp(-self.rate * x)/math.factorial(self.shape - 1)