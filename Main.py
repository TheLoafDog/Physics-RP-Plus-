from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import math
import ast

# Constants for colour

darkGrey = '#ababab'
lightGreen = '#bfffd7'
lightRed = '#ffbfbf'
darkRed = '#b50f00'
darkGreen = '#027500'
darkBlue = '#005969'

# List of RPs for side menu buttons

requiredPracticalList = ["RP1 Stationary Waves on a String", "RP2 Interference Effects", "RP3 Determination of g", "RP4 Determination of Young's Modulus", "RP5 Determination of Resistivity of a Wire", "RP6 Internal resistance and emf", "RP7 Simple Harmonic Motion", "RP8 Boyle's Law", "RP9 Charging and Discharging Capacitors", "RP10 Magnetic Force on a Wire", "RP11 Magnetic Flux Linkage", "RP12 Inverse Square Law"]

database=open("RP info.txt", "r", encoding="utf-8")
RP_dicts = database.readlines()

def hashGet(key):
    
    #hash function
    
    hash_val = 0
    
    for letter in key:
        hash_val += ord(letter)
    hash_val = hash_val % 97
    
    while ast.literal_eval(RP_dicts[hash_val][:-1])["name"] != key:
        hash_val += 1
        
    return ast.literal_eval(RP_dicts[hash_val][:-1])


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
    
    # Creates sidebar buttons
    
    for i in range(0,12):
        newSideBarButton = Button(master = sideBarButtonFrame, width = 20, height = 2, bd = 2, relief = "raised", text = requiredPracticalList[i], wraplength = 125, command = lambda i = i: openRP(mainFrame, hashGet(requiredPracticalList[i])["xAxis"], hashGet(requiredPracticalList[i])["yAxis"], hashGet(requiredPracticalList[i])["xEntryTitle"], hashGet(requiredPracticalList[i])["yEntryTitle"], hashGet(requiredPracticalList[i])["originalEquation"], hashGet(requiredPracticalList[i])["linearisedEquation"], hashGet(requiredPracticalList[i])["mode"]))
        newSideBarButton.grid(row = i, column = 0, padx = 5, pady = 5)
    
    root.mainloop()

def destroyFrames(mainFrame): # Subroutine to destroy all frames in mainFrame. Main Frame is a holder for other frames
    for frame in mainFrame.winfo_children():
        frame.destroy()

def createGraph(currentFrame, xLabel, yLabel): # Subroutine called when new required practical is opened. Creates the UI for the graph.
    
    # Gets all global variables to reset them, as this is a new required practical
    
    global x
    global y
    global rowIndex
    
    # Creates a frame to hold the graph
    
    graphHolder = Frame(master = currentFrame, width = 550, height = 500, bg = 'black')
    graphHolder.place(relx = 1, rely = 0, x = -10, y = 10, anchor = NE)
    
    # Creates the graph UI
    
    figure, axes = plt.subplots(figsize = (6, 5)) # Figure is the entire frame for the graph. Axes is the axes on the graph. Figsize is used for UI scale
    axes.set_ylabel(yLabel) # Sets the labels on the graph
    axes.set_xlabel(xLabel)
    figure.tight_layout() # Packs graph into frame
    
    # Canvas is used to draw the figure
    
    canvas = FigureCanvas(figure, master = graphHolder)
    canvas.get_tk_widget().pack(padx = 1, pady = 1)
    
    # Resets global variables
    
    x = np.array([0])
    y = np.array([0])
    rowIndex = 1
    
    # Creates the placeholder graph
    
    axes.scatter(x, y, marker = "+", color = "black", s = 100)
    
    axes.set_xlim([0, 10]) # Setting limits is visually for the graph. The current graph shows up to 10 on x and 10 on y
    axes.set_ylim([0, 10])
    
    canvas.draw() # Draws the graph
    
    return figure, axes, canvas # Returns figure, axes and canvas so the graph can be changed in the future

def createDataEntryFrame(RPFrame, xEntryTitle, yEntryTitle, mode, axes, canvas, xAxis, yAxis, gradientString, interceptString): # Creates the frame where the user can enter data
    
    # Creates base frame
    
    dataFrame = Frame(master = RPFrame, width = 240, height = 503, bg = darkGrey, bd = 2, relief = "groove")
    dataFrame.place(relx = 0, rely = 0, x = 10, y = 10)
    
    # Creates the labels that tell the user what to input
    
    xTitle = Label(master = dataFrame, width = 12, height = 3, bg = darkGrey, text = xEntryTitle, font = ('Arial Bold', 8), justify = CENTER, wraplength = 100)
    yTitle = Label(master = dataFrame, width = 12, height = 3, bg = darkGrey, text = yEntryTitle, font = ('Arial Bold', 8), justify = CENTER, wraplength = 100)
    
    xTitle.place(x = 10, y = 0)
    yTitle.place(x = 110, y = 0)
    
    # Creates the frame where the data entry frames will be gridded into
    
    dataEntryFrame = Frame(master = dataFrame, width = 216, height = 430, bg = darkGrey)
    dataEntryFrame.place(x = 10, y = 40)
    
    # Creates the data entry frame
    
    dataEntry = Frame(master = dataEntryFrame, width = 216, height = 20, bg = darkGrey)
    xEntry = Entry(master = dataEntry)
    yEntry = Entry(master = dataEntry)
    # The button will refresh the graph with the new entries
    addButton = Button(master = dataEntry, height = 20, width = 20, text = "", bg = lightGreen, justify = CENTER, command = lambda: refreshGraph(axes, canvas, xEntry.get(), yEntry.get(), dataEntry, addButton, dataEntryFrame, xAxis, yAxis, mode, gradientString, interceptString))
    xEntry.place(x = 0, y = 0, width = 90, height = 20)
    yEntry.place(x = 100, y = 0, width = 90, height = 20)
    addButton.place(x = 196, y = 0)
    dataEntry.grid(row = 0, column = 0, pady = 3)
    # First data entry will be gridded at row 0

def refreshGraph(axes, canvas, newX, newY, entryFrame, entryButton, entryListFrame, xLabel, yLabel, mode, gradientString, interceptString): # Refreshes the graph with the new data
    
    # Retrieves global variables
    
    global x
    global y
    global rowIndex
    
    # Tries to convert user input into numbers, if it cannot then it does nothing
    
    try:
        newX = float(newX)
        newY = float(newY)
        if mode == 1: # If the mode is 1 (1 / x), set the new x value as 1 / x
            newX = 1 / float(newX)
        elif mode == 2:
            newY = math.log(newY)
        elif mode == 3:
            radians = newX * ( math.pi / 180.0 )
            newX = math.cos(radians)
    except:
        return ""
    
    axes.cla() # Clears current axes
    
    axes.set_ylabel(yLabel) # Re-adds current labels
    axes.set_xlabel(xLabel)
    
    if newX in x and newY in y: # Checks to see if the data exists already (If it exists then a delete button was likely pressed, so it will treat it as a removal)
        entryFrame.destroy() # Deletes the entry frame as it was removed
        if len(x) == 1: # If it is the only entry, it resets the graph
            x = np.array([0])
            y = np.array([0])
        else: # Otherwise it just deletes the entry
            indexX = np.where(x == newX)[0][0]
            indexY = np.where(y == newY)[0][0]
            x = np.delete(x, indexX)
            y = np.delete(y, indexY)
    elif len(x) == 1 and x[0] == 0: # If there is no other data (x only has one entry, 0) and data is added
        
        mode = 0 # The mode is determined to see what operation is done to the entries. Mode 1, for example, applies 1 / x to the x entry
        
        if xLabel == "1 / Length (1 / m)": # Checks to see if mode 1 is applicable
            mode = 1
        elif yLabel == "ln(V)":
            mode = 2
        elif xLabel == "cos(θ)":
            mode = 3
        
        entryButton.config(bg = lightRed) # Changes the button colour to red, indicating that pressing it will remove the data entry
        x = np.array([newX]) # Replaces the x and y arrays with the new entry, since there is only one entry
        y = np.array([newY])
        
        # Creates the new frame for new entries
        
        dataEntry = Frame(master = entryListFrame, width = 216, height = 20, bg = darkGrey)
        xEntry = Entry(master = dataEntry)
        yEntry = Entry(master = dataEntry)
        addButton = Button(master = dataEntry, height = 20, width = 20, text = "", bg = lightGreen, justify = CENTER, command = lambda: refreshGraph(axes, canvas, xEntry.get(), yEntry.get(), dataEntry, addButton, entryListFrame, xLabel, yLabel, mode, gradientString, interceptString))
        xEntry.place(x = 0, y = 0, width = 90, height = 20)
        yEntry.place(x = 100, y = 0, width = 90, height = 20)
        addButton.place(x = 196, y = 0)
        dataEntry.grid(row = rowIndex, column = 0, pady = 3)
        rowIndex += 1 # Places it at the new row, and adds one to the row index
    elif len(x) == 16: # If there are max entries, do nothing
        return ""
    else:
        
        mode = 0 # The mode is determined to see what operation is done to the entries. Mode 1, for example, applies 1 / x to the x entry
        
        if xLabel == "1 / Length (1 / m)": # Checks to see if mode 1 is applicable
            mode = 1
        elif yLabel == "ln(V)":
            mode = 2
        elif xLabel == "cos(θ)":
            mode = 3
        
        # Does the exact same as previous condition, except appends the new values to the x and y arrays
        
        entryButton.config(bg = lightRed)
        x = np.append(x, [newX])
        y = np.append(y, [newY])
        
        dataEntry = Frame(master = entryListFrame, width = 216, height = 20, bg = darkGrey)
        xEntry = Entry(master = dataEntry)
        yEntry = Entry(master = dataEntry)
        addButton = Button(master = dataEntry, height = 20, width = 20, text = "", bg = lightGreen, justify = CENTER, command = lambda: refreshGraph(axes, canvas, xEntry.get(), yEntry.get(), dataEntry, addButton, entryListFrame, xLabel, yLabel, mode, gradientString, interceptString))
        xEntry.place(x = 0, y = 0, width = 90, height = 20)
        yEntry.place(x = 100, y = 0, width = 90, height = 20)
        addButton.place(x = 196, y = 0)
        dataEntry.grid(row = rowIndex, column = 0, pady = 3)
        rowIndex += 1
    
    sortIndices = np.argsort(x)
    
    x = x[sortIndices]
    y = y[sortIndices]
    
    axes.scatter(x, y, marker = "x", color = "black", s = 75) # Displays the new updated graph
    
    gradientString.set("Best: Unavailable") # Sets the string variables to unavailable, changes if they are available
    interceptString.set("Unavailable")
    
    if len(x) > 1 and len(y) > 1: # Draws gradient and changes string variables if applicable
        gradient, intercept = np.polyfit(x, y, 1)
        axes.plot(x, gradient * x + intercept, linestyle = "--", linewidth = 1)
        gradientString.set(f"Best: {str(round(gradient, 3))}")
        interceptString.set(str(round(intercept, 3)))
        
    
    if len(x) == 1 and x[0] == 0: # If there is no entry, set the x and y limits to 10 as placeholder
        axes.set_xlim([0, 10])
        axes.set_ylim([0, 10])
    else: # Otherwise set the x and y limits to 1.1x the largest values
        axes.set_xlim([0, np.max(x) * 1.1])
        axes.set_ylim([0, np.max(y) * 1.1])
    
    canvas.draw() # Draw the canvas

def calculateGradients(xUncertainty, yUncertainty, axes, canvas, xLabel, yLabel, minGradientString, maxGradientString):
    
    global x
    global y
    
    sortIndices = np.argsort(x)
    
    x = x[sortIndices]
    y = y[sortIndices]
    
    try:
        if len(xUncertainty) == 0 and len(yUncertainty) == 0:
            xUncertainty = 0
            yUncertainty = 0
        elif len(xUncertainty) == 0:
            xUncertainty = 0
            yUncertainty = float(yUncertainty)
        elif len(yUncertainty) == 0:
            yUncertainty = 0
            xUncertainty = float(xUncertainty)
        else:
            xUncertainty = float(xUncertainty)
            yUncertainty = float(yUncertainty)
    except:
        return ""
    
    axes.cla()
    
    axes.set_ylabel(yLabel)
    axes.set_xlabel(xLabel)
    
    axes.scatter(x, y, marker = "x", color = "black", s = 75)
    
    if xUncertainty > 0 and yUncertainty > 0:
        axes.errorbar(x, y, xerr = xUncertainty, yerr = yUncertainty, capsize=5, ls = 'none')
    elif xUncertainty == 0:
        axes.errorbar(x, y, yerr = yUncertainty, capsize=5, ls = 'none')
    elif yUncertainty == 0:
        axes.errorbar(x, y, xerr = xUncertainty, capsize=5, ls = 'none')
    
    minGradientString.set("Min: Unavailable")
    maxGradientString.set("Max: Unavailable")
    
    if len(x) > 1 and len(y) > 1: # Draws gradient and changes string variables if applicable
        gradient, intercept = np.polyfit(x, y, 1)
        axes.plot(x, gradient * x + intercept, linestyle = "--", linewidth = 1)
        
        minX = np.copy(x)
        minY = np.copy(y)
        
        minX[0] = minX[0] - xUncertainty
        minY[0] = minY[0] + yUncertainty
        
        minX[-1] = minX[-1] + xUncertainty
        minY[-1] = minY[-1] - yUncertainty
        
        minXStart = minX[0]
        minYStart = minY[0]
        
        minXEnd = minX[-1]
        minYEnd = minY[-1]
        
        minGradient = (minYEnd - minYStart) / (minXEnd - minXStart)
        minIntercept = minYStart - minGradient * minXStart
        
        axes.plot(minX, minGradient * minX + minIntercept, linestyle = "--", linewidth = 1)
        minGradientString.set(f"Min: {str(round(minGradient, 3))}")
        
        maxX = np.copy(x)
        maxY = np.copy(y)
        
        maxX[0] = maxX[0] + xUncertainty
        maxY[0] = maxY[0] - yUncertainty
        
        maxX[-1] = maxX[-1] - xUncertainty
        maxY[-1] = maxY[-1] + yUncertainty
        
        maxXStart = maxX[0]
        maxYStart = maxY[0]
        
        maxXEnd = maxX[-1]
        maxYEnd = maxY[-1]
        
        maxGradient = (maxYEnd - maxYStart) / (maxXEnd - maxXStart)
        maxIntercept = maxYStart - maxGradient * maxXStart
        
        axes.plot(maxX, maxGradient * maxX + maxIntercept, linestyle = "--", linewidth = 1)
        maxGradientString.set(f"Max: {str(round(maxGradient, 3))}")
    
    if len(x) == 1 and x[0] == 0: # If there is no entry, set the x and y limits to 10 as placeholder
        axes.set_xlim([0, 10])
        axes.set_ylim([0, 10])
    else: # Otherwise set the x and y limits to 1.1x the largest values
        axes.set_xlim([0, np.max(x) * 1.1])
        axes.set_ylim([0, np.max(y) * 1.1])
    
    canvas.draw() # Draw the canvas

def openRP(mainFrame, yAxis, xAxis, xEntryTitle, yEntryTitle, originalEquation, linearisedEquation, mode):
    destroyFrames(mainFrame)
    
    RPFrame = Frame(master = mainFrame, width = 880, height = 720, bd = 2, relief = "groove")
    
    figure, axes, canvas = createGraph(RPFrame, xAxis, yAxis)
    
    rpInfoFrame = Frame(master = RPFrame, width = 602, height = 178, bg = darkGrey, bd = 2, relief = "groove")
    rpInfoFrame.place(relx = 1, rely = 1, x = -10, y = -10, anchor = SE)
    
    bestGradientString = StringVar(master = rpInfoFrame, value = "Best: Unavailable")
    minGradientString = StringVar(master = rpInfoFrame, value = "Min: Unavailable")
    maxGradientString = StringVar(master = rpInfoFrame, value = "Max: Unavailable")
    interceptString = StringVar(master = rpInfoFrame, value = "Unavailable")
    
    originalEquationTitle = Label(master = rpInfoFrame, width = 27, height = 2, bg = darkGrey, bd = 0, text = "Original:", font = ('Arial Bold', 13), fg = darkRed)
    originalEquation = Label(master = rpInfoFrame, width = 27, height = 1, bg = darkGrey, bd = 0, text = originalEquation, font = ('Arial', 14))
    
    linearisedEquationTitle = Label(master = rpInfoFrame, width = 27, height = 2, bg = darkGrey, bd = 0, text = "Linearised:", font = ('Arial Bold', 13), fg = darkGreen)
    linearisedEquation = Label(master = rpInfoFrame, width = 27, height = 1, bg = darkGrey, bd = 0, text = linearisedEquation, font = ('Arial', 14))
    
    gradientTitle = Label(master = rpInfoFrame, width = 27, height = 2, bg = darkGrey, bd = 0, text = "Gradients:", font = ('Arial Bold', 13), fg = darkBlue)
    gradientFrame = Frame(master = rpInfoFrame, width = 27, height = 3, bg = darkGrey, bd = 0)
    
    bestGradientLabel = Label(master = gradientFrame, width = 27, height = 1, bg = darkGrey, bd = 0, textvariable = bestGradientString, font = ('Arial', 12))
    minGradientLabel = Label(master = gradientFrame, width = 27, height = 1, bg = darkGrey, bd = 0, textvariable = minGradientString, font = ('Arial', 12))
    maxGradientLabel = Label(master = gradientFrame, width = 27, height = 1, bg = darkGrey, bd = 0, textvariable = maxGradientString, font = ('Arial', 12))
    
    interceptTitle = Label(master = rpInfoFrame, width = 27, height = 2, bg = darkGrey, bd = 0, text = "y-intercept:", font = ('Arial Bold', 13), fg = darkBlue)
    interceptLabel = Label(master = rpInfoFrame, width = 27, height = 3, bg = darkGrey, bd = 0, textvariable = interceptString, font = ('Arial', 14))
    
    originalEquationTitle.grid(row = 0, column = 0)
    linearisedEquationTitle.grid(row = 0, column = 1)
    
    originalEquation.grid(row = 1, column = 0)
    linearisedEquation.grid(row = 1, column = 1)
    
    gradientTitle.grid(row = 2, column = 0)
    interceptTitle.grid(row = 2, column = 1)
    
    gradientFrame.grid(row = 3, column = 0)
    interceptLabel.grid(row = 3, column = 1)
    
    bestGradientLabel.grid(row = 0, column = 0)
    minGradientLabel.grid(row = 1, column = 0)
    maxGradientLabel.grid(row = 2, column = 0)
    
    createDataEntryFrame(RPFrame, xEntryTitle, yEntryTitle, mode, axes, canvas, xAxis, yAxis, bestGradientString, interceptString)
    
    extraFrame = Frame(master = RPFrame, width = 240, height = 177, bg = darkGrey, bd = 2, relief = "groove")
    extraFrame.place(rely = 1, relx = 0, y = -10, x = 10, anchor = SW)
    
    uncertaintyTitle = Label(master = extraFrame, width = 12, height = 2, text = "Uncertainty", font = ('Arial Bold', 10), bg = darkGrey)
    uncertaintyTitle.place(rely = 0, relx = 0.5, y = 3, anchor = N)
    
    xUncertaintyFrame = Frame(master = extraFrame, width = 200, height = 25, bg = darkGrey)
    xUncertaintyFrame.place(relx = 0.5, rely = 0, y = 43, anchor = N)
    
    xUncertaintyTitle = Label(master = xUncertaintyFrame, width = 4, height = 1, text = "x = ±", font = ('Arial', 11), bg = darkGrey)
    xUncertaintyTitle.grid(row = 0, column = 0)
    
    xUncertaintyEntry = Entry(master = xUncertaintyFrame)
    xUncertaintyEntry.grid(row = 0, column = 1)
    
    yUncertaintyFrame = Frame(master = extraFrame, width = 200, height = 25, bg = darkGrey)
    yUncertaintyFrame.place(relx = 0.5, rely = 0, y = 70, anchor = N)
    
    yUncertaintyTitle = Label(master = yUncertaintyFrame, width = 4, height = 1, text = "y = ±", font = ('Arial', 11), bg = darkGrey)
    yUncertaintyTitle.grid(row = 0, column = 0)
    
    yUncertaintyEntry = Entry(master = yUncertaintyFrame)
    yUncertaintyEntry.grid(row = 0, column = 1)
    
    calculateGradientButton = Button(master = extraFrame, width = 14, height = 1, text = "Calculate gradients", bd = 2, relief = "raised", command = lambda: calculateGradients(xUncertaintyEntry.get(), yUncertaintyEntry.get(), axes, canvas, xAxis, yAxis, minGradientString, maxGradientString))
    calculateGradientButton.place(relx = 0.5, rely = 0, y = 100, anchor = N)
    
    RPFrame.pack()

root = Tk()
main()
