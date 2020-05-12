from tkinter import *
import matplotlib.pyplot as plt

import settings

class EnterField(object):
    def __init__(self, framevar, inputrow, inputcolumn, inputtext, basicvalue, type):
        self.framevar = framevar
        self.inputrow = inputrow
        self.inputcolumn = inputcolumn
        self.inputtext = inputtext
        self.var = 0 + basicvalue

        #tzpe 1 is for float
        self.type = type

        self.CreateInputField()
        self.ShowIt()

    def CreateInputField(self):
        self.InputField = Entry(self.framevar)
        self.InputField.bind("<Return>", self.StoreNumber)
        self.InputFieldLabel = Label(self.framevar, text=self.inputtext + ": " + str(self.var))

    def ShowIt(self):
        self.InputField.grid(row=self.inputrow, column=self.inputcolumn, sticky=W)
        self.InputFieldLabel.grid(row=self.inputrow - 1, column=self.inputcolumn, sticky=W)

    def StoreNumber(self, arg):
        if self.type == 1:
            self.var = float(self.InputField.get())
        else:
            self.var = int(self.InputField.get())

        InputFieldLabel = Label(self.framevar, text=self.inputtext + ": " + str(self.var))
        InputFieldLabel.grid(row=self.inputrow - 1, column=self.inputcolumn, sticky=W)

class GeneralButton(object):
    def __init__(self, framevar, inputrow, inputcolumn, inputtext, function):
        Buttoncompare = Button(framevar, text=inputtext, command=function)
        Buttoncompare.grid(row=inputrow, column=inputcolumn, sticky=W)

class dropdownmenu(object):
    def __init__(self, framevar, rowID, columnID, defaultvalue, options):
        self.picked = defaultvalue

        self.screen = StringVar()
        self.screen.set(defaultvalue)

        self.framevar = framevar
        self.rowID = rowID
        self.columnID = columnID
        self.options = options

        self.ShowIt()

    def ShowIt(self):
        popupMenu = OptionMenu(self.framevar, self.screen, *self.options)
        Label(self.framevar, text="Choose a PDF").grid(row=self.rowID, column=self.columnID)
        popupMenu.grid(row=self.rowID+1, column=self.columnID)

        self.screen.trace('w', self.change_dropdown)

    def change_dropdown(self, *args):
        self.picked = self.screen.get()


def HistPlot():
    s = []
    x = int(settings.no_projects.var)
    settings.no_projects.var = 500

    for i in range(0, len(settings.pdf_functions)):
        s.append([])
        s[i] = settings.pdf_functions[str(settings.pdf_options[i])]()

        plt.hist(s[i], histtype='step', bins=20, label=str(settings.pdf_options[i]))

    settings.no_projects.var = int(x)

    plt.gca().set_xlim([0, settings.density_max.var])
    plt.legend()
    plt.show()

def HistPlot_selected():
    x = int(settings.no_projects.var)
    settings.no_projects.var = 5000

    s = settings.pdf_functions[str(settings.pdf.picked)]()
    plt.hist(s, histtype='step', bins=50, label=str(settings.pdf.picked))

    settings.no_projects.var = int(x)

    plt.gca().set_xlim([0, settings.density_max.var + 0.1 *settings.density_max.var])
    plt.legend()
    plt.show()


