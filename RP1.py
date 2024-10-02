#RP 1 Inverse Square Law
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np


import functions

# Constants for colour

darkGrey = '#ababab'
lightGreen = '#bfffd7'
lightRed = '#ffbfbf'


def openRP(mainFrame):
    xAxis = "1 / Length (1 / m)" # String for x axis
    yAxis = "Frequency (Hz)" # String for y axis
    
    xEntryTitle = "Length (m)" # String to tell user what to enter for x
    yEntryTitle = "Frequency (Hz)" #  # String to tell user what to enter for y
    
    originalEquation = "λ = 2L" # String for original equation
    linearisedEquation = "f = (v/2)(1/L)" # String for linearised equation
    
    mode = 1 # Mode is 1, meaning x will be 1 / x instead. If nothing special happens to entries, keep the mode as 0
    
    functions.destroyFrames(mainFrame) # Destroys all other frames
    
    RPFrame = Frame(master = mainFrame, width = 880, height = 720, bd = 2, relief = "groove")
    
    figure, axes, canvas = functions.createGraph(RPFrame, xAxis, yAxis) # Creates the graph
    
    rpInfoFrame = Frame(master = RPFrame, width = 602, height = 178, bg = darkGrey, bd = 2, relief = "groove")
    rpInfoFrame.place(relx = 1, rely = 1, x = -10, y = -10, anchor = SE)
    
    # Creates UI for RP data
    
    gradientString = StringVar(master = rpInfoFrame, value = f"Gradient: Unavailable")
    interceptString = StringVar(master = rpInfoFrame, value = f"y-intercept: Unavailable")
    
    originalEquation = Label(master = rpInfoFrame, width = 27, height = 4, bg = darkGrey, bd = 0, text = f"Original: {originalEquation}", font = ('Arial', 14))
    linearisedEquation = Label(master = rpInfoFrame, width = 27, height = 4, bg = darkGrey, bd = 0, text = f"Linearised: {linearisedEquation}", font = ('Arial', 14))
    gradientLabel = Label(master = rpInfoFrame, width = 27, height = 4, bg = darkGrey, bd = 0, textvariable = gradientString, font = ('Arial', 14))
    interceptLabel = Label(master = rpInfoFrame, width = 27, height = 4, bg = darkGrey, bd = 0, textvariable = interceptString, font = ('Arial', 14))
    
    originalEquation.grid(row = 0, column = 0)
    linearisedEquation.grid(row = 0, column = 1)
    gradientLabel.grid(row = 1, column = 0)
    interceptLabel.grid(row = 1, column = 1)
    
    functions.createDataEntryFrame(RPFrame, xEntryTitle, yEntryTitle, mode, axes, canvas, xAxis, yAxis, gradientString, interceptString) # Creates data entry
    
    RPFrame.pack()