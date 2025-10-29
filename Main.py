from WorldGen import World, Chunk, Tile, Back, Fore
from Utils import getch, Point, clearConsole, DIMX, DIMY, Directions
from PlayerGes import Player
from colorama import init, Cursor, Style
import time

import pickle
import os
import base64
import time

# Gestionnaire de sauvegarde intégré
class GameSave:
    @staticmethod
    def save(world, player, filename="game_save.dat"):
        """Sauvegarde le monde et le joueur dans un fichier chiffré simplement"""
        try:
            save_data = {
                'world': world,
                'player': player,
                'timestamp': time.time(),
                'version': '1.0'
            }
            
            # Sérialisation
            serialized = pickle.dumps(save_data)
            
            # Chiffrement simple (XOR avec clé)
            key = b"RPyG_Game_Save_Key_2024"
            encrypted = bytearray()
            for i, byte in enumerate(serialized):
                encrypted.append(byte ^ key[i % len(key)])
            
            # Encodage base64 et sauvegarde
            with open(filename, 'wb') as f:
                f.write(base64.b64encode(bytes(encrypted)))
            
            return True
        except Exception as e:
            print(f"Erreur sauvegarde: {e}")
            return False
    
    @staticmethod
    def load(filename="game_save.dat"):
        """Charge le monde et le joueur depuis le fichier"""
        try:
            if not os.path.exists(filename):
                return None
            
            # Lecture et décodage
            with open(filename, 'rb') as f:
                encrypted = base64.b64decode(f.read())
            
            # Déchiffrement
            key = b"RPyG_Game_Save_Key_2024"
            decrypted = bytearray()
            for i, byte in enumerate(encrypted):
                decrypted.append(byte ^ key[i % len(key)])
            
            # Désérialisation
            save_data = pickle.loads(bytes(decrypted))
            
            return save_data['world'], save_data['player'], save_data
        except Exception as e:
            print(f"Erreur chargement: {e}")
            return None
    
    @staticmethod
    def exists(filename="game_save.dat"):
        """Vérifie si une sauvegarde existe"""
        return os.path.exists(filename)

def displayVillageInfo(village):
    """Affiche les informations du village à droite des stats du joueur"""
    from colorama import Cursor, Fore, Style
    from Utils import DIMX, DIMY
    
    # Position à droite des stats du joueur (après la colonne des stats)
    start_x = DIMX * 4 + 35  # Décalé de 35 caractères par rapport aux stats
    start_y = 2
    
    prt = ""
    # Titre du village
    prt += Cursor.POS(start_x, start_y) + Style.BRIGHT + Fore.YELLOW + "[VILLAGE]"
    prt += Cursor.POS(start_x, start_y + 1) + "=" * 25
    
    # Informations du village
    prt += Cursor.POS(start_x, start_y + 3) + Style.RESET_ALL + Fore.CYAN + f"Nom: {village.name}"
    prt += Cursor.POS(start_x, start_y + 4) + Style.RESET_ALL + f"Type: {village.village_type.title()}"
    prt += Cursor.POS(start_x, start_y + 5) + Style.RESET_ALL + f"Taille: {village.size.title()}"
    
    # Population avec icône
    prt += Cursor.POS(start_x, start_y + 7) + Style.RESET_ALL + f"Population: {village.population:,}"
    
    # Richesse avec étoiles
    wealth_stars = "*" * village.wealth + "-" * (5 - village.wealth)
    prt += Cursor.POS(start_x, start_y + 8) + Style.RESET_ALL + f"Richesse: {wealth_stars}"
    prt += Cursor.POS(start_x, start_y + 9) + Style.RESET_ALL + f"   ({village.getWealthDescription()})"
    
    # Spécialité
    prt += Cursor.POS(start_x, start_y + 11) + Style.RESET_ALL + f"Specialite: {village.speciality}"
    
    # Maire
    prt += Cursor.POS(start_x, start_y + 13) + Style.RESET_ALL + f"Maire: {village.mayor}"
    
    # Information interactive
    prt += Cursor.POS(start_x, start_y + 15) + Style.DIM + Fore.GREEN + "Village non-interactif"
    prt += Cursor.POS(start_x, start_y + 16) + Style.DIM + "   (pour l'instant)"
    
    print(prt)

def save():
    """Fonction de sauvegarde pour le jeu"""
    global world, player
    
    success = GameSave.save(world, player)
    # if success:
    #     print("Partie sauvegardée avec succès !")
    # else:
    #     print("Erreur lors de la sauvegarde")
    return success

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

    # Variables globales pour sauvegarde
    global world, player
    
    # Vérifier s'il y a une sauvegarde au démarrage
    if GameSave.exists():
        from CleanInput import cleanInput
        choice = cleanInput("Une sauvegarde existe. Voulez-vous la charger ? (o/n/d pour supprimer): ").lower()
        if choice == 'o':
            result = GameSave.load()
            if result:
                world, player, save_data = result
                print(f"Partie chargée ! (sauvée le {time.ctime(save_data['timestamp'])})")
            else:
                print("Erreur lors du chargement, nouvelle partie...")
                world = World()    
                print("Génération du monde en cours... Please wait (~30s)")
                world.gen()
                # Utiliser le nouveau système de placement
                spawn_pos, spawn_world_pos = world.getRandomSpawnPosition()
                from CleanInput import cleanInput
                player_name = cleanInput('Enter your name: ')
                player = Player(player_name, spawn_pos, spawn_world_pos)
        elif choice == 'd':
            import os
            os.remove("game_save.dat")
            print("Sauvegarde supprimée. Nouvelle partie...")
            world = World()    
            print("Génération du monde en cours... Please wait (~30s)")
            world.gen()
            # Utiliser le nouveau système de placement
            spawn_pos, spawn_world_pos = world.getRandomSpawnPosition()
            from CleanInput import cleanInput
            player_name = cleanInput('Enter your name: ')
            player = Player(player_name, spawn_pos, spawn_world_pos)
        else:
            # Nouvelle partie
            world = World()    
            print("Génération du monde en cours... Please wait (~30s)")
            world.gen()
            # Utiliser le nouveau système de placement
            spawn_pos, spawn_world_pos = world.getRandomSpawnPosition()
            from CleanInput import cleanInput
            player_name = cleanInput('Enter your name: ')
            player = Player(player_name, spawn_pos, spawn_world_pos)
    else:
        # Pas de sauvegarde, nouvelle partie
        world = World()    
        print("Génération du monde en cours... Please wait (~30s)")
        world.gen()
        # Utiliser le nouveau système de placement
        spawn_pos, spawn_world_pos = world.getRandomSpawnPosition()
        from CleanInput import cleanInput
        player_name = cleanInput('Enter your name: ')
        player = Player(player_name, spawn_pos, spawn_world_pos)
        
        # Message de bienvenue avec le nouveau système
        from MessageSystem import showMessage
        welcome_msg = f"Bienvenue {player.name}!\n\n"
        welcome_msg += "🎯 Objectif: Trouvez et terminez les 3 donjons\n"
        welcome_msg += "🟣 Donjons violets = Non terminés\n"
        welcome_msg += "🟢 Donjons verts = Terminés\n\n"
        welcome_msg += "Contrôles: 8(↑) 4(←) 6(→) 2(↓)\n"
        welcome_msg += "s(Save) d(Debug) q(Quit)\n\n"
        welcome_msg += "💡 Astuce: Le 3ème donjon est protégé!\n"
        welcome_msg += "Il est entouré d'un cercle d'eau puis d'un cercle de montagnes.\n"
        welcome_msg += "Terminez les 2 premiers donjons pour obtenir les capacités nécessaires."
        showMessage(welcome_msg)
        
        # Effacer l'écran après le message de bienvenue
        clearConsole()

    while True:
        
        # Display - effacer d'abord pour un affichage propre
        clearConsole()
        print(Cursor.POS(1, 0))
        world.display(player)
        player.display()
        
        # Afficher les informations du village si le joueur est dessus
        current_village = player.getCurrentVillage(world)
        if current_village:
            displayVillageInfo(current_village)
        
        print(Cursor.POS(1, DIMY + 2))
        
        # Afficher les contrôles
        print(Style.RESET_ALL + "Contrôles: 8(↑) 4(←) 6(→) 2(↓) | s(Save) d(Debug) v(3ème donjon) q(Quit)")
        print("Donjons: 🟣 Non terminés | 🟢 Terminés")
        
        # Event
        key = ""
        while not key in ["q", "2", "4", "6", "8", "s", "d", "v"]:
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
            case "s": # Save
                save()
            case "d": # Debug - afficher les donjons
                from MessageSystem import showMessage
                message = "Donjons dans le monde:\n"
                for i, dungeon in enumerate(world.dungeons):
                    status = "✅ Terminé" if dungeon.completed else "❌ Non terminé"
                    message += f"Donjon {i+1}: Position ({dungeon.pos.x}, {dungeon.pos.y})\n"
                    message += f"Type: {dungeon.dungeon_type}\n"
                    message += f"Capacité: {dungeon.ability_given} - {status}\n\n"
                showMessage(message)
            case "v": # Voir le 3ème donjon
                from MessageSystem import showMessage
                third_dungeon = None
                for dungeon in world.dungeons:
                    if dungeon.ability_given == "victory":
                        third_dungeon = dungeon
                        break
                
                if third_dungeon:
                    message = f"3ème Donjon (Victoire finale):\n"
                    message += f"Position: ({third_dungeon.pos.x}, {third_dungeon.pos.y})\n"
                    message += f"Status: {'✅ Terminé' if third_dungeon.completed else '❌ Non terminé'}\n\n"
                    message += "Ce donjon est protégé par des cercles concentriques:\n"
                    message += "• Cercle 1: Obstacle autour du donjon\n"
                    message += "• Cercle 2: Autre obstacle autour du cercle 1\n"
                    message += "Vous devez avoir LES DEUX capacités pour l'atteindre!"
                else:
                    message = "3ème donjon introuvable!"
                showMessage(message)
            case "q":
                # Proposer de sauvegarder avant de quitter
                from CleanInput import cleanConfirm
                if cleanConfirm("Voulez-vous sauvegarder avant de quitter?", "n"):
                    save()
                    print("Partie sauvegardée ! Au revoir !")
                else:
                    print("Au revoir !")
                break
        
        time.sleep(0.2)

main()
