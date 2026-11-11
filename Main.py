from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

# Constants for colour

darkGrey = '#ababab'
lightGreen = '#bfffd7'
lightRed = '#ffbfbf'
darkRed = '#b50f00'
darkGreen = '#027500'
darkBlue = '#005969'

# List of RPs for side menu buttons

requiredPracticalList = ["RP1 Stationary Waves on a String", "RP2 Interference Effects", "RP3 Determination of g", "RP4 Determination of Young's Modulus", "RP5 Determination of Resistivity of a Wire", "RP6 Internal resistance and emf", "RP7 Simple Harmonic Motion", "RP8 Boyle's Law", "RP9 Charging and Discharging Capacitors", "RP10 Magnetic Force on a Wire", "RP11 Magnetic Flux Linkage", "RP12 Inverse Square Law"]

from rp_data import hashGet # Practical data lookup (shared with hashing.py)
from transforms import transform_point # Linearises a reading according to the practical's mode
from points import remove_point # Removes one (x, y) reading from the plotted arrays


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
        rp = hashGet(requiredPracticalList[i]) # Looked up once per button; the dict's xAxis/yAxis are the graph labels, the entry titles are the raw readings
        newSideBarButton = Button(master = sideBarButtonFrame, width = 20, height = 2, bd = 2, relief = "raised", text = requiredPracticalList[i], wraplength = 125, command = lambda rp = rp: openRP(mainFrame, rp["xAxis"], rp["yAxis"], rp["xEntryTitle"], rp["yEntryTitle"], rp["originalEquation"], rp["linearisedEquation"], rp["mode"]))
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
    
    # Creates the first data entry row (gridded at row 0)
    
    createEntryRow(dataEntryFrame, 0, axes, canvas, xAxis, yAxis, mode, gradientString, interceptString)

def createEntryRow(entryListFrame, row, axes, canvas, xLabel, yLabel, mode, gradientString, interceptString): # Creates one data-entry row (x entry, y entry, add/remove button) gridded at `row`
    
    dataEntry = Frame(master = entryListFrame, width = 216, height = 20, bg = darkGrey)
    xEntry = Entry(master = dataEntry)
    yEntry = Entry(master = dataEntry)
    # The button will refresh the graph with the new entries (and turns red once the entry is added, so pressing it again removes it)
    addButton = Button(master = dataEntry, height = 20, width = 20, text = "", bg = lightGreen, justify = CENTER, command = lambda: refreshGraph(axes, canvas, xEntry.get(), yEntry.get(), dataEntry, addButton, entryListFrame, xLabel, yLabel, mode, gradientString, interceptString))
    xEntry.place(x = 0, y = 0, width = 90, height = 20)
    yEntry.place(x = 100, y = 0, width = 90, height = 20)
    addButton.place(x = 196, y = 0)
    dataEntry.grid(row = row, column = 0, pady = 3)

def refreshGraph(axes, canvas, newX, newY, entryFrame, entryButton, entryListFrame, xLabel, yLabel, mode, gradientString, interceptString): # Refreshes the graph with the new data
    
    # Retrieves global variables
    
    global x
    global y
    global rowIndex
    
    removing = entryButton.cget("bg") == lightRed # A red button belongs to a row that has been added, so pressing it removes that reading
    
    if not removing: # Tries to convert user input into numbers, if it cannot then it does nothing
        try:
            newX, newY = transform_point(newX, newY, mode) # Mode 1 applies 1 / x, mode 2 ln(y), mode 3 cos(x) (see transforms.py)
        except:
            return ""
    
    axes.cla() # Clears current axes
    
    axes.set_ylabel(yLabel) # Re-adds current labels
    axes.set_xlabel(xLabel)
    
    if removing:
        entryFrame.destroy() # Deletes the entry frame as it was removed
        if len(x) == 1: # If it is the only entry, it resets the graph
            x = np.array([0])
            y = np.array([0])
        else: # Otherwise it removes the (x, y) pair that this row added (remembered on the button, so editing the boxes afterwards can't remove the wrong reading)
            x, y = remove_point(x, y, *entryButton.addedPoint)
    elif len(x) == 1 and x[0] == 0: # If there is no other data (x only has one entry, 0) and data is added
        
        entryButton.config(bg = lightRed) # Changes the button colour to red, indicating that pressing it will remove the data entry
        entryButton.addedPoint = (newX, newY) # Remembers which reading this row added, so removal matches the pair exactly
        x = np.array([newX]) # Replaces the x and y arrays with the new entry, since there is only one entry
        y = np.array([newY])
        
        # Creates the next empty row for new entries
        
        createEntryRow(entryListFrame, rowIndex, axes, canvas, xLabel, yLabel, mode, gradientString, interceptString)
        rowIndex += 1 # Places it at the new row, and adds one to the row index
    elif len(x) == 16: # If there are max entries, do nothing
        return ""
    else:
        
        # Does the exact same as previous condition, except appends the new values to the x and y arrays
        
        entryButton.config(bg = lightRed)
        entryButton.addedPoint = (newX, newY)
        x = np.append(x, [newX])
        y = np.append(y, [newY])
        
        createEntryRow(entryListFrame, rowIndex, axes, canvas, xLabel, yLabel, mode, gradientString, interceptString)
        rowIndex += 1
    
    axes.scatter(x, y, marker = "+", color = "black", s = 100) # Displays the new updated graph
    
    gradientString.set("Unavailable") # Sets the string variables to unavailable, changes if they are available
    interceptString.set("Unavailable")
    
    if len(x) > 1 and len(y) > 1: # Draws gradient and changes string variables if applicable
        gradient, intercept = np.polyfit(x, y, 1)
        axes.plot(x, gradient * x + intercept, linestyle = "--", linewidth = 1)
        gradientString.set(f"{str(gradient)}")
        interceptString.set(f"{str(intercept)}")
        
    
    if len(x) == 1 and x[0] == 0: # If there is no entry, set the x and y limits to 10 as placeholder
        axes.set_xlim([0, 10])
        axes.set_ylim([0, 10])
    else: # Otherwise set the x and y limits to 1.1x the largest values
        axes.set_xlim([0, np.max(x) * 1.1])
        axes.set_ylim([0, np.max(y) * 1.1])
    
    canvas.draw() # Draw the canvas
    
def openRP(mainFrame, xAxis, yAxis, xEntryTitle, yEntryTitle, originalEquation, linearisedEquation, mode): # xAxis / yAxis are the graph axis labels (already linearised, e.g. "1 / Length"); the entry titles describe the raw readings
    destroyFrames(mainFrame)
    
    RPFrame = Frame(master = mainFrame, width = 880, height = 720, bd = 2, relief = "groove")
    
    figure, axes, canvas = createGraph(RPFrame, xAxis, yAxis)
    
    rpInfoFrame = Frame(master = RPFrame, width = 602, height = 178, bg = darkGrey, bd = 2, relief = "groove")
    rpInfoFrame.place(relx = 1, rely = 1, x = -10, y = -10, anchor = SE)
    
    gradientString = StringVar(master = rpInfoFrame, value = "Unavailable")
    interceptString = StringVar(master = rpInfoFrame, value = "Unavailable")
    
    originalEquationTitle = Label(master = rpInfoFrame, width = 27, height = 2, bg = darkGrey, bd = 0, text = "Original:", font = ('Arial Bold', 13), fg = darkRed)
    originalEquation = Label(master = rpInfoFrame, width = 27, height = 2, bg = darkGrey, bd = 0, text = originalEquation, font = ('Arial', 14))
    
    linearisedEquationTitle = Label(master = rpInfoFrame, width = 27, height = 2, bg = darkGrey, bd = 0, text = "Linearised:", font = ('Arial Bold', 13), fg = darkGreen)
    linearisedEquation = Label(master = rpInfoFrame, width = 27, height = 2, bg = darkGrey, bd = 0, text = linearisedEquation, font = ('Arial', 14))
    
    gradientTitle = Label(master = rpInfoFrame, width = 27, height = 2, bg = darkGrey, bd = 0, text = "Gradient:", font = ('Arial Bold', 13), fg = darkBlue)
    gradientLabel = Label(master = rpInfoFrame, width = 27, height = 2, bg = darkGrey, bd = 0, textvariable = gradientString, font = ('Arial', 14))
    
    interceptTitle = Label(master = rpInfoFrame, width = 27, height = 2, bg = darkGrey, bd = 0, text = "y-intercept:", font = ('Arial Bold', 13), fg = darkBlue)
    interceptLabel = Label(master = rpInfoFrame, width = 27, height = 2, bg = darkGrey, bd = 0, textvariable = interceptString, font = ('Arial', 14))
    
    originalEquationTitle.grid(row = 0, column = 0)
    linearisedEquationTitle.grid(row = 0, column = 1)
    
    originalEquation.grid(row = 1, column = 0)
    linearisedEquation.grid(row = 1, column = 1)
    
    gradientTitle.grid(row = 2, column = 0)
    interceptTitle.grid(row = 2, column = 1)
    
    gradientLabel.grid(row = 3, column = 0)
    interceptLabel.grid(row = 3, column = 1)
    
    createDataEntryFrame(RPFrame, xEntryTitle, yEntryTitle, mode, axes, canvas, xAxis, yAxis, gradientString, interceptString)
    
    RPFrame.pack()

if __name__ == "__main__": # Only open the window when run directly, so the module can be imported (e.g. by tests)
    root = Tk()
    main()
