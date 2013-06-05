#! /usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 'david'

def getDataSalida():
    file = open("../data/Salida.out", "r")
    lineas = file.readlines()
    lineas = lineas[0].split()
    return lineas