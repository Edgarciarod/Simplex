#! /usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 'david'

def ParsingToFile(arg_Entrada):
    file = open("../data/Entrada.in", "w")

    file.write(str(len(arg_Entrada[1])) + " " + str(len(arg_Entrada[4])) + "\n")

    for i in arg_Entrada[2]:
        file.write( str(i)+" ")

    file.write("\n")
    k = 0
    for i in arg_Entrada[4]:
        for j in i:
            file.write(str(j)+" ")
        file.write(str(arg_Entrada[6][k]) + " " + str(arg_Entrada[5][k]) + "\n")
        k += 1