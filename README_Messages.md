# Système de Messages et Interface Propre

## Système de Messages Encadrés

### Utilisation Simple

```python
from MessageSystem import showMessage

# Message simple (attend Entrée et efface l'écran après)
showMessage("Bonjour!")

# Message sur plusieurs lignes (attend Entrée et efface l'écran après)
showMessage("Ligne 1\nLigne 2\nLigne 3")

# Message sans attendre de touche (n'efface pas l'écran)
showMessage("Information rapide", False)
```

## Système d'Input Propre

### Nouvelles fonctions d'entrée

```python
from CleanInput import cleanInput, cleanConfirm

# Input qui nettoie l'écran après la saisie
name = cleanInput("Entrez votre nom: ")

# Confirmation qui nettoie l'écran après
if cleanConfirm("Voulez-vous continuer?", "o"):
    print("Confirmé!")
```

## Fonctionnalités

- **Encadrement automatique** : Messages encadrés avec des caractères `|` et `─`
- **Centrage** : Les boîtes sont centrées à l'écran
- **Division automatique** : Les longs messages (>5 lignes) sont divisés en plusieurs boîtes
- **Attente Entrée uniquement** : Seule la touche Entrée fait continuer
- **Style** : Texte blanc sur fond noir par-dessus le jeu
- **🆕 NETTOYAGE AUTOMATIQUE** : L'écran est effacé après chaque interaction

## Nouveau dans cette version

- **Interface toujours propre** : Plus de résidus de prompts ou messages
- **Nettoyage automatique** : Tous les messages et inputs nettoient l'écran après usage
- **Expérience fluide** : Transitions propres entre les écrans
- **Functions spécialisées** : `cleanInput()` et `cleanConfirm()` pour les saisies

## Dans le jeu

Le système est utilisé pour :
- **Messages de donjons** : S'effacent après lecture
- **Menu de debug** : Interface propre
- **Messages de bienvenue** : Disparaissent après lecture
- **Saisies utilisateur** : Nom du joueur, confirmations, etc.
- **Transitions** : Entre les menus et le jeu

## Avantages

✅ **Plus de pollution visuelle**
✅ **Interface toujours nette**
✅ **Expérience utilisateur améliorée**
✅ **Transitions fluides**
✅ **Focus sur le gameplay**