import random
import math
from colorama import Back, Cursor, Style, Fore
from Utils import Point, Directions, DIMX, DIMY

class Village:
    def __init__(self, pos: Point, village_type: str, size: str):
        self.pos = pos  # Position dans le monde (worldPos)
        self.village_type = village_type  # "coastal", "forest", "mountain", "plain"
        self.size = size  # "small", "medium", "large"
        self.population = self.getPopulation()
        self.name = self.generateName()
        self.wealth = self.calculateWealth()
        self.speciality = self.getSpeciality()
        self.mayor = self.generateMayor()
    
    def getPopulation(self):
        """Détermine la population selon la taille"""
        if self.size == "small":
            return random.randint(50, 150)
        elif self.size == "medium":
            return random.randint(150, 400)
        else:  # large
            return random.randint(400, 800)
    
    def generateName(self):
        """Génère un nom pour le village selon son type"""
        prefixes = {
            "coastal": ["Port", "Baie", "Marine", "Côte", "Phare"],
            "forest": ["Bois", "Forêt", "Sylve", "Chêne", "Pin"],
            "mountain": ["Mont", "Pic", "Roc", "Pierre", "Sommet"],
            "plain": ["Champ", "Plaine", "Blé", "Prairie", "Vert"]
        }
        
        suffixes = ["ville", "bourg", "ham", "heim", "ton", "feld", "en", "sur"]
        
        prefix = random.choice(prefixes.get(self.village_type, ["Grand"]))
        suffix = random.choice(suffixes)
        
        return f"{prefix}{suffix}"
    
    def calculateWealth(self):
        """Calcule la richesse du village"""
        base_wealth = {
            "small": random.randint(1, 3),
            "medium": random.randint(2, 4), 
            "large": random.randint(3, 5)
        }
        
        type_bonus = {
            "coastal": 1,  # Commerce maritime
            "plain": 1,    # Agriculture
            "forest": 0,   # Ressources naturelles
            "mountain": 0  # Mines
        }
        
        wealth_level = base_wealth[self.size] + type_bonus.get(self.village_type, 0)
        return min(5, max(1, wealth_level))  # Entre 1 et 5
    
    def getSpeciality(self):
        """Détermine la spécialité du village"""
        specialities = {
            "coastal": ["Pêche", "Commerce maritime", "Construction navale", "Sel marin"],
            "forest": ["Bûcheronnage", "Chasse", "Herboristerie", "Artisanat du bois"],
            "mountain": ["Extraction minière", "Forge", "Taille de pierre", "Élevage"],
            "plain": ["Agriculture", "Élevage", "Tissage", "Brasserie"]
        }
        
        return random.choice(specialities.get(self.village_type, ["Artisanat"]))
    
    def generateMayor(self):
        """Génère un nom pour le maire"""
        first_names = ["Aldric", "Béatrice", "Cédric", "Diane", "Édouard", "Fiona", 
                      "Guillaume", "Hélène", "Ivan", "Juliette", "Kevin", "Lucie"]
        last_names = ["Dubois", "Martin", "Bernard", "Moreau", "Laurent", "Lefebvre",
                     "Roux", "Fournier", "Girard", "Bonnet", "Dupont", "Lambert"]
        
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def getWealthDescription(self):
        """Retourne une description textuelle de la richesse"""
        descriptions = {
            1: "Très pauvre",
            2: "Pauvre", 
            3: "Modeste",
            4: "Prospère",
            5: "Très riche"
        }
        return descriptions.get(self.wealth, "Inconnue")

class Dungeon:
    def __init__(self, pos: Point, dungeon_type: str, ability_given: str):
        self.pos = pos  # Position dans le monde (worldPos - chunks)
        self.absolute_pos: Point = None  # Position absolue exacte de la tuile (sera définie lors du placement)
        self.dungeon_type = dungeon_type  # "accessible", "water_or_mountain", "both"
        self.ability_given = ability_given  # "water", "mountain"
        self.completed = False
    
    def complete(self):
        self.completed = True

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
    water    : Tile = Tile(1, "Eau",      Fore.BLUE,          "░░", 0.66)
    beach    : Tile = Tile(2, "Plage",    Fore.LIGHTYELLOW_EX,"░░", 0.60)
    plain    : Tile = Tile(3, "Plaine",   Fore.LIGHTGREEN_EX, "░░", 0.75)
    forest   : Tile = Tile(4, "Foret",    Fore.GREEN,         "░░", 0.66)
    mountain : Tile = Tile(5, "Montagne", Fore.WHITE,         "▲▲", 0.40)
    desert   : Tile = Tile(6, "Desert",   Fore.YELLOW,        "░░", 0.50)
    swamp    : Tile = Tile(7, "Marécage", Fore.LIGHTBLACK_EX, "░░", 0.45)
    river    : Tile = Tile(8, "Rivière",  Fore.CYAN,          "░░", 0.60)
    jungle   : Tile = Tile(9, "Jungle",   Fore.LIGHTGREEN_EX, "##", 0.55)
    tundra   : Tile = Tile(10, "Toundra", Fore.LIGHTCYAN_EX,  "..", 0.65)
    volcano  : Tile = Tile(11, "Volcan",  Fore.RED,           "▲▲", 0.30)
    village  : Tile = Tile(12, "Village", Fore.LIGHTWHITE_EX, "⌂⌂", 0.00)
    dungeon  : Tile = Tile(13, "Donjon",  Fore.MAGENTA,       "██", 0.00)

    @staticmethod
    def getAllTiles():
        return [
            Tiles.water,
            Tiles.beach,
            Tiles.plain,
            Tiles.forest,
            Tiles.mountain,
            Tiles.desert,
            Tiles.swamp,
            Tiles.river,
            Tiles.jungle,
            Tiles.tundra,
            Tiles.volcano,
            Tiles.village,
            Tiles.dungeon
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
        return (tiles[0] if tiles[0] != Tiles.dungeon else tiles[1])

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

class PerlinNoise:
    """Générateur de bruit de Perlin simplifié pour la génération d'archipel"""
    
    def __init__(self, seed=None):
        if seed is None:
            seed = random.randint(0, 999999)
        random.seed(seed)
        self.permutation = list(range(256))
        random.shuffle(self.permutation)
        self.permutation *= 2
        
    def fade(self, t):
        """Fonction de lissage"""
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    def lerp(self, a, b, t):
        """Interpolation linéaire"""
        return a + t * (b - a)
    
    def grad(self, hash_val, x, y):
        """Fonction de gradient simplifié"""
        h = hash_val & 3
        if h == 0: return x + y
        elif h == 1: return -x + y
        elif h == 2: return x - y
        else: return -x - y
    
    def noise(self, x, y):
        """Génère du bruit de Perlin pour les coordonnées x, y"""
        # Coordonnées de la cellule
        xi = int(x) & 255
        yi = int(y) & 255
        
        # Coordonnées relatives dans la cellule
        xf = x - int(x)
        yf = y - int(y)
        
        # Courbes de lissage
        u = self.fade(xf)
        v = self.fade(yf)
        
        # Hachage des coordonnées des 4 coins
        aa = self.permutation[self.permutation[xi] + yi]
        ab = self.permutation[self.permutation[xi] + yi + 1]
        ba = self.permutation[self.permutation[xi + 1] + yi]
        bb = self.permutation[self.permutation[xi + 1] + yi + 1]
        
        # Interpolation
        x1 = self.lerp(self.grad(aa, xf, yf), self.grad(ba, xf - 1, yf), u)
        x2 = self.lerp(self.grad(ab, xf, yf - 1), self.grad(bb, xf - 1, yf - 1), u)
        
        return self.lerp(x1, x2, v)
    
    def octave_noise(self, x, y, octaves=4, persistence=0.5, scale=0.1):
        """Génère du bruit de Perlin avec plusieurs octaves"""
        value = 0
        amplitude = 1
        frequency = scale
        max_value = 0
        
        for _ in range(octaves):
            value += self.noise(x * frequency, y * frequency) * amplitude
            max_value += amplitude
            amplitude *= persistence
            frequency *= 2
        
        return value / max_value

class World:
    BOUNDX = [0, DIMX - 1]
    BOUNDY = [0, DIMY - 1]

    def __init__(self) -> None:
        self.world : list[list[Chunk]] = [ [None]*(DIMY) for i in range(DIMX) ]
        self.dungeons : list[Dungeon] = []
        self.villages : list[Village] = []

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
        return Point(0, 0)  # Retourner une position par défaut si aucune case vide trouvée

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
        """Génère un archipel d'îles avec du bruit de Perlin"""
        print("Generation de l'archipel...")
        
        # Créer le générateur de bruit de Perlin
        perlin = PerlinNoise()
        
        # Dimensions de la carte mondiale
        world_width = DIMX * DIMX
        world_height = DIMY * DIMY
        
        print("Generation du bruit de Perlin...")
        # Générer la carte de bruit de Perlin (valeurs 0-255)
        noise_map = []
        for y in range(world_height):
            row = []
            for x in range(world_width):
                # Générer le bruit de Perlin et le convertir en valeur 0-255
                noise_value = perlin.octave_noise(x, y, octaves=4, persistence=0.5, scale=0.02)
                # Normaliser de [-1,1] vers [0,255]
                noise_255 = int((noise_value + 1) * 127.5)
                noise_255 = max(0, min(255, noise_255))  # Clamp entre 0 et 255
                row.append(noise_255)
            noise_map.append(row)
        
        print("Creation de l'archipel...")
        # Modifier le bruit pour créer un archipel d'îles
        self.createArchipelago(noise_map, world_width, world_height)
        
        print("Conversion en terrain avec seuils...")
        # Convertir les valeurs de bruit en types de terrain selon vos seuils
        terrain_map = []
        for y in range(world_height):
            row = []
            for x in range(world_width):
                noise_value = noise_map[y][x]
                
                # Appliquer vos seuils
                if noise_value <= 120:
                    terrain_type = Tiles.water.id  # Eau
                elif noise_value <= 135:
                    terrain_type = Tiles.beach.id  # Plage
                elif noise_value <= 220:
                    terrain_type = Tiles.plain.id  # Plaine (biomes à intégrer après)
                else:
                    terrain_type = Tiles.mountain.id  # Montagne
                
                row.append(terrain_type)
            terrain_map.append(row)
        
        print("Integration des biomes dans les plaines...")
        # Améliorer les biomes dans les zones de plaines
        self.generateBiomes(terrain_map, perlin, world_width, world_height)
        
        print("Generation des rivieres...")
        # Ajouter des rivières depuis les montagnes
        self.generateRivers(terrain_map, noise_map, world_width, world_height)
        
        print("Construction des chunks...")
        # Convertir la carte de terrain en chunks
        for x in range(DIMX):
            for y in range(DIMY):
                self.world[x][y] = Chunk()
                for ix in range(DIMX):
                    for iy in range(DIMY):
                        world_x = x * DIMX + ix
                        world_y = y * DIMY + iy
                        tile_id = terrain_map[world_y][world_x]
                        self.world[x][y].map[ix][iy] = Tiles.getTile(tile_id)
        
        print("Placement des villages...")
        # Placer les villages AVANT les donjons
        self.placeVillages()
        
        print("Placement des donjons...")
        # Placer les donjons EN DERNIER pour éviter qu'ils tombent dans l'eau
        self.placeDungeons()
        
        print("Archipel genere avec succes !")
    
    def placeVillages(self):
        """Place des villages sur des terrains appropriés"""
        print("Recherche d'emplacements pour villages...")
        
        # Analyser tous les chunks pour trouver les bons emplacements
        suitable_positions = {
            "coastal": [],    # Près de l'eau
            "forest": [],     # Zones forestières
            "plain": [],      # Plaines
            "mountain": []    # Zones montagneuses
        }
        
        for x in range(DIMX):
            for y in range(DIMY):
                chunk = self.world[x][y]
                
                # Analyser le contenu du chunk
                tile_counts = {}
                for ix in range(DIMX):
                    for iy in range(DIMY):
                        tile = chunk.map[ix][iy]
                        if tile.name in tile_counts:
                            tile_counts[tile.name] += 1
                        else:
                            tile_counts[tile.name] = 1
                
                total_tiles = DIMX * DIMY
                pos = Point(x, y)
                
                # Classifier selon le type de terrain dominant
                water_ratio = tile_counts.get("Eau", 0) / total_tiles
                beach_ratio = tile_counts.get("Plage", 0) / total_tiles
                plain_ratio = tile_counts.get("Plaine", 0) / total_tiles
                forest_ratio = tile_counts.get("Foret", 0) / total_tiles
                mountain_ratio = tile_counts.get("Montagne", 0) / total_tiles
                
                # Village côtier - près de l'eau mais pas dedans
                if beach_ratio > 0.2 and water_ratio < 0.5 and plain_ratio > 0.1:
                    suitable_positions["coastal"].append(pos)
                
                # Village forestier
                elif forest_ratio > 0.4:
                    suitable_positions["forest"].append(pos)
                
                # Village de plaine
                elif plain_ratio > 0.6:
                    suitable_positions["plain"].append(pos)
                
                # Village de montagne
                elif mountain_ratio > 0.2 and plain_ratio > 0.2:
                    suitable_positions["mountain"].append(pos)
        
        # Mélanger les positions
        for positions in suitable_positions.values():
            random.shuffle(positions)
        
        print(f"Positions trouvees - Cotiers: {len(suitable_positions['coastal'])}, "
              f"Forestiers: {len(suitable_positions['forest'])}, "
              f"Plaines: {len(suitable_positions['plain'])}, "
              f"Montagne: {len(suitable_positions['mountain'])}")
        
        # Placer 3-6 villages de différents types
        villages_to_place = [
            ("coastal", "medium"),
            ("forest", "small"), 
            ("plain", "large"),
            ("mountain", "small"),
            ("coastal", "small"),
            ("forest", "medium")
        ]
        
        placed_positions = set()
        
        for village_type, size in villages_to_place:
            if suitable_positions[village_type]:
                # Choisir une position pas trop proche des autres villages
                pos = None
                for candidate in suitable_positions[village_type]:
                    # Vérifier qu'on n'est pas trop près d'un autre village
                    too_close = False
                    for placed_pos in placed_positions:
                        distance = abs(candidate.x - placed_pos[0]) + abs(candidate.y - placed_pos[1])
                        if distance < 3:  # Minimum 3 chunks de distance
                            too_close = True
                            break
                    
                    if not too_close:
                        pos = candidate
                        break
                
                if pos:
                    village = Village(pos, village_type, size)
                    # Placer la tuile et obtenir la position exacte
                    exact_pos = self.placeVillageTile(pos)
                    village.pos = exact_pos  # Mettre à jour avec la position exacte
                    self.villages.append(village)
                    placed_positions.add((pos.x, pos.y))
                    print(f"Village {village_type} ({size}) place en ({exact_pos.x}, {exact_pos.y}) - {village.population} habitants")
        
        print(f"Total: {len(self.villages)} villages places")
    
    def placeVillageTile(self, worldPos: Point) -> Point:
        """Place une tuile village dans un chunk et retourne la position exacte"""
        chunk = self.world[worldPos.x][worldPos.y]
        
        # Trouver un bon emplacement dans le chunk (éviter l'eau)
        for attempts in range(50):  # Essayer 50 fois
            x = random.randint(0, DIMX - 1)
            y = random.randint(0, DIMY - 1)
            
            current_tile = chunk.map[x][y]
            # Placer le village sur un terrain approprié
            if current_tile.id not in [Tiles.water.id, Tiles.river.id, Tiles.mountain.id, Tiles.volcano.id]:
                chunk.map[x][y] = Tiles.village
                # Calculer la position absolue
                absolute_x = worldPos.x * DIMX + x
                absolute_y = worldPos.y * DIMY + y
                return Point(absolute_x, absolute_y)
        
        # Si on n'a pas trouvé de bon endroit, forcer sur une plaine
        chunk.map[0][0] = Tiles.village
        absolute_x = worldPos.x * DIMX + 0
        absolute_y = worldPos.y * DIMY + 0
        return Point(absolute_x, absolute_y)
    
    def createArchipelago(self, noise_map, width, height):
        """Modifie le bruit de Perlin pour créer un archipel d'îles"""
        center_x, center_y = width // 2, height // 2
        
        # 1. Forcer l'eau sur les bords de la carte
        border_size = 20  # Largeur de la bordure d'eau
        for y in range(height):
            for x in range(width):
                # Distance au bord le plus proche
                dist_to_edge = min(x, y, width - 1 - x, height - 1 - y)
                
                # Si on est près du bord, forcer l'eau
                if dist_to_edge < border_size:
                    # Transition graduelle vers l'eau
                    water_strength = 1.0 - (dist_to_edge / border_size)
                    noise_map[y][x] = int(noise_map[y][x] * (1 - water_strength))
        
        # 2. Créer des masques d'îles multiples
        island_centers = [
            (width * 0.2, height * 0.2),    # Île nord-ouest
            (width * 0.8, height * 0.2),    # Île nord-est
            (width * 0.5, height * 0.35),   # Île centrale nord
            (width * 0.3, height * 0.55),   # Île ouest
            (width * 0.7, height * 0.55),   # Île est
            (width * 0.15, height * 0.8),   # Île sud-ouest
            (width * 0.85, height * 0.8),   # Île sud-est
            (width * 0.5, height * 0.75),   # Île centrale sud
            (width * 0.6, height * 0.4),    # Petite île centre-est
            (width * 0.4, height * 0.65),   # Petite île centre-ouest
        ]
        
        for y in range(height):
            for x in range(width):
                # Calculer l'influence de chaque île
                max_island_influence = 0
                
                for island_x, island_y in island_centers:
                    # Distance à cette île
                    dist_to_island = math.sqrt((x - island_x)**2 + (y - island_y)**2)
                    
                    # Rayon d'influence de l'île (plus petit = îles plus petites)
                    island_radius = min(width, height) * 0.12  # Réduire pour plus de petites îles
                    
                    # Calculer l'influence (1.0 au centre, 0.0 au bord)
                    if dist_to_island < island_radius:
                        influence = 1.0 - (dist_to_island / island_radius)
                        # Courbe pour adoucir les bords
                        influence = influence ** 0.7
                        max_island_influence = max(max_island_influence, influence)
                
                # Appliquer l'influence des îles au bruit
                if max_island_influence > 0:
                    # Amplifier le bruit dans les zones d'îles
                    noise_map[y][x] = int(noise_map[y][x] + (255 - noise_map[y][x]) * max_island_influence * 0.7)
                else:
                    # Réduire le bruit dans les zones d'océan
                    noise_map[y][x] = int(noise_map[y][x] * 0.2)
        
        # 3. Ajouter des variation pour des îlots plus petits
        perlin_small = PerlinNoise()
        for y in range(height):
            for x in range(width):
                # Petit bruit pour créer des îlots supplémentaires
                small_noise = perlin_small.octave_noise(x, y, octaves=3, persistence=0.4, scale=0.08)
                small_255 = int((small_noise + 1) * 127.5)
                
                # Ajouter des petites îles occasionnelles
                if small_255 > 220 and noise_map[y][x] < 140:
                    noise_map[y][x] = min(255, noise_map[y][x] + 80)
    
    def generateBiomes(self, terrain_map, perlin, width, height):
        """Améliore la génération en ajoutant des biomes spécialisés dans les plaines"""
        print("Diversification des biomes...")
        
        # Compter les plaines pour avoir des statistiques
        plain_count = 0
        for y in range(height):
            for x in range(width):
                if terrain_map[y][x] == Tiles.plain.id:
                    plain_count += 1
        
        print(f"Transformation de {plain_count} tuiles de plaine en biomes...")
        
        # Générer des zones de biomes dans les plaines
        for y in range(height):
            for x in range(width):
                if terrain_map[y][x] == Tiles.plain.id:
                    
                    # 1. Forêts - 35% des plaines
                    forest_noise = perlin.octave_noise(x + 1000, y + 1000, octaves=3, scale=0.04)
                    forest_255 = int((forest_noise + 1) * 127.5)
                    
                    if forest_255 > 140:  # 35% de chance pour les forêts
                        terrain_map[y][x] = Tiles.forest.id
                    
                    # 2. Jungles - dans les zones très humides (près de l'eau)
                    elif forest_255 > 120:  # 15% supplémentaire
                        # Vérifier s'il y a de l'eau à proximité
                        has_water_nearby = False
                        for dx in range(-3, 4):
                            for dy in range(-3, 4):
                                nx, ny = x + dx, y + dy
                                if 0 <= nx < width and 0 <= ny < height:
                                    if terrain_map[ny][nx] in [Tiles.water.id, Tiles.river.id]:
                                        has_water_nearby = True
                                        break
                            if has_water_nearby:
                                break
                        
                        if has_water_nearby:
                            jungle_noise = perlin.octave_noise(x + 3000, y + 3000, octaves=2, scale=0.06)
                            if jungle_noise > 0.2:
                                terrain_map[y][x] = Tiles.jungle.id
                    
                    # 3. Marécages - zones humides près de l'eau
                    swamp_noise = perlin.octave_noise(x + 2000, y + 2000, octaves=3, scale=0.07)
                    swamp_255 = int((swamp_noise + 1) * 127.5)
                    
                    if swamp_255 < 60:  # 20% de chance pour les marécages
                        # Vérifier s'il y a de l'eau à proximité
                        has_water_nearby = False
                        for dx in range(-2, 3):
                            for dy in range(-2, 3):
                                nx, ny = x + dx, y + dy
                                if 0 <= nx < width and 0 <= ny < height:
                                    if terrain_map[ny][nx] in [Tiles.water.id, Tiles.beach.id, Tiles.river.id]:
                                        has_water_nearby = True
                                        break
                            if has_water_nearby:
                                break
                        
                        if has_water_nearby:
                            terrain_map[y][x] = Tiles.swamp.id
                    
                    # 4. Déserts - zones arides éloignées de l'eau
                    elif swamp_255 > 200:  # 15% de chance pour le désert
                        # Vérifier qu'on est loin de l'eau
                        far_from_water = True
                        for dx in range(-4, 5):
                            for dy in range(-4, 5):
                                nx, ny = x + dx, y + dy
                                if 0 <= nx < width and 0 <= ny < height:
                                    if terrain_map[ny][nx] in [Tiles.water.id, Tiles.river.id]:
                                        far_from_water = False
                                        break
                            if not far_from_water:
                                break
                        
                        if far_from_water:
                            desert_noise = perlin.octave_noise(x + 4000, y + 4000, octaves=2, scale=0.05)
                            if desert_noise > 0.3:
                                terrain_map[y][x] = Tiles.desert.id
                    
                    # 5. Toundra - zones froides (nord de la carte ou hautes altitudes)
                    if y < height * 0.2:  # Nord de la carte
                        tundra_noise = perlin.octave_noise(x + 5000, y + 5000, octaves=2, scale=0.08)
                        if tundra_noise > 0.4:
                            terrain_map[y][x] = Tiles.tundra.id
        
        # 6. Volcans - remplacer quelques montagnes par des volcans
        volcano_count = 0
        for y in range(height):
            for x in range(width):
                if terrain_map[y][x] == Tiles.mountain.id and volcano_count < 3:
                    volcano_noise = perlin.octave_noise(x + 6000, y + 6000, octaves=1, scale=0.1)
                    if volcano_noise > 0.7:
                        terrain_map[y][x] = Tiles.volcano.id
                        volcano_count += 1
        
        print(f"Biomes generes: forets, jungles, marecages, deserts, toundras, {volcano_count} volcans")
    
    def generateRivers(self, terrain_map, noise_map, width, height):
        """Génère des rivières depuis les montagnes vers la mer"""
        print("Generation de rivieres visibles...")
        
        # Trouver les points de départ (montagnes hautes et zones élevées)
        mountain_peaks = []
        for y in range(height):
            for x in range(width):
                if terrain_map[y][x] == Tiles.mountain.id and noise_map[y][x] > 230:
                    mountain_peaks.append((x, y))
                # Ajouter aussi des sources depuis les zones élevées de plaine
                elif terrain_map[y][x] == Tiles.plain.id and noise_map[y][x] > 200:
                    mountain_peaks.append((x, y))
        
        # Créer plus de rivières depuis les sommets
        num_rivers = min(15, max(5, len(mountain_peaks)))  # Entre 5 et 15 rivières
        selected_peaks = random.sample(mountain_peaks, num_rivers) if mountain_peaks else []
        
        print(f"Creation de {len(selected_peaks)} rivieres...")
        for start_x, start_y in selected_peaks:
            self.createRiver(terrain_map, noise_map, start_x, start_y, width, height)
    
    def createRiver(self, terrain_map, noise_map, start_x, start_y, width, height):
        """Crée une rivière en suivant la pente (vers les valeurs de bruit plus faibles)"""
        current_x, current_y = start_x, start_y
        visited = set()
        river_length = 0
        max_river_length = 80  # Rivières plus longues
        
        while river_length < max_river_length:
            if (current_x, current_y) in visited:
                break
            
            visited.add((current_x, current_y))
            
            # Si on atteint l'eau, on s'arrête
            if terrain_map[current_y][current_x] == Tiles.water.id:
                break
            
            # Placer de l'eau de rivière (même sur certaines montagnes)
            if terrain_map[current_y][current_x] != Tiles.mountain.id or noise_map[current_y][current_x] < 235:
                terrain_map[current_y][current_x] = Tiles.river.id
                
                # Élargir la rivière parfois pour la rendre plus visible
                if river_length % 8 == 0:  # Tous les 8 pas
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nx, ny = current_x + dx, current_y + dy
                        if (0 <= nx < width and 0 <= ny < height and 
                            terrain_map[ny][nx] not in [Tiles.water.id, Tiles.mountain.id, Tiles.river.id]):
                            terrain_map[ny][nx] = Tiles.river.id
            
            # Trouver la direction vers les valeurs de bruit plus faibles
            best_direction = None
            lowest_noise = noise_map[current_y][current_x]
            
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
            for dx, dy in directions:
                new_x, new_y = current_x + dx, current_y + dy
                
                if 0 <= new_x < width and 0 <= new_y < height and (new_x, new_y) not in visited:
                    new_noise = noise_map[new_y][new_x]
                    # Préférer les directions qui descendent
                    if new_noise < lowest_noise or (new_noise == lowest_noise and random.random() < 0.3):
                        lowest_noise = new_noise
                        best_direction = (dx, dy)
            
            # Si pas de pente trouvée, essayer une direction aléatoire
            if best_direction is None:
                available_directions = []
                for dx, dy in directions:
                    new_x, new_y = current_x + dx, current_y + dy
                    if 0 <= new_x < width and 0 <= new_y < height and (new_x, new_y) not in visited:
                        available_directions.append((dx, dy))
                
                if available_directions:
                    best_direction = random.choice(available_directions)
                else:
                    break
            
            current_x += best_direction[0]
            current_y += best_direction[1]
            river_length += 1
    
    def isAccessibleWithoutObstacles(self, worldPos: Point) -> bool:
        """Vérifie si une position est accessible sans obstacles (eau/montagne)"""
        # Utilise un algorithme BFS pour voir si on peut atteindre depuis (0,0) sans obstacles
        visited = set()
        queue = [(0, 0)]
        visited.add((0, 0))
        
        while queue:
            x, y = queue.pop(0)
            if x == worldPos.x and y == worldPos.y:
                return True
            
            # Vérifier les voisins
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < DIMX and 0 <= ny < DIMY and (nx, ny) not in visited:
                    chunk = self.world[nx][ny]
                    # Vérifier si le chunk est majoritairement accessible
                    if self.isChunkAccessible(chunk):
                        visited.add((nx, ny))
                        queue.append((nx, ny))
        
        return False
    
    def isChunkAccessible(self, chunk: Chunk) -> bool:
        """Vérifie si un chunk est majoritairement accessible (sans eau/montagne)"""
        water_count = 0
        mountain_count = 0
        total_tiles = DIMX * DIMY
        
        for x in range(DIMX):
            for y in range(DIMY):
                tile = chunk.map[x][y]
                if tile.id == Tiles.water.id or tile.id == Tiles.river.id:
                    water_count += 1
                elif tile.id == Tiles.mountain.id:
                    mountain_count += 1
        
        # Un chunk est accessible s'il a moins de 70% d'eau et moins de 70% de montagnes
        return (water_count / total_tiles) < 0.7 and (mountain_count / total_tiles) < 0.7
    
    def requiresWaterCrossing(self, start: Point, end: Point) -> bool:
        """Vérifie si aller de start à end nécessite de traverser l'eau"""
        # Pathfinding sans pouvoir traverser l'eau
        visited = set()
        queue = [(start.x, start.y)]
        visited.add((start.x, start.y))
        
        while queue:
            x, y = queue.pop(0)
            if x == end.x and y == end.y:
                return False  # Accessible sans eau
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < DIMX and 0 <= ny < DIMY and (nx, ny) not in visited:
                    chunk = self.world[nx][ny]
                    if not self.isChunkMajorityType(chunk, Tiles.water):
                        visited.add((nx, ny))
                        queue.append((nx, ny))
        
        return True  # Nécessite de traverser l'eau
    
    def requiresMountainCrossing(self, start: Point, end: Point) -> bool:
        """Vérifie si aller de start à end nécessite de traverser les montagnes"""
        # Pathfinding sans pouvoir traverser les montagnes
        visited = set()
        queue = [(start.x, start.y)]
        visited.add((start.x, start.y))
        
        while queue:
            x, y = queue.pop(0)
            if x == end.x and y == end.y:
                return False  # Accessible sans montagnes
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < DIMX and 0 <= ny < DIMY and (nx, ny) not in visited:
                    chunk = self.world[nx][ny]
                    if not self.isChunkMajorityType(chunk, Tiles.mountain):
                        visited.add((nx, ny))
                        queue.append((nx, ny))
        
        return True  # Nécessite de traverser les montagnes
    
    def isChunkMajorityType(self, chunk: Chunk, tile_type: Tile) -> bool:
        """Vérifie si un chunk est majoritairement d'un type donné"""
        count = 0
        total_tiles = DIMX * DIMY
        
        for x in range(DIMX):
            for y in range(DIMY):
                if chunk.map[x][y] == tile_type:
                    count += 1
        
        return count > total_tiles * 0.5
    
    def placeDungeons(self):
        """Place 3 donjons selon les spécifications - placement basé sur les tuiles individuelles"""
        print("Placement intelligent des donjons (basé sur les tuiles)...")
        
        # Positions occupées par les villages (en coordonnées absolues)
        village_positions = {(v.pos.x, v.pos.y) for v in self.villages}
        
        # Trouver toutes les positions de tuiles accessibles
        accessible_positions = []
        obstacle_positions = []
        all_land_positions = []
        
        # Parcourir tous les chunks et toutes les tuiles
        for chunk_x in range(DIMX):
            for chunk_y in range(DIMY):
                chunk = self.world[chunk_x][chunk_y]
                
                for tile_x in range(DIMX):
                    for tile_y in range(DIMY):
                        # Calculer la position absolue
                        abs_x = chunk_x * DIMX + tile_x
                        abs_y = chunk_y * DIMY + tile_y
                        
                        # Éviter les villages
                        if (abs_x, abs_y) in village_positions:
                            continue
                        
                        # Vérifier qu'on n'est pas trop près d'un village
                        too_close_to_village = False
                        for vx, vy in village_positions:
                            distance = abs(abs_x - vx) + abs(abs_y - vy)
                            if distance < 10:  # Minimum 10 tuiles des villages
                                too_close_to_village = True
                                break
                        
                        if too_close_to_village:
                            continue
                        
                        tile = chunk.map[tile_x][tile_y]
                        pos = Point(abs_x, abs_y)
                        
                        # Classificer les tuiles selon leur accessibilité
                        if tile.id in [Tiles.plain.id, Tiles.forest.id, Tiles.beach.id, Tiles.jungle.id, Tiles.desert.id, Tiles.tundra.id, Tiles.swamp.id]:
                            accessible_positions.append(pos)
                            all_land_positions.append(pos)
                        elif tile.id in [Tiles.water.id, Tiles.river.id, Tiles.mountain.id]:
                            # Positions nécessitant des capacités spéciales
                            obstacle_positions.append(pos)
                            all_land_positions.append(pos)
        
        print(f"Positions accessibles trouvees: {len(accessible_positions)}")
        print(f"Positions avec obstacles: {len(obstacle_positions)}")
        print(f"Villages a eviter: {len(village_positions)}")
        
        # Mélanger les listes
        random.shuffle(accessible_positions)
        random.shuffle(obstacle_positions)
        random.shuffle(all_land_positions)
        
        # Donjon 1: DOIT être accessible (sans obstacles)
        if accessible_positions:
            pos1 = accessible_positions[0]
            ability1 = "water"  # Première capacité
            dungeon1 = Dungeon(Point(pos1.x // DIMX, pos1.y // DIMY), "accessible", ability1)
            dungeon1.absolute_pos = pos1  # Stocker la position absolue
            self.dungeons.append(dungeon1)
            self.placeDungeonTileAbsolute(pos1)
            print(f"Donjon 1 (accessible): tuile ({pos1.x}, {pos1.y}) - capacite eau")
        else:
            print("ERREUR: Aucune position accessible trouvée!")
            return
        
        # Donjon 2: Peut être sur des obstacles (nécessite capacité eau ou montagne)
        used_positions = {(pos1.x, pos1.y)}
        
        # Chercher une position d'obstacle loin du donjon 1
        pos2 = None
        for candidate in obstacle_positions + accessible_positions:
            if (candidate.x, candidate.y) not in used_positions:
                # Vérifier la distance avec le donjon 1
                distance = abs(candidate.x - pos1.x) + abs(candidate.y - pos1.y)
                if distance > 50:  # Minimum 50 tuiles de distance
                    pos2 = candidate
                    break
        
        if not pos2 and all_land_positions:
            # Fallback: prendre n'importe quelle position éloignée
            for candidate in all_land_positions:
                if (candidate.x, candidate.y) not in used_positions:
                    distance = abs(candidate.x - pos1.x) + abs(candidate.y - pos1.y)
                    if distance > 30:
                        pos2 = candidate
                        break
        
        if not pos2:
            pos2 = Point(100, 100)  # Position par défaut
        
        used_positions.add((pos2.x, pos2.y))
        ability2 = "mountain"  # Deuxième capacité
        dungeon2 = Dungeon(Point(pos2.x // DIMX, pos2.y // DIMY), "water_or_mountain", ability2)
        dungeon2.absolute_pos = pos2
        self.dungeons.append(dungeon2)
        self.placeDungeonTileAbsolute(pos2)
        print(f"Donjon 2 (obstacles): tuile ({pos2.x}, {pos2.y}) - capacite montagne")
        
        # Donjon 3: Victoire finale - loin des autres
        pos3 = None
        for candidate in all_land_positions:
            if (candidate.x, candidate.y) not in used_positions:
                # Vérifier la distance avec les autres donjons
                dist1 = abs(candidate.x - pos1.x) + abs(candidate.y - pos1.y)
                dist2 = abs(candidate.x - pos2.x) + abs(candidate.y - pos2.y)
                if dist1 > 50 and dist2 > 50:
                    pos3 = candidate
                    break
        
        if not pos3:
            pos3 = Point(200, 200)  # Position par défaut
        
        dungeon3 = Dungeon(Point(pos3.x // DIMX, pos3.y // DIMY), "both", "victory")
        dungeon3.absolute_pos = pos3
        self.dungeons.append(dungeon3)
        self.placeDungeonTileAbsolute(pos3)
        print(f"Donjon 3 (final): tuile ({pos3.x}, {pos3.y}) - victoire")
        
        # Entourer le 3ème donjon d'obstacles
        self.surroundDungeonWithObstaclesAbsolute(pos3)
    
    def placeDungeonTileAbsolute(self, absolute_pos: Point):
        """Place une tuile donjon à une position absolue spécifique"""
        chunk_x = absolute_pos.x // DIMX
        chunk_y = absolute_pos.y // DIMY
        tile_x = absolute_pos.x % DIMX
        tile_y = absolute_pos.y % DIMY
        
        # Vérifier que les coordonnées sont valides
        if (0 <= chunk_x < DIMX and 0 <= chunk_y < DIMY and 
            0 <= tile_x < DIMX and 0 <= tile_y < DIMY):
            chunk = self.world[chunk_x][chunk_y]
            chunk.map[tile_x][tile_y] = Tiles.dungeon
        else:
            print(f"AVERTISSEMENT: Position donjon invalide ({absolute_pos.x}, {absolute_pos.y})")
    
    def surroundDungeonWithObstaclesAbsolute(self, absolute_pos: Point):
        """Entoure le donjon d'eau puis de montagnes en cercles concentriques (position absolue)"""
        import math
        center_x, center_y = absolute_pos.x, absolute_pos.y
        
        # Premier cercle: eau (rayon 2-3)
        for radius in range(2, 4):
            for angle in range(0, 360, 45):  # 8 directions
                offset_x = int(radius * math.cos(math.radians(angle)))
                offset_y = int(radius * math.sin(math.radians(angle)))
                
                obs_x = center_x + offset_x
                obs_y = center_y + offset_y
                
                chunk_x = obs_x // DIMX
                chunk_y = obs_y // DIMY
                tile_x = obs_x % DIMX
                tile_y = obs_y % DIMY
                
                if (0 <= chunk_x < DIMX and 0 <= chunk_y < DIMY and 
                    0 <= tile_x < DIMX and 0 <= tile_y < DIMY):
                    chunk = self.world[chunk_x][chunk_y]
                    if chunk.map[tile_x][tile_y].id not in [Tiles.village.id, Tiles.dungeon.id]:
                        chunk.map[tile_x][tile_y] = Tiles.water
        
        # Deuxième cercle: montagnes (rayon 4-5)
        for radius in range(4, 6):
            for angle in range(0, 360, 30):  # Plus de directions
                offset_x = int(radius * math.cos(math.radians(angle)))
                offset_y = int(radius * math.sin(math.radians(angle)))
                
                obs_x = center_x + offset_x
                obs_y = center_y + offset_y
                
                chunk_x = obs_x // DIMX
                chunk_y = obs_y // DIMY
                tile_x = obs_x % DIMX
                tile_y = obs_y % DIMY
                
                if (0 <= chunk_x < DIMX and 0 <= chunk_y < DIMY and 
                    0 <= tile_x < DIMX and 0 <= tile_y < DIMY):
                    chunk = self.world[chunk_x][chunk_y]
                    if chunk.map[tile_x][tile_y].id not in [Tiles.village.id, Tiles.dungeon.id, Tiles.water.id]:
                        chunk.map[tile_x][tile_y] = Tiles.mountain
    
    def placeDungeonTile(self, worldPos: Point, dungeon_index: int = 0):
        """Place une tuile donjon dans un chunk à différentes positions selon l'index"""
        chunk = self.world[worldPos.x][worldPos.y]
        center_x, center_y = DIMX // 2, DIMY // 2
        
        # Positions possibles pour les donjons dans un chunk
        positions = [
            (center_x, center_y),           # Centre
            (center_x - 2, center_y - 2),  # Haut-gauche
            (center_x + 2, center_y + 2),  # Bas-droite
            (center_x + 2, center_y - 2),  # Haut-droite
            (center_x - 2, center_y + 2)   # Bas-gauche
        ]
        
        pos_x, pos_y = positions[min(dungeon_index, len(positions) - 1)]
        
        # S'assurer que la position est valide
        pos_x = max(0, min(pos_x, DIMX - 1))
        pos_y = max(0, min(pos_y, DIMY - 1))
        
        chunk.map[pos_x][pos_y] = Tiles.dungeon
    
    def surroundDungeonWithObstacles(self, worldPos: Point):
        """Entoure le donjon d'eau puis de montagnes en cercles concentriques"""
        chunk = self.world[worldPos.x][worldPos.y]
        
        # Trouver la position exacte du donjon dans le chunk
        dungeon_tile_pos = None
        for x in range(DIMX):
            for y in range(DIMY):
                if chunk.map[x][y] == Tiles.dungeon:
                    dungeon_tile_pos = Point(x, y)
                    break
            if dungeon_tile_pos:
                break
        
        if not dungeon_tile_pos:
            return  # Pas de donjon trouvé, sortir
        
        # Déterminer aléatoirement l'ordre des obstacles
        if random.random() < 0.5:
            inner_obstacle = Tiles.water
            outer_obstacle = Tiles.mountain
        else:
            inner_obstacle = Tiles.mountain
            outer_obstacle = Tiles.water
        
        # Cercle 1: Tiles adjacentes au donjon (rayon 1)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Skip le donjon lui-même
                
                new_x = dungeon_tile_pos.x + dx
                new_y = dungeon_tile_pos.y + dy
                
                if 0 <= new_x < DIMX and 0 <= new_y < DIMY:
                    chunk.map[new_x][new_y] = inner_obstacle
        
        # Cercle 2: Tiles adjacentes aux tiles du cercle 1 (rayon 2)
        positions_to_fill = []
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                if abs(dx) <= 1 and abs(dy) <= 1:
                    continue  # Skip le centre et le cercle 1
                
                new_x = dungeon_tile_pos.x + dx
                new_y = dungeon_tile_pos.y + dy
                
                if 0 <= new_x < DIMX and 0 <= new_y < DIMY:
                    positions_to_fill.append((new_x, new_y))
        
        # Appliquer le second obstacle
        for x, y in positions_to_fill:
            chunk.map[x][y] = outer_obstacle
    
    def fillChunkWithTerrain(self, chunk: Chunk, terrain_type: Tile, coverage: float):
        """Remplit un chunk avec un type de terrain donné selon un pourcentage de couverture"""
        total_tiles = DIMX * DIMY
        tiles_to_fill = int(total_tiles * coverage)
        
        # Créer une liste de toutes les positions
        positions = []
        for x in range(DIMX):
            for y in range(DIMY):
                positions.append((x, y))
        
        # Mélanger et prendre le nombre requis de positions
        random.shuffle(positions)
        for i in range(min(tiles_to_fill, len(positions))):
            x, y = positions[i]
            chunk.map[x][y] = terrain_type
    
    def getRandomSpawnPosition(self) -> tuple[Point, Point]:
        """Retourne une position de spawn aléatoire pour le joueur"""
        # Chercher des chunks accessibles près des bordures
        spawn_candidates = []
        
        for x in range(DIMX):
            for y in range(DIMY):
                chunk = self.world[x][y]
                if self.isChunkAccessible(chunk):
                    # Vérifier si c'est près d'une bordure de chunk pour faciliter le changement
                    for tile_x in range(DIMX):
                        for tile_y in range(DIMY):
                            tile = chunk.map[tile_x][tile_y]
                            if tile in [Tiles.plain, Tiles.forest]:
                                # Favoriser les positions près des bordures
                                is_near_border = (tile_x < 3 or tile_x >= DIMX-3 or 
                                                tile_y < 3 or tile_y >= DIMY-3)
                                if is_near_border:
                                    spawn_candidates.append((Point(tile_x, tile_y), Point(x, y)))
        
        if spawn_candidates:
            return random.choice(spawn_candidates)
        else:
            # Fallback: position par défaut
            return Point(DIMX//2, DIMY//2), Point(0, 0)
    
    def getDungeonAt(self, worldPos: Point):
        """Retourne le donjon à la position donnée, ou None"""
        for dungeon in self.dungeons:
            if dungeon.pos.x == worldPos.x and dungeon.pos.y == worldPos.y:
                return dungeon
        return None

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
                
                # Priorité 1: Afficher le joueur (toujours visible)
                if player.worldPos.x == x and player.worldPos.y == y:
                    prt += Back.WHITE + tile.color + tile.car + Back.RESET
                else:
                    # Priorité 2: Vérifier s'il y a un donjon à cette position
                    dungeon = self.getDungeonAt(Point(x, y))
                    if dungeon:
                        if dungeon.completed:
                            # Donjon terminé - affichage différent
                            color = Back.GREEN + Fore.WHITE
                        else:
                            # Donjon non terminé
                            color = Back.MAGENTA + Fore.WHITE
                        prt += color + "  " + Back.RESET
                    else:
                        # Priorité 3: Affichage normal du terrain
                        prt += tile.color + tile.car
            print(Cursor.POS(DIMX * 2 + 2, y + 2) + prt)
            prt = ""
