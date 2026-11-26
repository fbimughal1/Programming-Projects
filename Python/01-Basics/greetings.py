RED =   '\033[91m'
GREEN = '\033[92m'
COLOR3 = '\033[93m'
COLOR4 = '\033[94m'

RESET = '\033[0m'

def ShowGreeting():
    print("Welcome to Pakistan!")

def ShowInColor(text, color):
    print(f'\033[{90+color}m{text}\033[0m')


def Calculate_Area(radius):
    area = 3.14 * radius * radius
    return area

ShowGreeting()
ShowInColor('Welcome to the Colorful Text Display Program!', 2)

radius = float(input("Enter the radius of the circle: "))
area = Calculate_Area(radius)
print(f"The area of the circle with radius {radius} is: {area}")



