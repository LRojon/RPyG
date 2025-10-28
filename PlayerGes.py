from Utils import Point, Directions, DIMY, DIMX
from WorldGen import World, Chunk, Tiles
from colorama import Back, Fore, Cursor, Style
import math

class Player:
    
    def __init__(self, name, pos, worldPos, canWalkMountain = False, canWalkWater = False):
        self.pos : Point = pos
        self.worldPos : Point = worldPos
        self.canWalkMountain : bool = canWalkMountain
        self.canWalkWater : bool = canWalkWater
        self.name = name
        self.force = 1
        self.defense = 1
        self.vitesse = 1
        self.lvl = 1
        self.xp = 0
        self.skillPts = 0
        self.strPts = 0
        self.defPts = 0
        self.spePts = 0
    
    def getMaxXp(self):
        return self.lvl * 100
    
    def addXP(self, amount):
        maxXP = self.getMaxXp()
        self.xp += amount
        if self.xp >= maxXP:
            self.xp -= maxXP
            self.lvl += 1

    def canMove(self, direction: Directions, world: World) -> int:

        nextPos: Point = Point(self.pos.x, self.pos.y)
        nextWorldPos: Point = Point(self.worldPos.x, self.worldPos.y)
        match direction:
            case Directions.Up:
                nextPos.y -= 1
                if nextPos.y < 0:
                    nextWorldPos.y -= 1
            case Directions.Right:
                nextPos.x += 1
                if nextPos.x >= DIMX:
                    nextWorldPos.x += 1
            case Directions.Down:
                nextPos.y += 1
                if nextPos.y >= DIMY:
                    nextWorldPos.y += 1
            case Directions.Left:
                nextPos.x -= 1
                if nextPos.x < 0:
                    nextWorldPos.x -= 1
        chunk: Chunk = world.world[self.worldPos.x][self.worldPos.y]
        if not nextPos.isInRectangle(len(chunk.map), len(chunk.map[0])):
            if nextWorldPos.isInRectangle(len(world.world), len(world.world[0])):
                return 2
            else:
                return 0
        if (not self.canWalkMountain) and chunk.map[nextPos.x][nextPos.y] == Tiles.mountain:
            return 0
        if (not self.canWalkWater) and chunk.map[nextPos.x][nextPos.y] == Tiles.water:
            return 0
        
        return 1

    def move(self, dir: Directions, world: World):
        canMoveResult = self.canMove(dir, world)
        
        if canMoveResult == 0:
            return  # Ne peut pas bouger
        
        match dir:
            case Directions.Up:
                if canMoveResult == 2:
                    self.worldPos.y -= 1
                    self.pos.y = DIMY - 1
                else:
                    self.pos.y -= 1
            case Directions.Right:
                if canMoveResult == 2:
                    self.worldPos.x += 1
                    self.pos.x = 0
                else:
                    self.pos.x += 1
            case Directions.Down:
                if canMoveResult == 2:
                    self.worldPos.y += 1
                    self.pos.y = 0
                else:
                    self.pos.y += 1
            case Directions.Left:
                if canMoveResult == 2:
                    self.worldPos.x -= 1
                    self.pos.x = DIMX - 1
                else:
                    self.pos.x -= 1
    
    def display(self):
        print(Style.RESET_ALL)
        for i in range(DIMY):
            print(Cursor.POS(DIMX * 4 + 2, 2 + i) + "|")
        print(Cursor.POS(1, 1))

        percentXP = round(self.xp / self.getMaxXp() * 10)

        prt = ""
        prt += Cursor.POS(DIMX * 4 + 3, 2) + Back.WHITE + Fore.BLACK + self.name
        prt += (" " * (30 - len(self.name) - 5 - len(str(self.lvl)))) + "lvl. " + str(self.lvl) + "\n\n"
        prt += Cursor.POS(DIMX * 4 + 3, 3) + Style.RESET_ALL + "[" + ("░" * percentXP) + (" " * (10 - percentXP)) + "]"
        prt += str(self.xp) + "/" + str(self.getMaxXp()) + "\n\n"
        prt += Cursor.POS(DIMX * 4 + 3, 4) + Style.RESET_ALL + "Stat:\n"
        prt += Cursor.POS(DIMX * 4 + 3, 5) + Fore.RED   + "STR" + "          " + str(self.force) + "\n"
        prt += Cursor.POS(DIMX * 4 + 3, 6) + Fore.BLUE  + "DEF" + "          " + str(self.defense) + "\n"
        prt += Cursor.POS(DIMX * 4 + 3, 7) + Fore.GREEN + "SPE" + "          " + str(self.vitesse) + "\n"

        print(prt)