#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'edgar'


operadores = ["=", "+", "-", "*"]


def parseObjectiveFunction(kind, objectiveFunction):
    """
    Esta funcion toma la funcion objetivo;('p = 0.5*x + 3*y + z + 4*w')
    devuelve la lista de sus variable en oroden i.e ['x1', 'x2', 'x3']
    sus coeficientes i.e [1.0, 3.9, 0.0]
    y la variable a optimizar i.e 'z'
    """
    listOfVariables = []
    vectorOfProblem = []

    i = 0
    tmp_variable = ""
    varOptimizable = ""

    try:
        while True:  # Este while saca la variable a optimizar
            if objectiveFunction[i] == ' ':  # tira los espacios
                i += 1
                continue
            elif objectiveFunction[i] == '=':
                i += 1
                break
            else:
                varOptimizable += objectiveFunction[i]
                i += 1
            if i > len(objectiveFunction):
                return None
    except IndexError:
        return None

    signo = 1
    while i < len(objectiveFunction):  # saca las variables y sus coeficientes
        if objectiveFunction[i] == ' ':
            i += 1
            continue
        elif objectiveFunction[i] == '*':
            vectorOfProblem.append(signo * float(tmp_variable))
            tmp_variable = ""
            signo = 1
        elif objectiveFunction[i] == '-':
            signo = -1
            if len(listOfVariables) == len(vectorOfProblem) and len(vectorOfProblem) != 0:
                if len(tmp_variable) == 0:
                    return None
                vectorOfProblem.append(float(signo))
            elif len(listOfVariables) == len(vectorOfProblem) and len(vectorOfProblem) == 0:
                signo = -1
                i += 1
                continue
            listOfVariables.append(tmp_variable)
            tmp_variable = ""
        elif objectiveFunction[i] == '+':
            signo *= 1
            if len(listOfVariables) == len(vectorOfProblem):
                vectorOfProblem.append(float(signo))
            listOfVariables.append(tmp_variable)
            tmp_variable = ""
        else:
            tmp_variable += objectiveFunction[i]
        i += 1
    listOfVariables.append(tmp_variable)

    if kind == "Minimize":
        vectorOfProblem = [-i for i in vectorOfProblem]

    return listOfVariables, vectorOfProblem, varOptimizable


def parseConstrains(problem, listOfVariables):
    A = [[0.0 for l in xrange(len(listOfVariables))] for j in xrange(len(problem) - 1)]
    b = []
    desigualdades = []
    del problem[0]
    for i in xrange(len(problem)):
        lineProblem = problem[i].strip(' ')
        #print lineProblem
        k = 0
        tmp_var = ""
        tmp_value = 1.0
        signo = 1.0
        n_var = 0
        n_val = 0
        while True:
            if lineProblem[k] == ' ':
                if k >= len(lineProblem):
                    break
                k += 1
                continue
            elif lineProblem[k] == '<' or lineProblem[k] == '>' or lineProblem[k] == '=':

                if lineProblem[k] == '<':
                    desigualdades.append(-1)
                elif lineProblem[k] == '>':
                    desigualdades.append(1)
                else:
                    desigualdades.append(0)
                if lineProblem[k + 1] == '=':
                    k += 2
                else:
                    k += 1
                b.append(float(lineProblem[k:].strip()))
                break
            elif lineProblem[k] not in operadores:
                tmp_var += lineProblem[k]
            elif lineProblem[k] == '*':
                tmp_value = signo * float(tmp_var)
                tmp_var = ""
                n_val += 1
            elif lineProblem[k] == '+':
                if n_var == n_val:
                    #print tmp_var, i
                    A[i][listOfVariables.index(tmp_var)] = signo
                    n_var += 1
                    tmp_var = ""
                else:
                    #print tmp_var, i
                    A[i][listOfVariables.index(tmp_var)] = signo * tmp_value
                    n_var += 1
                    tmp_var = ""
                    tmp_value = 1.0
                signo = 1.0
            elif lineProblem[k] == '-':
                if k == 0:
                    signo = -1.0
                    k += 1
                    continue
                elif n_var == n_val and n_val != 0:
                    A[i][listOfVariables.index(tmp_var)] = signo
                    n_var += 1
                    tmp_var = ""
                else:
                    A[i][listOfVariables.index(tmp_var)] = signo * tmp_value
                    n_var += 1
                    tmp_var = ""
                    tmp_value = 1.0
                signo = -1.0
            k += 1
        #print tmp_var, listOfVariables.index(tmp_var), i

        A[i][listOfVariables.index(tmp_var)] = signo * tmp_value


    return A, b, desigualdades


def parseProblem(myProblem):
    """
    Esta función toma una cadena de la formma

    "Maximize p = -0.5*x + 3*y + z + 4*w
    x + y + z + w <= 40
    2*x + y - z - w >= 10
    2*w - y >= 10"

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
    #print(kindOfProblem, problem)
    try:
        listOfVariables, vectorOfProblem, varOptimizable = parseObjectiveFunction(kindOfProblem, problem)
    except :
        return None
    try:
        matrixOfCoeficient, vectorOfCoeficient, vectorOfInequalitys = parseConstrains(myProblem, listOfVariables)
    except :
        return None

    return kindOfProblem, listOfVariables, vectorOfProblem, varOptimizable, matrixOfCoeficient, vectorOfCoeficient, vectorOfInequalitys

if __name__ == "__main__":
    problem_test_string = "Maximize p = -0.5*x - 3*y + z + 4*w \n\
    -x + y + z + w <= 40\n\
    2*x + y - z - w >= 10\n\
    2*w - y = 10"
    print parseProblem(problem_test_string)

