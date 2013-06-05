#! /usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 'david'

def ParsingToOutput(arg_Entrada, arg_Salida):
    if arg_Entrada == "Minimize":
        arg_Salida[0] = -arg_Salida[0]
    texto = arg_Entrada[3] + " = " + arg_Salida[0]
    k = 1
    for i in arg_Entrada[1]:
        texto = texto + ", " + i + " = " + arg_Salida[k]
        k += 1
    return texto