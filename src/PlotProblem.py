#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from sympy import *

__author__ = 'edgar'


def PlotProblem(arg_In):
    print type(arg_In)
    print type(arg_In[1])
    if len(arg_In[1]) != 2:
        return None

    x1 = np.arrange
    print x, y

if __name__ == "__main__":
    PlotProblem(['Maximize', ['x', 'y'], [-0.5, -3.0], 'p', [[-1.0, 1.0], [2.0, -1.0]], [-1, 1]])
