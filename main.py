# this is the main file
from tkinter import *

import settings
import fun
import screen
import export
import scenarios

root = Tk()
root.geometry("800x600")


#set up of frames
    # Frames definition
frame_one = Frame(root, background="grey")
frame_one.grid(row=0, column=0, sticky = "nsew")
frame_two = Frame(root, background="pink")
frame_two.grid(row=1, column=0, sticky="nsew")
frame_three = Frame(root, background="blue")
frame_three.grid(row=2, column=0, sticky="nsew")

frame_one_one = Frame(root, background="pink")
frame_one_one.grid(row=0, column=1, sticky="nsew")
frame_two_two = Frame(root, background="red")
frame_two_two.grid(row=1, column=1, sticky="nsew")

frame_one_three = Frame(root, background="yellow")
frame_one_three.grid(row=0, column=2, sticky="nsew")

    # delete all frames
frameslist = [frame_one, frame_two, frame_one_one, frame_two_two, frame_one_three]
def deleteframes ():
    for i in frameslist:
        for widget in i.winfo_children():
            widget.destroy()


def gen_inputfields():
    settings.no_projects = screen.EnterField(framevar=frame_one, inputrow=1, inputcolumn=0, inputtext="Number of projects", basicvalue=100, type=0)
    settings.density_min = screen.EnterField(framevar=frame_one, inputrow=3, inputcolumn=0, inputtext="density_min", basicvalue=250, type=0)
    settings.density_max = screen.EnterField(framevar=frame_one, inputrow=5, inputcolumn=0, inputtext="density_max", basicvalue=650, type=0)
    settings.LCOE_min = screen.EnterField(framevar=frame_one, inputrow=7, inputcolumn=0, inputtext="LCOE_min", basicvalue=35, type=0)
    settings.LCOE_max = screen.EnterField(framevar=frame_one, inputrow=9, inputcolumn=0, inputtext="LCOE_max", basicvalue=75, type=0)

    settings.others_change = screen.EnterField(framevar=frame_one, inputrow=11, inputcolumn=0, inputtext="Other factors % ", basicvalue=0, type=0)

    settings.el_price = screen.EnterField(framevar=frame_one, inputrow=13, inputcolumn=0, inputtext="Electricity price ", basicvalue=0, type=0)

    settings.extra_compensation = screen.EnterField(framevar=frame_one, inputrow=15, inputcolumn=0, inputtext="Extra comp % ", basicvalue=100, type=0)


    Buttonthatdoessomething = screen.GeneralButton(framevar=frame_two, inputrow=0, inputcolumn=0, inputtext="Generate once", function=scenarios.generate_once)
    Buttonthatdoessomethingb = screen.GeneralButton(framevar=frame_two, inputrow=0, inputcolumn=1, inputtext="Generate once germ", function=scenarios.generate_once_germ)

    Buttonthatdoessomething2 = screen.GeneralButton(framevar=frame_two, inputrow=2, inputcolumn=0, inputtext="Generate x times", function=scenarios.generate_xtimes)
    Buttonthatdoessomething2b = screen.GeneralButton(framevar=frame_two, inputrow=2, inputcolumn=1, inputtext="Generate x times germ", function=scenarios.generate_xtimes_germ)

    Buttonthatdoessomething3 = screen.GeneralButton(framevar=frame_two, inputrow=4, inputcolumn=0, inputtext="Generate specific scenario", function=scenarios.generate_specific_combination)
    Buttonthatdoessomething3b = screen.GeneralButton(framevar=frame_two, inputrow=4, inputcolumn=1, inputtext="Generate specific scenario germ", function=scenarios.generate_specific_combination_germ)

    Buttonthatdoessomething4b = screen.GeneralButton(framevar=frame_two, inputrow=6, inputcolumn=1, inputtext="Generate German auctions", function=scenarios.generate_german_auctions)


    settings.pdf = screen.dropdownmenu(framevar=frame_one_one, rowID=0, columnID=0, defaultvalue=settings.pdf_options[0], options=settings.pdf_options)

    settings.pdf_parameter1 = screen.EnterField(framevar=frame_one_one, inputrow=3, inputcolumn=0, inputtext="Parameter1", basicvalue=1, type=1)
    settings.pdf_parameter2 = screen.EnterField(framevar=frame_one_one, inputrow=5, inputcolumn=0, inputtext="Parameter1", basicvalue=1, type=1)


    settings.winning_projects = screen.EnterField(framevar=frame_one_three, inputrow=1, inputcolumn=0, inputtext="winning projects", basicvalue=50, type=0)
    settings.iterations = screen.EnterField(framevar=frame_one_three, inputrow=3, inputcolumn=0,
                                                  inputtext="No. of iterations", basicvalue=1, type=0)



    Buttonpdfs = screen.GeneralButton(framevar=frame_two_two, inputrow=0, inputcolumn=0,
                                                   inputtext="show pdf", function=screen.HistPlot_selected)
    Buttonpdfs = screen.GeneralButton(framevar=frame_two_two, inputrow=1, inputcolumn=0,
                                                   inputtext="show pdfs", function=screen.HistPlot)

# initial set up of input variables and input fields
settings.changable_var()
gen_inputfields()
settings.create_variables()


def Page1():
    pass

def Page2():
    gen_inputfields()


#Topmenubar - just TESTING
class menuscreens(Frame):
    def __init__(self):
        super().__init__()
        self.navigationbar()

    def navigationbar(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        menubar.add_command(label="Page1", command=lambda: Page1())
        menubar.add_command(label="Gen Again", command=lambda: Page2())
        menubar.add_command(label="Delete", command=lambda: deleteframes())




menuscreens()
root.mainloop()


