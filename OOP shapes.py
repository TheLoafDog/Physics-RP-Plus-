class shape():
    def __init__(self, name, length):
        self.name = name
        self.length = length
        
    def getName(self):
        return(self.name)

    def getLength(self):
        return(self.length)

    def setLength(self):
        self.length = int(input("Length is: "))

    def calcArea(self, length):
        area = length * length
        return area

class rectangle(shape):
    def __init__(self,name,length, width):
        shape.__init__(self,name,length)
        rectangle.width = width

    def setWidth(self):
        self.width = int(input("Width is: "))

    def calcArea(self, length, width):
        area = length * width
        return area

class circle(shape):
    def __init__(self,name,length):
        shape.__init__(self,name,length)

    def calcArea(self, length):
        π = 3.141592653589793238462643
        area = π * length * length
        return area

def options():
    for i in shapes:
        print(shapes.index(i)+1, ") ", i.name, "\n")
    ans = int(input("Pick a shape: "))
    return ans

def options_2():
    print("1) Change dimensions of shape \n")
    print("2) Display dimension and area \n")
    ans = int(input("Input: "))
    return ans



square = rectangle("square",5, 5)
rectangle = rectangle("rectangle",3,5)
circle = circle("circle",5)

shapes = [square, circle, rectangle]


print("MENU \n")

shape = shapes[options() - 1]
print("")

if options_2() == 1:
    shape.setLength()
    if shape == rectangle:
        shape.setWidth()
    elif shape == square:
        shape.width = shape.length
    
    
print(shape.length)
if shape == rectangle:
    print(shape.width)
    print(shape.calcArea(shape.length, shape.width))
else:
    print(shape.calcArea(shape.length))

#this is not robust so inputs invalid inputs may or may not work




