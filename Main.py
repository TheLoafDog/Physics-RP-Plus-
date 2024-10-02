#RP 12 Inverse Square Law

from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

# other python files
import  RP1


# Constants for colour

darkGrey = '#ababab'
lightGreen = '#bfffd7'
lightRed = '#ffbfbf'

# List of RPs for side menu buttons

requiredPracticalList = ["RP1 Stationary Waves on a String", "RP2 Interference Effects", "RP3 Determination of g", "RP4 Determination of Young's Modulus", "RP5 Determination of Resistivity of a Wire", "RP6 Internal resistance and emf", "RP7 Simple Harmonic Motion", "RP8 Boyle's Law", "RP9 Charging and Discharging Capacitors", "RP10 Magnetic Force on a Wire", "RP11 Magnetic Flux Linkage", "RP12 Inverse Square Law"]

# Global variables

x = np.array([0]) # x is the points on the x axis. Gets reset every time new practical is opened.
y = np.array([0]) # y is the points on the y axis. Gets reset every time new practical is opened.
rowIndex = 1 # This is used for creating new entries. It uses the rowIndex as the row when gridding. Gets reset every time new practical is opened.

def main():
    
    # Creates main menu
    
    root.title("Physics RP Plus")
    root.minsize(1080, 720)
    root.geometry("1080x720")
    
    root.rowconfigure(0, weight = 1)
    root.columnconfigure(0, weight = 2)
    root.columnconfigure(1, weight = 8)
    
    # Creates side bar
    
    sideBar = Frame(master = root, width = 200, height = 720, bd = 2, relief = "groove", bg = darkGrey)
    sideBar.grid(row = 0, column = 0, sticky = "nsew")
    
    sideBarTitle = Label(master = sideBar, width = 20, height = 3, text = "Physics RP Plus", bg = darkGrey, font = ('Arial', 12))
    sideBarTitle.place(relx = 0.5, rely = 0.05, anchor = CENTER)
    
    sideBarButtonFrame = Frame(master = sideBar, width = 150, height = 625, bd = 2, relief = "groove", bg = darkGrey)
    sideBarButtonFrame.place(relx = 0.5, rely = 0.525, anchor = CENTER)
    
    # For scaling program
    
    mainFrame = Frame(master = root, width = 880, height = 720, bd = 2, relief = "groove")
    mainFrame.grid(row = 0, column = 1, sticky = "nsew")
    
    # Creates a welcome frame. Parent is mainFrame so when you delete children of the mainFrame, welcomeFrame is deleted
    
    welcomeFrame = Frame(master = mainFrame, width = 880, height = 720, bd = 2, relief = "groove")
    
    titleText = Label(master = welcomeFrame, width = 20, height = 2, text = "Physics RP Plus", font = ('Arial Bold', 45))
    titleText.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    
    contributors = Label(master = welcomeFrame, width = 45, height = 2, text = "Developed by Brandon Jake Nuñez and Fahad Wasim", font = ('Arial', 15))
    contributors.place(relx = 0.5, rely = 0.6, anchor = CENTER)
    
    welcomeFrame.pack()
    
    # Puts all the subroutines in a list to assign it to button commands
    
    requiredPracticalSubroutines = [RP1.openRP, openRP2, openRP3, openRP4, openRP5, openRP6, openRP7, openRP8, openRP9, openRP10, openRP11, openRP12]
    
    # Creates sidebar buttons
    
    for i in range(0,12):
        newSideBarButton = Button(master = sideBarButtonFrame, width = 20, height = 2, bd = 2, relief = "raised", text = requiredPracticalList[i], wraplength = 125, command = lambda i = i: requiredPracticalSubroutines[i](mainFrame))
        newSideBarButton.grid(row = i, column = 0, padx = 5, pady = 5)
    
    root.mainloop()

def openRP2(mainFrame):
    print("")

def openRP3(mainFrame):
    print("")

def openRP4(mainFrame):
    print("")

def openRP5(mainFrame):
    print("")

def openRP6(mainFrame):
    print("")

def openRP7(mainFrame):
    print("")

def openRP8(mainFrame):
    print("")

def openRP9(mainFrame):
    print("")

def openRP10(mainFrame):
    print("")

def openRP11(mainFrame):
    print("")

def openRP12(mainFrame):
    print("")

root = Tk()
main()

