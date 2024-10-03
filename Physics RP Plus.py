from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import math

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
    
    requiredPracticalSubroutines = [openRP1, openRP2, openRP3, openRP4, openRP5, openRP6, openRP7, openRP8, openRP9, openRP10, openRP11, openRP12]
    
    # Creates sidebar buttons
    
    for i in range(0,12):
        newSideBarButton = Button(master = sideBarButtonFrame, width = 20, height = 2, bd = 2, relief = "raised", text = requiredPracticalList[i], wraplength = 125, command = lambda i = i: requiredPracticalSubroutines[i](mainFrame))
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
    
    xTitle = Label(master = dataFrame, width = 12, height = 4, bg = darkGrey, text = xEntryTitle, font = ('Arial Bold', 8), justify = CENTER)
    yTitle = Label(master = dataFrame, width = 12, height = 4, bg = darkGrey, text = yEntryTitle, font = ('Arial Bold', 8), justify = CENTER)
    
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
    
    axes.scatter(x, y, marker = "+", color = "black", s = 100) # Displays the new updated graph
    
    gradientString.set("Gradient: Unavailable") # Sets the string variables to unavailable, changes if they are available
    interceptString.set("y-intercept: Unavailable")
    
    if len(x) > 1 and len(y) > 1: # Draws gradient and changes string variables if applicable
        gradient, intercept = np.polyfit(x, y, 1)
        axes.plot(x, gradient * x + intercept, linestyle = "--", linewidth = 1)
        gradientString.set(f"Gradient: {str(gradient)}")
        interceptString.set(f"y-intercept: {str(intercept)}")
        
    
    if len(x) == 1 and x[0] == 0: # If there is no entry, set the x and y limits to 10 as placeholder
        axes.set_xlim([0, 10])
        axes.set_ylim([0, 10])
    else: # Otherwise set the x and y limits to 1.1x the largest values
        axes.set_xlim([0, np.max(x) * 1.1])
        axes.set_ylim([0, np.max(y) * 1.1])
    
    canvas.draw() # Draw the canvas

def openRP1(mainFrame):
    xAxis = "1 / Length (1 / m)" # String for x axis
    yAxis = "Frequency (Hz)" # String for y axis
    
    xEntryTitle = "Length (m)" # String to tell user what to enter for x
    yEntryTitle = "Frequency (Hz)" #  # String to tell user what to enter for y
    
    originalEquation = "λ = 2L" # String for original equation
    linearisedEquation = "f = (v/2)(1/L)" # String for linearised equation
    
    mode = 1 # Mode is 1, meaning x will be 1 / x instead. If nothing special happens to entries, keep the mode as 0
    
    # PAST THIS NOTHING CHANGES ---------------------------------------------------------------------------------------
    
    destroyFrames(mainFrame) # Destroys all other frames
    
    RPFrame = Frame(master = mainFrame, width = 880, height = 720, bd = 2, relief = "groove")
    
    figure, axes, canvas = createGraph(RPFrame, xAxis, yAxis) # Creates the graph
    
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
    
    createDataEntryFrame(RPFrame, xEntryTitle, yEntryTitle, mode, axes, canvas, xAxis, yAxis, gradientString, interceptString) # Creates data entry
    
    RPFrame.pack()
    
def openRP2(mainFrame):
    xAxis = "Distance from slit to screen (m)"
    yAxis = "Distance between each fringe (m)"
    
    xEntryTitle = "Slit screen distance (m)"
    yEntryTitle = "Fringe spacing (m)"
    
    originalEquation = "w = λD/s"
    linearisedEquation = "w = (λ/s)D"
    
    mode = 0
    
    destroyFrames(mainFrame)
    
    RPFrame = Frame(master = mainFrame, width = 880, height = 720, bd = 2, relief = "groove")
    
    figure, axes, canvas = createGraph(RPFrame, xAxis, yAxis)
    
    rpInfoFrame = Frame(master = RPFrame, width = 602, height = 178, bg = darkGrey, bd = 2, relief = "groove")
    rpInfoFrame.place(relx = 1, rely = 1, x = -10, y = -10, anchor = SE)
    
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
    
    createDataEntryFrame(RPFrame, xEntryTitle, yEntryTitle, mode, axes, canvas, xAxis, yAxis, gradientString, interceptString)
    
    RPFrame.pack()

def openRP3(mainFrame):
    xAxis = "Time (s)"
    yAxis = "Height x 2 / Time (m/s)"
    
    xEntryTitle = "Time (s)"
    yEntryTitle = "2h/t (m/s)"
    
    originalEquation = "s = ut + 1/2(at)²"
    linearisedEquation = "2h/t = gt + 2u"
    
    mode = 0
    
    destroyFrames(mainFrame)
    
    RPFrame = Frame(master = mainFrame, width = 880, height = 720, bd = 2, relief = "groove")
    
    figure, axes, canvas = createGraph(RPFrame, xAxis, yAxis)
    
    rpInfoFrame = Frame(master = RPFrame, width = 602, height = 178, bg = darkGrey, bd = 2, relief = "groove")
    rpInfoFrame.place(relx = 1, rely = 1, x = -10, y = -10, anchor = SE)
    
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
    
    createDataEntryFrame(RPFrame, xEntryTitle, yEntryTitle, mode, axes, canvas, xAxis, yAxis, gradientString, interceptString)
    
    RPFrame.pack()


def openRP4(mainFrame):
    xAxis = "Change in length (m)"
    yAxis = "Force (N)"
    
    xEntryTitle = "ΔL (m)"
    yEntryTitle = "Force (N)"
    
    originalEquation = "Young Modulus = Tensile stress / Tensile strain"
    linearisedEquation = "F = (Young Modulus x A / L)ΔL"
    
    mode = 0
    
    destroyFrames(mainFrame)
    
    RPFrame = Frame(master = mainFrame, width = 880, height = 720, bd = 2, relief = "groove")
    
    figure, axes, canvas = createGraph(RPFrame, xAxis, yAxis)
    
    rpInfoFrame = Frame(master = RPFrame, width = 602, height = 178, bg = darkGrey, bd = 2, relief = "groove")
    rpInfoFrame.place(relx = 1, rely = 1, x = -10, y = -10, anchor = SE)
    
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
    
    createDataEntryFrame(RPFrame, xEntryTitle, yEntryTitle, mode, axes, canvas, xAxis, yAxis, gradientString, interceptString)
    
    RPFrame.pack()


def openRP5(mainFrame):
    xAxis = "Length of wire (m)"
    yAxis = "Resistance (Ω)"
    
    xEntryTitle = "Length (m)"
    yEntryTitle = "Resistance (Ω)"
    
    originalEquation = "ρ = RA/L"
    linearisedEquation = "R = (ρ/A)L"
    
    mode = 0
    
    destroyFrames(mainFrame)
    
    RPFrame = Frame(master = mainFrame, width = 880, height = 720, bd = 2, relief = "groove")
    
    figure, axes, canvas = createGraph(RPFrame, xAxis, yAxis)
    
    rpInfoFrame = Frame(master = RPFrame, width = 602, height = 178, bg = darkGrey, bd = 2, relief = "groove")
    rpInfoFrame.place(relx = 1, rely = 1, x = -10, y = -10, anchor = SE)
    
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
    
    createDataEntryFrame(RPFrame, xEntryTitle, yEntryTitle, mode, axes, canvas, xAxis, yAxis, gradientString, interceptString)
    
    RPFrame.pack()

def openRP6(mainFrame):
    xAxis = "Current (A)"
    yAxis = "Voltage (V)"
    
    xEntryTitle = "Current (A)"
    yEntryTitle = "Voltage (V)"
    
    originalEquation = "E = I(R + r)"
    linearisedEquation = "V = (-r)I + E"
    
    mode = 0
    
    destroyFrames(mainFrame)
    
    RPFrame = Frame(master = mainFrame, width = 880, height = 720, bd = 2, relief = "groove")
    
    figure, axes, canvas = createGraph(RPFrame, xAxis, yAxis)
    
    rpInfoFrame = Frame(master = RPFrame, width = 602, height = 178, bg = darkGrey, bd = 2, relief = "groove")
    rpInfoFrame.place(relx = 1, rely = 1, x = -10, y = -10, anchor = SE)
    
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
    
    createDataEntryFrame(RPFrame, xEntryTitle, yEntryTitle, mode, axes, canvas, xAxis, yAxis, gradientString, interceptString)
    
    RPFrame.pack()

def openRP7(mainFrame):
    print("COME BACK TO THIS")

def openRP8(mainFrame):
    print("COME BACK TO THIS")

def openRP9(mainFrame):
    xAxis = "Time (s)"
    yAxis = "ln(V)"
    
    xEntryTitle = "Time (s)"
    yEntryTitle = "Voltage (V)"
    
    originalEquation = "V = V₀e^(-t/RC)"
    linearisedEquation = "ln(V) = (-1/RC)t + ln(V₀)"
    
    mode = 2
    
    destroyFrames(mainFrame)
    
    RPFrame = Frame(master = mainFrame, width = 880, height = 720, bd = 2, relief = "groove")
    
    figure, axes, canvas = createGraph(RPFrame, xAxis, yAxis)
    
    rpInfoFrame = Frame(master = RPFrame, width = 602, height = 178, bg = darkGrey, bd = 2, relief = "groove")
    rpInfoFrame.place(relx = 1, rely = 1, x = -10, y = -10, anchor = SE)
    
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
    
    createDataEntryFrame(RPFrame, xEntryTitle, yEntryTitle, mode, axes, canvas, xAxis, yAxis, gradientString, interceptString)
    
    RPFrame.pack()

def openRP10(mainFrame):
    xAxis = "Current (A)"
    yAxis = "Mass (kg)"
    
    xEntryTitle = "Current (A)"
    yEntryTitle = "Mass (kg)"
    
    originalEquation = "F = nBIL"
    linearisedEquation = "m = (nBL/g)I"
    
    mode = 0
    
    destroyFrames(mainFrame)
    
    RPFrame = Frame(master = mainFrame, width = 880, height = 720, bd = 2, relief = "groove")
    
    figure, axes, canvas = createGraph(RPFrame, xAxis, yAxis)
    
    rpInfoFrame = Frame(master = RPFrame, width = 602, height = 178, bg = darkGrey, bd = 2, relief = "groove")
    rpInfoFrame.place(relx = 1, rely = 1, x = -10, y = -10, anchor = SE)
    
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
    
    createDataEntryFrame(RPFrame, xEntryTitle, yEntryTitle, mode, axes, canvas, xAxis, yAxis, gradientString, interceptString)
    
    RPFrame.pack()


def openRP11(mainFrame):
    xAxis = "cos(θ)"
    yAxis = "ε₀ (V)"
    
    xEntryTitle = "Angle (θ)"
    yEntryTitle = "Peak emf (V)"
    
    originalEquation = "ε = -B₀ANωsin(ωt)cos(θ)"
    linearisedEquation = "ε₀ = B₀ANωcos(θ)"
    
    mode = 3
    
    destroyFrames(mainFrame)
    
    RPFrame = Frame(master = mainFrame, width = 880, height = 720, bd = 2, relief = "groove")
    
    figure, axes, canvas = createGraph(RPFrame, xAxis, yAxis)
    
    rpInfoFrame = Frame(master = RPFrame, width = 602, height = 178, bg = darkGrey, bd = 2, relief = "groove")
    rpInfoFrame.place(relx = 1, rely = 1, x = -10, y = -10, anchor = SE)
    
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
    
    createDataEntryFrame(RPFrame, xEntryTitle, yEntryTitle, mode, axes, canvas, xAxis, yAxis, gradientString, interceptString)
    
    RPFrame.pack()

def openRP12(mainFrame):
    print("")

root = Tk()
main()
