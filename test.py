import keyboard
import string
import random
import math
import time
import os
from colorama import init, Cursor, Fore, Back, Style
init()

def clear():
    os.system('cls')

class Point:
    x: int
    y: int
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def isHere(self, x, y):
        return self.x == x and self.y == y

class Player:
    pos: Point
    
    def __init__(self, pos):
        self.pos = pos

    def move(self, direction):
        match direction:
            case 0:
                self.pos.y -= 1
            case 1:
                self.pos.x += 1
            case 2:
                self.pos.y += 1
            case 3:
                self.pos.x -= 1

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

def createRoom(dimx, dimy, direction = -1):
    room = [ [0]*dimy for i in range(dimx) ]
    
    if direction < 0:
        doorDir = random.randint(0,3)
    else:
        doorDir = direction
    
    doorX = 0
    doorY = 0
    match doorDir:
        case 0:
            doorX = math.ceil(dimx/2) - 1
            doorY = 0
        case 1:
            doorX = dimx - 1
            doorY = math.ceil(dimy/2) - 1
        case 2:
            doorX = math.ceil(dimx/2) - 1
            doorY = dimy - 1
        case 3:
            doorX = 0
            doorY = math.ceil(dimy/2) - 1
    
    for x in range(len(room)):
        for y in range(len(room[0])):
            if (x > 0) and (x < dimx - 1) and (y > 0) and (y < dimy -1):
                room[x][y] = 1
            else:
                room[x][y] = 0
            
            if (x == doorX) and (y == doorY):
                room[x][y] = 1
    
    return room

def displayRoom(room, player: Player):
    ret = ""
    for x in range(len(room)):
        for y in range(len(room[0])):
            if player.pos.isHere(x, y):
                print(Cursor.POS(x + 1, y + 1) + "@")
                continue
            
            match room[x][y]:
                case 0:
                    print(Cursor.POS(x + 1, y + 1) + "#")
                case 1:
                    print(Cursor.POS(x + 1, y + 1) + ".")
                case _:
                    print(Cursor.POS(x + 1, y + 1) + " ")
            
            print(Cursor.POS(-x - 1, -y - 1))
    print(Cursor.POS(0, len(room[0]) + 1) + Style.RESET_ALL)

def main():
    dimx = 8
    dimy = 8
    
    player = Player(Point(3, 3))
    
    doorDir = -1
    room = createRoom(dimx, dimy, doorDir)
    while True:
        
        clear()
        displayRoom(room, player)
        key = ""
        
        while not key in ["q", "2", "4", "6", "8"]:
            key = getch()
        
        match key:
            case "8": # Up
                player.move(0)
            case "6": # Right
                player.move(1)
            case "2": # Down
                player.move(2)
            case "4": # Left
                player.move(3)
            case "q":
                break
        
        time.sleep(0.2)

main()