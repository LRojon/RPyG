from WorldGen import World, Chunk, Tile, Back, Fore
from Utils import getch, Point, clearConsole, DIMX, DIMY, Directions
from PlayerGes import Player
from colorama import init, Cursor, Style
import time

def save():
    pass

def displayOpti(world: World, player: Player):
    pos = player.pos
    wpos = player.worldPos
    prtm = ""
    prtw = ""
    prtg = ""
    
    chunk: Chunk = world.world[wpos.x][wpos.y]

    print(Style.RESET_ALL + Cursor.POS(1, 1))
    for y in range(DIMY):
        prtm = ""
        prtw = ""
        for x in range(DIMX):

            if not chunk.map[x][y] is None:
                tile = chunk.map[x][y]

                if pos.x == x and pos.y == y:
                    prtm += Fore.RESET + Back.RESET + "^^"
                else:
                    prtm += tile.color + tile.car
            else:
                prtm += Back.RESET + "__"

            tile: Tile = world.world[x][y].getWorldDisplay()
            if wpos.x == x and wpos.y == y:
                prtw += Back.CYAN + tile.color + tile.car + Back.RESET
            else:
                prtw += tile.color + tile.car
        prtg += prtm + Style.RESET_ALL + " | " + prtw + "\n"
    print(prtg)

def main():
    init()

    world = World()    
    player = Player(input('Enter your name: '), Point(3, 3), Point(0, 0))
    print("Wolrd Generation in progress... Please wait (~30s)")
    world.gen()

    while True:
        
        # Display
        clearConsole()
        print(Cursor.POS(1, 0))
        world.display(player)
        player.display()
        
        # Event
        key = ""
        while not key in ["q", "2", "4", "6", "8"]:
            key = getch()
        match key:
            case "8": # Up
                player.move(Directions.Up, world)
            case "6": # Right
                player.move(Directions.Right, world)
            case "2": # Down
                player.move(Directions.Down, world)
            case "4": # Left
                player.move(Directions.Left, world)
            case "q":
                break
        
        time.sleep(0.2)

main()
