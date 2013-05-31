#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'edgar'


def parseObjectiveFunction(objectiveFunction):
    listOfVariables = []
    vectorOfProblem = []
    return listOfVariables, vectorOfProblem


def parseProblem(myProblem):
    """
    Esta función toma una cadena de la formma

    "Maximize p = 0.5*x + 3*y + z + 4*w
    x + y + z + w <= 40
    2*x + y - z - w >= 10
    w - y >= 10"

    La función recibe una cadena con los siguientes elementos:
    1) La palabra "Maximizar" o "Minimizar"
    2) La función objetivo Ej. p=2x1+4x2 (Yo creo que sin espacios)
    3) M restricciones Ej. x1+2*x2<=8 (No sé si separadas por un salto de línea, o por comas

    La función debe regresar una lista con los siguientes elementos:
    1) Un vector de cadenas, donde la i-ésima cadena representa la i-ésima variable.
    2) Un vector con los coeficientes de la función objetivo,
       donde el i-ésimo elemento corresponde al coeficiente de la i-ésima variable. Hacer el
       correspondiente cambio en los coeficientes si la función es de Minimizar.
    3) Una matriz, donde el elemento (i, j) corresponde al coeficiente
       de la j-ésima variable en la i-ésima restricción.
    4) Una matriz, donde el elemento (i, 0) corresponde al coeficiente de la i-ésima
       restricción y el elemento (i, 1) es un -1 si la restricción es un menor qué,
       un 0 si es un igual qué o un 1 si es un mayor qué.
    5) Un booleano, que tendrá un valor false si hay algun error en la entrada o true si todo salió bien.
    6) Una cadena con el error surgido si hubo alguno o una cadena vacía si no hubo ningún error.
    7) Un booleano, que tendrá valor true si la función es de Maximizar o false si es de Minimizar.
    """
    myProblem = [token.strip(" ") for token in myProblem.strip(" ").split("\n")]
    kindOfProblem, aux,  problem = myProblem[0].partition(" ")
    kindOfProblem = kindOfProblem.strip(" ")
    print(kindOfProblem, problem)
    listOfVariables, vectorOfProblem = parseObjectiveFunction(problem)

    return kindOfProblem, listOfVariables, vectorOfProblem, myProblem

if __name__ == "__main__":
    problem_test_string = "Maximize p = 0.5*x + 3*y + z + 4*w \n\
    x + y + z + w <= 40\n\
    2*x + y - z - w >= 10\n\
    w - y >= 10"
    print parseProblem(problem_test_string)

