#! /usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 'david'

# Importamos el módulo pygtk y le indicamos que use la versión 2
import pygtk
pygtk.require("2.0")

# Luego importamos el módulo de gtk y el gtk.glade, este ultimo que nos sirve
# para poder llamar/utilizar al archivo de glade
import gtk
import gtk.glade

from SimplexParser import *
from ParsingToFile import *
from getDataSalida import *
from ParsingToOutput import *
from subprocess import call

class MainWin:
    def __init__(self):
        # Le decimos a nuestro programa que archivo de glade usar (puede tener
        # un nombre distinto del script). Si no esta en el mismo directorio del
        # script habría que indicarle la ruta completa en donde se encuentra

        self.widgets = gtk.glade.XML("Simplex2.glade")

        # Creamos un pequeño diccionario que contiene las señales definidas en
        # glade y su respectivo método (o llamada)
        signals = { "on_Solve_clicked" : self.on_Solve_clicked,
                    "on_Clear_clicked" : self.on_Clear_clicked,
                    "on_Example_clicked" : self.on_Example_clicked,
                    "gtk_main_quit" : gtk.main_quit }

        # Luego se auto-conectan las señales.
        self.widgets.signal_autoconnect(signals)

        # Ahora obtenemos del archivo glade los widgets que vamos a
        # utilizar (en este caso son label1 y entry1)
        self.Salida = self.widgets.get_widget("Salida")
        self.Entrada = self.widgets.get_widget("Entrada")

    def on_Example_clicked(self, widget):
        problem_test_string = "Maximize p = -0.5*x + 3*y + z + 4*w \n\
x + y + z + w <= 40\n\
2*x + y - z - w >= 10\n\
2*w - y = 10"
        self.Entrada.get_buffer().set_text(problem_test_string)

    def on_Solve_clicked(self, widget):
        texto_Entrada = self.Entrada.get_buffer().get_text(self.Entrada.get_buffer().get_start_iter(), self.Entrada.get_buffer().get_end_iter())
        arg_Entrada = parseProblem(texto_Entrada)
        if arg_Entrada is None:
            self.Salida.get_buffer().set_text("Tu formato de entrada es incorrecto")
        else:
            print arg_Entrada
            ParsingToFile(arg_Entrada)
            if call(["timeout","2", "../bin/Simplex"]) != 0:
                self.Salida.get_buffer().set_text("No hay solución óptima para este problema")
            else:
                arg_Salida = getDataSalida()
                print arg_Salida
                texto_Salida = ParsingToOutput(arg_Entrada, arg_Salida)
                self.Salida.get_buffer().set_text(texto_Salida)

    def on_Clear_clicked(self, widget):
        self.Entrada.get_buffer().delete(self.Entrada.get_buffer().get_start_iter(), self.Entrada.get_buffer().get_end_iter())
        self.Salida.get_buffer().delete(self.Salida.get_buffer().get_start_iter(), self.Salida.get_buffer().get_end_iter())

# Para terminar iniciamos el programa
if __name__ == "__main__":
    MainWin()
    gtk.main()