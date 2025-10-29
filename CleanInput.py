from Utils import clearConsole

def cleanInput(prompt: str) -> str:
    """
    Fonction d'input qui nettoie l'écran après la saisie
    
    Args:
        prompt: Le texte à afficher pour demander l'entrée
    
    Returns:
        La chaîne saisie par l'utilisateur
    """
    result = input(prompt)
    clearConsole()
    return result

def cleanConfirm(prompt: str, default: str = "n") -> bool:
    """
    Fonction de confirmation qui nettoie l'écran après
    
    Args:
        prompt: La question à poser
        default: Valeur par défaut ("o" ou "n")
    
    Returns:
        True si l'utilisateur confirme, False sinon
    """
    full_prompt = f"{prompt} ({'O/n' if default == 'o' else 'o/N'}): "
    response = input(full_prompt).lower() or default
    clearConsole()
    return response == 'o'