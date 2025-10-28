import random
from colorama import Back, Cursor, Style, Fore
from Utils import Point, Directions, DIMX, DIMY

class Tile:
    id: int
    name: str
    color: str
    car: str

    def __init__(self, id, name, color, car, propagation: float) -> None:
        self.id = id
        self.name = name
        self.color = color
        self.car = car
        self.propagation = propagation
    
    def toString(self):
        return "id: " + str(self.id) + " name: " + self.name

class Tiles:
    empty    : Tile = Tile(0, "Vide",     Fore.RESET,         "[]", 0.00)
    plain    : Tile = Tile(1, "Plaine",   Fore.LIGHTGREEN_EX, "░░", 0.75)
    forest   : Tile = Tile(2, "Foret",    Fore.GREEN,         "░░", 0.66)
    water    : Tile = Tile(3, "Eau",      Fore.BLUE,          "░░", 0.66)
    mountain : Tile = Tile(4, "Montagne", Fore.RESET,         "░░", 0.40)
    desert   : Tile = Tile(5, "Desert",   Fore.YELLOW,        "░░", 0.50)

    @staticmethod
    def getAllTiles():
        return [
            Tiles.plain,
            Tiles.forest,
            Tiles.water,
            Tiles.mountain,
            Tiles.desert
        ]
    @staticmethod
    def getTile(id: int) -> Tile:
        for t in Tiles.getAllTiles():
            if t.id == id:
                return t
        return Tiles.empty
    @staticmethod
    def getRandomTile() -> Tile:
        tiles = Tiles.getAllTiles()
        random.shuffle(tiles)
        return tiles[0]

class Chunk:
    map: list[list[Tile]]

    def __init__(self) -> None:
        self.map = [ [None]*DIMY for i in range(DIMX) ]
    
    def getWorldDisplay(self): # Get car and color for the display of worldmap
        tileSum = {}
        for y in range(DIMY):
            for x in range(DIMX):
                if not self.map[x][y].id in tileSum:
                    tileSum[self.map[x][y].id] = 1
                else:
                    tileSum[self.map[x][y].id] += 1
        maxKey = -1
        maxVal = -1
        for key in tileSum:
            value = tileSum[key]
            if maxVal < value:
                maxVal = value
                maxKey = key
        return Tiles.getTile(maxKey)

    def display(self, playerPos):
        prt = ""
        for y in range(DIMY):
            for x in range(DIMX):
                if not self.map[x][y] is None:
                    tile = self.map[x][y]

                    if playerPos.x == x and playerPos.y == y:
                        prt += Fore.RESET + Back.RESET + "^^"
                    else:
                        prt += tile.color + tile.car
                else:
                    prt += Back.RESET + "__"

            prt += "\n"
        print(prt)

class World:
    BOUNDX = [0, DIMX - 1]
    BOUNDY = [0, DIMY - 1]

    def __init__(self) -> None:
        self.world : list[list[Chunk]] = [ [None]*(DIMY) for i in range(DIMX) ]

    def isGenFinish(self, world):
        for x in range(DIMX ** 2):
            for y in range(DIMY ** 2):
                if world[x][y] == 0:
                    return False
        return True
    
    def getEmptyRemaining(self, world) -> list[Point]:
        emptyRemaining = []
        for x in range(DIMX ** 2):
            for y in range(DIMY ** 2):
                if world[x][y] == 0:
                    emptyRemaining.append(Point(x, y))
        return emptyRemaining
    
    def getNextEmpty(self, world) -> Point:
        empty: Point
        for x in range(DIMX ** 2):
            for y in range(DIMY ** 2):
                if world[x][y] == 0:
                    return Point(x, y)

    def getTile(self, id) -> Tile:
        for tile in Tiles.getAllTiles():
            if tile.id == id:
                return tile
        return Tiles.getAllTiles()[0]
    
    # strenght float between 0 and 1 = chance to apply the tile
    def applyTile(self, world: list[list[int]], x: int, y: int, tile: Tile, strenght: float, maxRange:int=10):
        world[x][y] = tile.id
        if maxRange <= -1:
            return
        
        dirs = [Directions.Up, Directions.Right, Directions.Down, Directions.Left]
        random.shuffle(dirs)
        for dir in dirs:
            nextCoord = Point(x, y).getCoordAfterMove(dir)
            if nextCoord.isInRectangle(len(world), len(world[0])):
                if world[nextCoord.x][nextCoord.y] != tile.id:
                    if random.random() <= strenght:
                        self.applyTile(world, nextCoord.x, nextCoord.y, tile, tile.propagation, maxRange - 1)

    def gen(self):
        world : list[list[int]] = [ [0]*(DIMY**2) for i in range(DIMX**2) ]

        while True:
            emptyPos = self.getNextEmpty(world)  # self.getEmptyRemaining(world)
            pos = emptyPos # emptyPos[random.randrange(len(emptyPos))]
            tile = Tiles.getRandomTile()
            self.applyTile(world, pos.x, pos.y, tile, tile.propagation, 20)

            if self.isGenFinish(world):
                break
        
        for x in range(0, DIMX):
            for y in range(0, DIMY):
                self.world[x][y] = Chunk()
                for ix in range(0, DIMX):
                    for iy in range(0, DIMY):
                        id : int = world[y * DIMY + iy][x * DIMX + ix]
                        self.world[x][y].map[ix][iy] = Tiles.getTile(id)

    def getCurrentChunk(self, player) -> Chunk:
        return self.world[player.worldPos.x][player.worldPos.y]
    
    def display(self, player):
        playerPos : Point = player.pos

        chunk: Chunk = self.world[player.worldPos.x][player.worldPos.y]
        chunk.display(playerPos)
        print(Style.RESET_ALL + Cursor.POS(1, 1))

        for i in range(DIMY):
            print(Cursor.POS(DIMX * 2 + 1, 2 + i) + "|")
        print(Cursor.POS(1, 1))
        prt = ""
        for y in range(0, DIMY):
            for x in range(0, DIMX):
                tile: Tile = self.world[x][y].getWorldDisplay()
                if player.worldPos.x == x and player.worldPos.y == y:
                    prt += Back.WHITE + tile.color + tile.car + Back.RESET
                else:
                    prt += tile.color + tile.car
            print(Cursor.POS(DIMX * 2 + 2, y + 2) + prt)
            prt = ""
