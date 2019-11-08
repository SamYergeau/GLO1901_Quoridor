import argparse
import api


'''
def prompt_prochaine_action
Description:
    demande à l'utilisateur d'exécuter sa prochaine action et lui
    explique le format et les options de commandes qui lui sont possible
Input:
    None
Return:
    None
'''
def prompt_prochaine_action():
    # demander au joueur d'entrer sa prochaine action
    print("entrer votre prochain coup:")
    # expliquer l'orthographe de la commande à entrer
    print("entrer: python main.py [idul] --action [type] [posx] [posy]")
    # expliquer le paramètre type
    print("[type]: type de coup à jouer:")
    # expliquer les options de types de coups
    print("    - 'D': Déplacer l'avatar sur le plateau de jeu (attention: déplacer de 1 case à la foi seulement)")
    print("    - 'MH: Placer un mur horizontal sur le plateau de jeu")
    print("    - 'MV: Placer un mur vertical sur le plateau de jeu")
    # expliquer le paramètre posx
    print("[posx]: Position en X où déplacer l'avatar ou placer un mur")
    # expliquer le paramètre posy
    print("[posy]: Position en Y où déplacer l'avatar ou placer un mur")


'''
def afficher_damier_ascii(etat)
Desctiprion:
    Une fonction qui construit une visualisation graphique de la table de jeu
    en se basant sur les informations données dans le dictionnaire "etat"
    et l'affiche à la console de commange
Input:
    etat(dict)
        Un dictionnaire contenant l'état du jeu. contient:
            - {"joueurs": list[dict]} informations sur les joueurs:
                - {"Nom": str}:  Le nom du joueur
                - {"murs": int}: Le nombre de murs que le joueur peut encore jouer
                - {"pos": list}: La position [x, y]* du joueur 
            - {"murs": dict}: la position des murs:
                - {"horizontaux": list}:    Une liste des positions [x, y]* des murs horizontaux
                - {"verticaux": list}:      Une liste des positions [x, y]* des murs verticaux
            *la position du joueur est relative à la grille VISUELLE du tableau affiché
Return: 
    none
Note:   ce tableau de jeu est fait en sorte qu'il puisse être configurable.
        Sa taille et son nombre de joueur peuvent donc être changés sans 
        impacter la stabilité. Ainsi, des modifications futures seront beaucoup
        plus faciles.
'''
def afficher_damier_ascii(etat):
    # définition des contraintes du tableau de jeu
    # permet de modifier la taille du jeu si désiré
    '''TODO: ajuster le code pour pouvoir ajuster le spacing entre les lignes'''
    BOARD_HORIZONTAL_POSITIONS = 9
    BOARD_VERTICAL_POSITIONS = 9    
    BOARD_SPACING_HORIZONTAL = ((BOARD_HORIZONTAL_POSITIONS * 4) - 1)
    # Extraction des variables du dictionnaire
    # joueurs
    joueurs = etat["joueurs"]
    # murs horizontaux et verticaux
    murs = etat["murs"]
    murs_horizontaux = murs["horizontaux"]
    murs_verticaux = murs["verticaux"]
    # tableaux d'équivalences entre les adresses du jeu et notre tableau
    game_pos_X = range(1, (BOARD_HORIZONTAL_POSITIONS * 4), 4)
    game_pos_Y = range(((BOARD_VERTICAL_POSITIONS - 1) * 2), -1, -2)
    # Création du tableau de jeu
    légende = "légende: " # place holder où ajouter tous les joueurs (pour permettre plus de 2 joueurs)
    top_line = (' ' * 3) + ('-' * BOARD_SPACING_HORIZONTAL) + '\n'
    board = [légende]
    # game board
    '''TODO: optimiser cette boucle'''
    for i in reversed(range(BOARD_VERTICAL_POSITIONS * 2)):
        if (i % 2) != 0:
            board += ["{} |".format((i + 1) // 2)] 
            board += [' ', '.',]
            board += ([' ', ' ', ' ','.'] * (BOARD_HORIZONTAL_POSITIONS - 1))
            board += [' ', '|\n']
        else:
             board += ["  |"] 
             board += ([' '] * BOARD_SPACING_HORIZONTAL)
             board += ['|\n']
    # bottom board line
    board += "--|" + ('-' * BOARD_SPACING_HORIZONTAL) + '\n'
    # bottom number line
    board += (' ' * 2) + '| '
    for i in range(1, BOARD_HORIZONTAL_POSITIONS):
	    board += str(i) + (' ' * 3)
    board += "9\n"
    # insertion des joueurs dans board
    for num, joueur in enumerate(joueurs):
        # ajout du joueur à la légende du tableau
        légende += "{}={} ".format((num + 1), joueur['nom'])
        # obtention de la position en [x, y] du joueur
        position = joueur["pos"]
        # vérification que la position est dans les contraintes
        if (0 > position[0] > BOARD_HORIZONTAL_POSITIONS) or (0 > position[1] > BOARD_VERTICAL_POSITIONS):
            raise IndexError("Adresse du joueur invalide!")
        # calcul du décallage relatif au tableau
        position_X = game_pos_X[(position[0] - 1)]
        position_Y = game_pos_Y[(position[1] - 1)]
        indice = position_X + (position_Y * BOARD_SPACING_HORIZONTAL)
        decallage = ((((indice + 1) // BOARD_SPACING_HORIZONTAL) * 2) + 2)
        indice += decallage
        # Insérer le personnage dans le tableau de jeu
        board[indice] = str(num + 1)
    # complétion de la légende du tableau
    board[0] = légende + '\n' + top_line 
    # insertion des murs horizontaux dans board
    for murH in murs_horizontaux:
        # vérification que la position est dans les contraintes
        if (1 > murH[0] > (BOARD_HORIZONTAL_POSITIONS - 1)) or (2 > murH[1] > BOARD_VERTICAL_POSITIONS):
            raise IndexError("Position du mur horizontal invalide!")
        position_X = (game_pos_X[(murH[0] - 1)] - 1)
        position_Y = (game_pos_Y[(murH[1] - 1)] + 1)
        indice = position_X + (position_Y * BOARD_SPACING_HORIZONTAL)
        decallage = ((((indice + 1) // BOARD_SPACING_HORIZONTAL) * 2) + 2)
        indice += decallage
        # itérer pour placer les 5 murs
        for i in range(7):
            board[(indice + i)] = '-'
    # insertion des murs verticaux
    for murV in murs_verticaux:
        # vérification que la position est dans les contraintes
        if (2 > murV[0] > BOARD_HORIZONTAL_POSITIONS) or (1 > murV[1] > BOARD_VERTICAL_POSITIONS):
            raise IndexError("Position du mur vertical invalide!")
        position_X = (game_pos_X[(murV[0] - 1)] - 2)
        position_Y = game_pos_Y[(murV[1] - 1)]
        indice = position_X + (position_Y * BOARD_SPACING_HORIZONTAL)
        decallage = ((((indice + 1) // BOARD_SPACING_HORIZONTAL) * 2) + 2)
        indice += decallage
        # itérer pour placer les 3 murs
        for i in range(3):
            board[(indice - (i * (BOARD_SPACING_HORIZONTAL + 2)))] = '|'
    # afficher le jeu sous forme d'une chaine de caractères
    print(''.join(board))