from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

darkGrey = '#ababab'
lightGreen = '#bfffd7'
lightRed = '#ffbfbf'

requiredPracticalList = ["RP1 Stationary Waves on a String", "RP2 Interference Effects", "RP3 Determination of g", "RP4 Determination of Young's Modulus", "RP5 Determination of Resistivity of a Wire", "RP6 Internal resistance and emf", "RP7 Simple Harmonic Motion", "RP8 Boyle's Law", "RP9 Charging and Discharging Capacitors", "RP10 Magnetic Force on a Wire", "RP11 Magnetic Flux Linkage", "RP12 Inverse Square Law"]

x = np.array([0])
y = np.array([0])
gradient = "Unavailable"
intercept = "Unavailable"
rowIndex = 1

def main():
    
    root.title("Physics RP Plus")
    root.minsize(1080, 720)
    root.geometry("1080x720")
    
    root.rowconfigure(0, weight = 1)
    root.columnconfigure(0, weight = 2)
    root.columnconfigure(1, weight = 8)
    
    sideBar = Frame(master = root, width = 200, height = 720, bd = 2, relief = "groove", bg = darkGrey)
    sideBar.grid(row = 0, column = 0, sticky = "nsew")
    
    sideBarTitle = Label(master = sideBar, width = 20, height = 3, text = "Physics RP Plus", bg = darkGrey, font = ('Arial', 12))
    sideBarTitle.place(relx = 0.5, rely = 0.05, anchor = CENTER)
    
    sideBarButtonFrame = Frame(master = sideBar, width = 150, height = 625, bd = 2, relief = "groove", bg = darkGrey)
    sideBarButtonFrame.place(relx = 0.5, rely = 0.525, anchor = CENTER)
    
    mainFrame = Frame(master = root, width = 880, height = 720, bd = 2, relief = "groove")
    mainFrame.grid(row = 0, column = 1, sticky = "nsew")
    
    welcomeFrame = Frame(master = mainFrame, width = 880, height = 720, bd = 2, relief = "groove")
    
    titleText = Label(master = welcomeFrame, width = 20, height = 2, text = "Physics RP Plus", font = ('Arial Bold', 45))
    titleText.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    
    contributors = Label(master = welcomeFrame, width = 45, height = 2, text = "Developed by Brandon Jake Nuñez and Fahad Wasim", font = ('Arial', 15))
    contributors.place(relx = 0.5, rely = 0.6, anchor = CENTER)
    
    welcomeFrame.pack()
    
    requiredPracticalSubroutines = [openRP1, openRP2, openRP3, openRP4, openRP5, openRP6, openRP7, openRP8, openRP9, openRP10, openRP11, openRP12]
    
    for i in range(0,12):
        newSideBarButton = Button(master = sideBarButtonFrame, width = 20, height = 2, bd = 2, relief = "raised", text = requiredPracticalList[i], wraplength = 125, command = lambda i = i: requiredPracticalSubroutines[i](mainFrame))
        newSideBarButton.grid(row = i, column = 0, padx = 5, pady = 5)
    
    root.mainloop()

def destroyFrames(mainFrame):
    for frame in mainFrame.winfo_children():
        frame.destroy()

def createGraph(currentFrame, xLabel, yLabel):
    global x
    global y
    global gradient
    global intercept
    global rowIndex
    
    graphHolder = Frame(master = currentFrame, width = 550, height = 500, bg = 'black')
    graphHolder.place(relx = 1, rely = 0, x = -10, y = 10, anchor = NE)
    
    figure, axes = plt.subplots(figsize = (6, 5))
    axes.set_ylabel(yLabel)
    axes.set_xlabel(xLabel)
    figure.tight_layout()
    
    canvas = FigureCanvas(figure, master = graphHolder)
    canvas.get_tk_widget().pack(padx = 1, pady = 1)
    
    x = np.array([0])
    y = np.array([0])
    gradient = "Unavailable"
    intercept = "Unavailable"
    rowIndex = 1
    
    axes.scatter(x, y, marker = "+", color = "black", s = 100)
    
    axes.set_xlim([0, 10])
    axes.set_ylim([0, 10])
    
    canvas.draw()
    
    return figure, axes, canvas

def createDataEntryFrame(RPFrame, xEntryTitle, yEntryTitle, mode, axes, canvas, xAxis, yAxis):
    dataFrame = Frame(master = RPFrame, width = 240, height = 503, bg = darkGrey, bd = 2, relief = "groove")
    dataFrame.place(relx = 0, rely = 0, x = 10, y = 10)
    
    xTitle = Label(master = dataFrame, width = 12, height = 4, bg = darkGrey, text = xEntryTitle, font = ('Arial Bold', 8), justify = CENTER)
    yTitle = Label(master = dataFrame, width = 12, height = 4, bg = darkGrey, text = yEntryTitle, font = ('Arial Bold', 8), justify = CENTER)
    
    xTitle.place(x = 10, y = 0)
    yTitle.place(x = 110, y = 0)
    
    dataEntryFrame = Frame(master = dataFrame, width = 216, height = 430, bg = darkGrey)
    dataEntryFrame.place(x = 10, y = 40)
    
    dataEntry = Frame(master = dataEntryFrame, width = 216, height = 20, bg = darkGrey)
    xEntry = Entry(master = dataEntry)
    yEntry = Entry(master = dataEntry)
    addButton = Button(master = dataEntry, height = 20, width = 20, text = "", bg = lightGreen, justify = CENTER, command = lambda: refreshGraph(axes, canvas, xEntry.get(), yEntry.get(), dataEntry, addButton, dataEntryFrame, xAxis, yAxis, mode))
    xEntry.place(x = 0, y = 0, width = 90, height = 20)
    yEntry.place(x = 100, y = 0, width = 90, height = 20)
    addButton.place(x = 196, y = 0)
    dataEntry.grid(row = 0, column = 0, pady = 3)

def refreshGraph(axes, canvas, newX, newY, entryFrame, entryButton, entryListFrame, xLabel, yLabel, mode):
    
    global x
    global y
    global gradient
    global intercept
    global rowIndex
    
    try:
        newX = float(newX)
        newY = float(newY)
        if mode == 1:
            newX = 1 / float(newX)
    except:
        return ""
    
    axes.cla()
    
    axes.set_ylabel(yLabel)
    axes.set_xlabel(xLabel)
    
    if newX in x and newY in y:
        entryFrame.destroy()
        if len(x) == 1:
            x = np.array([0])
            y = np.array([0])
        else:
            indexX = np.where(x == newX)[0][0]
            indexY = np.where(y == newY)[0][0]
            x = np.delete(x, indexX)
            y = np.delete(y, indexY)
    elif len(x) == 1 and x[0] == 0:
        mode = 0
        
        if xLabel == "1 / Length (1 / m)":
            mode = 1
        
        entryButton.config(bg = lightRed)
        x = np.array([newX])
        y = np.array([newY])
        
        dataEntry = Frame(master = entryListFrame, width = 216, height = 20, bg = darkGrey)
        xEntry = Entry(master = dataEntry)
        yEntry = Entry(master = dataEntry)
        addButton = Button(master = dataEntry, height = 20, width = 20, text = "", bg = lightGreen, justify = CENTER, command = lambda: refreshGraph(axes, canvas, xEntry.get(), yEntry.get(), dataEntry, addButton, entryListFrame, xLabel, yLabel, mode))
        xEntry.place(x = 0, y = 0, width = 90, height = 20)
        yEntry.place(x = 100, y = 0, width = 90, height = 20)
        addButton.place(x = 196, y = 0)
        dataEntry.grid(row = rowIndex, column = 0, pady = 3)
        rowIndex += 1
    elif len(x) == 16:
        return ""
    else:
        mode = 0
        
        if xLabel == "1 / Length (1 / m)":
            mode = 1
        
        entryButton.config(bg = lightRed)
        x = np.append(x, [newX])
        y = np.append(y, [newY])
        
        dataEntry = Frame(master = entryListFrame, width = 216, height = 20, bg = darkGrey)
        xEntry = Entry(master = dataEntry)
        yEntry = Entry(master = dataEntry)
        addButton = Button(master = dataEntry, height = 20, width = 20, text = "", bg = lightGreen, justify = CENTER, command = lambda: refreshGraph(axes, canvas, xEntry.get(), yEntry.get(), dataEntry, addButton, entryListFrame, xLabel, yLabel, mode))
        xEntry.place(x = 0, y = 0, width = 90, height = 20)
        yEntry.place(x = 100, y = 0, width = 90, height = 20)
        addButton.place(x = 196, y = 0)
        dataEntry.grid(row = rowIndex, column = 0, pady = 3)
        rowIndex += 1
    
    axes.scatter(x, y, marker = "+", color = "black", s = 100)
    
    gradient = "Unavailable"
    intercept = "Unavailable"
    
    if len(x) > 1 and len(y) > 1:
        gradient, intercept = np.polyfit(x, y, 1)
        axes.plot(x, gradient * x + intercept, linestyle = "--", linewidth = 1)
    
    if len(x) == 1 and x[0] == 0:
        axes.set_xlim([0, 10])
        axes.set_ylim([0, 10])
    else:
        axes.set_xlim([0, np.max(x) * 1.1])
        axes.set_ylim([0, np.max(y) * 1.1])
    
    canvas.draw()

def openRP1(mainFrame):
    xAxis = "1 / Length (1 / m)"
    yAxis = "Frequency (Hz)"
    
    xEntryTitle = "Length (m)"
    yEntryTitle = "Frequency (Hz)"
    
    mode = 1
    
    destroyFrames(mainFrame)
    
    RPFrame = Frame(master = mainFrame, width = 880, height = 720, bd = 2, relief = "groove")
    
    figure, axes, canvas = createGraph(RPFrame, xAxis, yAxis)
    
    createDataEntryFrame(RPFrame, xEntryTitle, yEntryTitle, mode, axes, canvas, xAxis, yAxis)
    
    rpInfoFrame = Frame(master = RPFrame, width = 602, height = 178, bg = darkGrey, bd = 2, relief = "groove")
    rpInfoFrame.place(relx = 1, rely = 1, x = -10, y = -10, anchor = SE)
    
    originalEquation = Label(master = rpInfoFrame, width = 27, height = 4, bg = darkGrey, bd = 0, text = "Original: λ = 2l", font = ('Arial', 14))
    linearisedEquation = Label(master = rpInfoFrame, width = 27, height = 4, bg = darkGrey, bd = 0, text = "Linearised: ", font = ('Arial', 14))
    gradientLabel = Label(master = rpInfoFrame, width = 27, height = 4, bg = darkGrey, bd = 0, text = "Gradient: ", font = ('Arial', 14))
    interceptLabel = Label(master = rpInfoFrame, width = 27, height = 4, bg = darkGrey, bd = 0, text = "y-intercept: ", font = ('Arial', 14))
    
    originalEquation.grid(row = 0, column = 0)
    linearisedEquation.grid(row = 0, column = 1)
    gradientLabel.grid(row = 1, column = 0)
    interceptLabel.grid(row = 1, column = 1)
    
    RPFrame.pack()
    
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

