from enum import Enum
import keyboard
import string
from colorama import Back, Cursor, Style
from colorama.ansi import clear_screen

DIMX = 20
DIMY = 20

# ← 4
# → 6
# ↑  8
# ↓  2
def getch():
    alphabet = list(string.ascii_lowercase)
    while True:
        for letter in alphabet: # detect when a letter is pressed
            if keyboard.is_pressed(letter):
                return letter
        for num in range(10): # detect numbers 0-9
            if keyboard.is_pressed(str(num)):
                return str(num)

def clearConsole():
    print(clear_screen(),end='')

class Directions(Enum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3

class Point:
    x: int
    y: int
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def isHere(self, x, y):
        return self.x == x and self.y == y
    
    def getCoordAfterMove(self, dir: Directions):
        match dir:
            case Directions.Up:
                return Point(self.x, self.y - 1)
            case Directions.Right:
                return Point(self.x + 1, self.y)
            case Directions.Down:
                return Point(self.x, self.y + 1)
            case Directions.Left:
                return Point(self.x - 1, self.y)
    
    def isInRectangle(self, width, height):
        return (self.x >= 0 and self.x < width) and (self.y >= 0 and self.y < height)