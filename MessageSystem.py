from colorama import Back, Fore, Cursor, Style
from Utils import clearConsole

def waitForEnter():
    """Attend spécifiquement la touche Entrée sans afficher de prompt"""
    try:
        # Utiliser input() sans texte pour éviter l'affichage dans le prompt
        input("")
    except:
        # Fallback au cas où il y aurait un problème
        input()

class MessageBox:
    
    @staticmethod
    def showMessage(message: str, wait_for_input: bool = True):
        """
        Affiche un message encadré en blanc sur noir par-dessus le jeu
        
        Args:
            message: Le message à afficher
            wait_for_input: Si True, attend une touche. Si False, affiche juste le message
        """
        lines = message.split('\n')
        
        # Si plus de 4-5 lignes, diviser en plusieurs boîtes
        if len(lines) > 5:
            MessageBox._showMultipleMessages(lines, wait_for_input)
        else:
            MessageBox._showSingleMessage(lines, wait_for_input)
    
    @staticmethod
    def _showSingleMessage(lines: list, wait_for_input: bool):
        """Affiche une seule boîte de message"""
        if not lines:
            return
        
        # Calculer la largeur nécessaire
        max_width = max(len(line) for line in lines) if lines else 0
        box_width = max_width + 4  # 2 espaces de chaque côté
        
        # Créer la boîte
        border_line = "|" + "─" * (box_width - 2) + "|"
        
        # Afficher la boîte au milieu de l'écran
        start_row = 10
        start_col = max(1, (80 - box_width) // 2)  # Centrer approximativement
        
        print(Cursor.POS(start_col, start_row) + Back.WHITE + Fore.BLACK + border_line)
        
        for i, line in enumerate(lines):
            padded_line = f"| {line:<{box_width-4}} |"
            print(Cursor.POS(start_col, start_row + 1 + i) + Back.WHITE + Fore.BLACK + padded_line)
        
        print(Cursor.POS(start_col, start_row + 1 + len(lines)) + Back.WHITE + Fore.BLACK + border_line)
        
        if wait_for_input:
            # Ligne pour "Appuyez sur Entrée"
            instruction = "Appuyez sur Entrée..."
            instruction_line = f"| {instruction:<{box_width-4}} |"
            print(Cursor.POS(start_col, start_row + 2 + len(lines)) + Back.WHITE + Fore.BLACK + instruction_line)
            print(Cursor.POS(start_col, start_row + 3 + len(lines)) + Back.WHITE + Fore.BLACK + border_line)
            
            # Attendre spécifiquement la touche Entrée
            waitForEnter()
            
            # Effacer l'écran après l'entrée pour nettoyer l'affichage
            clearConsole()
        
        print(Style.RESET_ALL)
    
    @staticmethod
    def _showMultipleMessages(lines: list, wait_for_input: bool):
        """Affiche plusieurs boîtes de message pour de longs textes"""
        chunk_size = 4
        chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
        
        for i, chunk in enumerate(chunks):
            is_last = (i == len(chunks) - 1)
            MessageBox._showSingleMessage(chunk, wait_for_input and is_last)
            
            if not is_last and wait_for_input:
                # Entre les chunks, attendre Entrée
                waitForEnter()
                # Effacer l'écran entre les messages
                clearConsole()

# Fonction d'utilisation simple comme un print
def showMessage(message: str, wait_for_input: bool = True):
    """
    Fonction simple pour afficher un message encadré
    
    Usage:
        showMessage("Bonjour!")
        showMessage("Message long\\nsur plusieurs\\nlignes")
        showMessage("Message sans attente", False)
    """
    MessageBox.showMessage(message, wait_for_input)