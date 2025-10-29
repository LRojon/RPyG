from Utils import Point, Directions, DIMY, DIMX
from colorama import Back, Fore, Cursor, Style
import math

# Import pour éviter les références circulaires
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from WorldGen import World, Chunk, Tiles, Dungeon

class Player:
    
    def __init__(self, name, pos, worldPos, canWalkMountain = False, canWalkWater = False):
        self.pos : Point = pos
        self.worldPos : Point = worldPos
        self.canWalkMountain : bool = canWalkMountain
        self.canWalkWater : bool = canWalkWater
        self.name = name
        self.game_completed = False  # Nouveau: marquer si le jeu est terminé
        self.hp = 10
        self.maxHP = 10
        self.force = 1
        self.defense = 1
        self.vitesse = 1
        self.lvl = 1
        self.xp = 0
        self.skillPts = 0
        self.hpPts  = 0
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

    def canMove(self, direction: Directions, world) -> int:
        from WorldGen import Tiles, Chunk
        
        nextPos: Point = Point(self.pos.x, self.pos.y)
        nextWorldPos: Point = Point(self.worldPos.x, self.worldPos.y)
        
        match direction:
            case Directions.Up:
                nextPos.y -= 1
                if nextPos.y < 0:
                    nextWorldPos.y -= 1
                    nextPos.y = DIMY - 1  # Se déplacer vers le bas du nouveau chunk
            case Directions.Right:
                nextPos.x += 1
                if nextPos.x >= DIMX:
                    nextWorldPos.x += 1
                    nextPos.x = 0  # Se déplacer vers la gauche du nouveau chunk
            case Directions.Down:
                nextPos.y += 1
                if nextPos.y >= DIMY:
                    nextWorldPos.y += 1
                    nextPos.y = 0  # Se déplacer vers le haut du nouveau chunk
            case Directions.Left:
                nextPos.x -= 1
                if nextPos.x < 0:
                    nextWorldPos.x -= 1
                    nextPos.x = DIMX - 1  # Se déplacer vers la droite du nouveau chunk
        
        # Vérifier les limites du monde
        if not nextWorldPos.isInRectangle(len(world.world), len(world.world[0])):
            return 0
        
        # Vérifier le terrain dans la chunk appropriée
        target_chunk: Chunk = world.world[nextWorldPos.x][nextWorldPos.y]
        target_tile = target_chunk.map[nextPos.x][nextPos.y]
        
        # Vérifier les obstacles sans debug
        if target_tile == Tiles.mountain and not self.canWalkMountain:
            return 0
        if (target_tile == Tiles.water or target_tile == Tiles.river) and not self.canWalkWater:
            return 0
        
        # Retourner 2 si on change de chunk, 1 sinon
        if nextWorldPos.x != self.worldPos.x or nextWorldPos.y != self.worldPos.y:
            return 2
        else:
            return 1

    def move(self, dir: Directions, world):
        from WorldGen import Tiles
        
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
        
        # Vérifier s'il y a un donjon à la nouvelle position
        self.checkForDungeon(world)
    
    def checkForDungeon(self, world):
        """Vérifie s'il y a un donjon à la position actuelle du joueur"""
        from WorldGen import Tiles
        from Utils import DIMX, DIMY
        
        # Calculer la position absolue du joueur
        absolute_x = self.worldPos.x * DIMX + self.pos.x
        absolute_y = self.worldPos.y * DIMY + self.pos.y
        
        # Vérifier si on est sur une tuile donjon
        current_chunk = world.world[self.worldPos.x][self.worldPos.y]
        current_tile = current_chunk.map[self.pos.x][self.pos.y]
        
        if current_tile == Tiles.dungeon:
            # Trouver le donjon correspondant à cette position exacte
            for dungeon in world.dungeons:
                if (dungeon.absolute_pos and 
                    dungeon.absolute_pos.x == absolute_x and 
                    dungeon.absolute_pos.y == absolute_y and
                    not dungeon.completed):
                    self.enterDungeon(dungeon)
                    break
    
    def enterDungeon(self, dungeon):
        """Gère l'entrée dans un donjon"""
        from MessageSystem import showMessage
        
        message = f"🏰 Vous entrez dans un donjon de type: {dungeon.dungeon_type}\n"
        message += "🗡️  Vous combattez les monstres du donjon...\n"
        message += "✅ Donjon terminé avec succès!\n\n"
        
        # Donner la capacité
        if dungeon.ability_given == "water":
            self.canWalkWater = True
            message += "🌊 Vous avez obtenu la capacité de traverser l'eau!"
        elif dungeon.ability_given == "mountain":
            self.canWalkMountain = True
            message += "⛰️  Vous avez obtenu la capacité de traverser les montagnes!"
        elif dungeon.ability_given == "victory":
            message += "🏆 FÉLICITATIONS! 🏆\n"
            message += "Vous avez terminé le jeu!\n"
            message += "Vous êtes maintenant le maître de tous les éléments!"
        
        # Marquer le donjon comme terminé
        dungeon.complete()
        
        # Vérifier si c'est la victoire finale
        if dungeon.ability_given == "victory":
            self.game_completed = True  # Marquer le jeu comme terminé
        
        # Donner de l'expérience
        self.addXP(100)
        message += f"\n📈 +100 XP!"
        
        showMessage(message)
    
    def display(self):
        print(Style.RESET_ALL)
        for i in range(DIMY):
            print(Cursor.POS(DIMX * 4 + 2, 2 + i) + "|")
        print(Cursor.POS(1, 1))

        percentXP = round(self.xp / self.getMaxXp() * 10)
        percentHP = round(self.hp / self.maxHP * 10)

        prt = ""
        prt += Cursor.POS(DIMX * 4 + 3, 2)  + Back.WHITE + Fore.BLACK + self.name
        prt += (" " * (30 - len(self.name) - 5 - len(str(self.lvl)))) + "lvl. " + str(self.lvl)
        prt += Cursor.POS(DIMX * 4 + 3, 4)  + Style.RESET_ALL + Fore.RED + "PV: [" + ("░" * percentHP) + (" " * (10 - percentHP)) + "] "
        prt += str(self.hp) + "/" + str(self.maxHP)
        prt += Cursor.POS(DIMX * 4 + 3, 5)  + Style.RESET_ALL + "XP: [" + ("░" * percentXP) + (" " * (10 - percentXP)) + "] "
        prt += str(self.xp) + "/" + str(self.getMaxXp())
        prt += Cursor.POS(DIMX * 4 + 3, 7)  + Style.RESET_ALL + "Stat:"
        prt += (" " * (30 - 5 - 11 - len(str(self.skillPts)))) + "Skill pts. " + str(self.skillPts)
        prt += Cursor.POS(DIMX * 4 + 3, 8)  + Fore.RED   + "STR" + "          " + str(self.force)
        prt += Cursor.POS(DIMX * 4 + 3, 9)  + Fore.BLUE  + "DEF" + "          " + str(self.defense)
        prt += Cursor.POS(DIMX * 4 + 3, 10) + Fore.GREEN + "SPE" + "          " + str(self.vitesse)
        
        # Afficher les capacités spéciales
        prt += Cursor.POS(DIMX * 4 + 3, 12) + Style.RESET_ALL + "Capacités:"
        if self.canWalkWater:
            prt += Cursor.POS(DIMX * 4 + 3, 13) + Fore.CYAN + "🌊 Traverser l'eau"
        else:
            prt += Cursor.POS(DIMX * 4 + 3, 13) + Fore.RED + "❌ Eau bloquée"
        
        if self.canWalkMountain:
            line = 14 if self.canWalkWater else 14
            prt += Cursor.POS(DIMX * 4 + 3, line) + Fore.WHITE + "⛰️  Traverser montagnes"
        else:
            line = 14
            prt += Cursor.POS(DIMX * 4 + 3, line) + Fore.RED + "❌ Montagne bloquée"

        print(prt)
    
    def getCurrentVillage(self, world):
        """Retourne le village sur lequel se trouve le joueur, ou None"""
        from WorldGen import Tiles
        from Utils import DIMX, DIMY
        
        # Calculer la position absolue du joueur dans le monde
        absolute_x = self.worldPos.x * DIMX + self.pos.x
        absolute_y = self.worldPos.y * DIMY + self.pos.y
        
        # Vérifier si le joueur est sur une tuile village
        current_chunk = world.world[self.worldPos.x][self.worldPos.y]
        current_tile = current_chunk.map[self.pos.x][self.pos.y]
        
        if current_tile.id == Tiles.village.id:
            # Trouver le village correspondant à cette position
            for village in world.villages:
                if village.pos.x == absolute_x and village.pos.y == absolute_y:
                    return village
        
        return None