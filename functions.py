from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

# Constants for colour

darkGrey = '#ababab'
lightGreen = '#bfffd7'
lightRed = '#ffbfbf'


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