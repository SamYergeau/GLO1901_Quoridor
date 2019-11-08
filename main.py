'''
Summary line.
main.py
document principal du jeu quoridor
'''
import argparse
import api


'''
Summary line. 
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
    print("    - 'D': Déplacer l'avatar sur le plateau de jeu")
    print("    - 'MH: Placer un mur horizontal sur le plateau de jeu")
    print("    - 'MV: Placer un mur vertical sur le plateau de jeu")
    # expliquer le paramètre posx
    print("[posx]: Position en X où déplacer l'avatar ou placer un mur")
    # expliquer le paramètre posy
    print("[posy]: Position en Y où déplacer l'avatar ou placer un mur")


'''
Summary line. 
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
    board_positions = 9
    spacing_horizontal = ((board_positions * 4) - 1)
    # tableaux d'équivalences entre les adresses du jeu et notre tableau
    game_pos_x = range(1, (board_positions * 4), 4)
    game_pos_y = range(((board_positions - 1) * 2), -1, -2)
    # Création du tableau de jeu
    # place holder où ajouter tous les joueurs (pour permettre plus de 2 joueurs)
    légende = "légende: "
    board = [légende]
    # game board
    for i in reversed(range(board_positions * 2)):
        if (i % 2) != 0:
            board += ["{} |".format((i + 1) // 2)]
            board += [' ', '.']
            board += ([' ', ' ', ' ', '.'] * (board_positions - 1))
            board += [' ', '|\n']
        else:
            board += ["  |"]
            board += ([' '] * spacing_horizontal)
            board += ['|\n']
    # bottom board line
    board += "--|" + ('-' * spacing_horizontal) + '\n'
    # bottom number line
    board += (' ' * 2) + '| '
    for i in range(1, board_positions):
	    board += str(i) + (' ' * 3)
    board += "9\n"
    # insertion des joueurs dans board
    for num, joueur in enumerate(etat["joueurs"]):
        # ajout du joueur à la légende du tableau
        légende += "{}={} ".format((num + 1), joueur['nom'])
        # obtention de la position en [x, y] du joueur
        position = joueur["pos"]
        # vérification que la position est dans les contraintes
        if ((0 > position[0] > board_positions) or
                (0 > position[1] > board_positions)):
            raise IndexError("Adresse du joueur invalide!")
        # calcul du décallage relatif au tableau
        indice = (game_pos_x[(position[0] - 1)] +
                    (game_pos_y[(position[1] - 1)] * spacing_horizontal))
        decallage = ((((indice + 1) // spacing_horizontal) * 2) + 2)
        indice += decallage
        # Insérer le personnage dans le tableau de jeu
        board[indice] = str(num + 1)
    # complétion de la légende du tableau
    board[0] = légende + '\n' + (' ' * 3) + ('-' * spacing_horizontal) + '\n'
    # insertion des murs horizontaux dans board
    for murh in etat["murs"]["horizontaux"]:
        # vérification que la position est dans les contraintes
        if ((1 > murh[0] > (board_positions - 1)) or
                (2 > murh[1] > board_positions)):
            raise IndexError("Position du mur horizontal invalide!")
        indice = ((game_pos_x[(murh[0] - 1)] - 1) +
                    ((game_pos_y[(murh[1] - 1)] + 1) * spacing_horizontal))
        decallage = ((((indice + 1) // spacing_horizontal) * 2) + 2)
        indice += decallage
        # itérer pour placer les 5 murs
        for i in range(7):
            board[(indice + i)] = '-'
    # insertion des murs verticaux
    for murv in etat["murs"]["verticaux"]:
        # vérification que la position est dans les contraintes
        if (2 > murv[0] > board_positions) or (1 > murv[1] > board_positions):
            raise IndexError("Position du mur vertical invalide!")
        indice = ((game_pos_x[(murv[0] - 1)] - 2) +
                    (game_pos_y[(murv[1] - 1)] * spacing_horizontal))
        decallage = ((((indice + 1) // spacing_horizontal) * 2) + 2)
        indice += decallage
        # itérer pour placer les 3 murs
        for i in range(3):
            board[(indice - (i * (spacing_horizontal + 2)))] = '|'
    # afficher le jeu sous forme d'une chaine de caractères
    print(''.join(board))


'''
Summary line. 
def boucler(id)
Description:
    fonction de logistique principale du code. L'orsqu'une commande contenant des actions
    est reçue, notifie le serveur, affiche le nouveau tableau de jeu et demande au joueur de jouer son prochain coup
Input:
    newcommand (argparse.argumentparser.Nameplace):
        un Nameplace contenant les actions du joueur qui sera passé au serveur
Return:
    None
'''
def boucler(newcommand):
    # envoyer la nouvelle commande au serveur
    # on va cherche le id dans son holder
    with open('id_holder.txt', 'r') as fich:
        id = fich.read()
    newboard = api.jouer_coup(id, newcommand.lister[0],
                        (newcommand.lister[1], newcommand.lister[2]))
    # afficher le tableau de jeu
    afficher_damier_ascii(newboard['état'])
    # demander au joueur de jouer son prochain coup
    prompt_prochaine_action()


'''
Summary line. 
def debuter
Description:
    initialise un nouveau tableau de jeu et store le id de la partie
Input:
    comm (Nameplace)
        un objet contenant la valeur du idul entrée par le joueur au terminal
        associé à la clé 'idul'
Return:
    None
'''
def debuter(comm):
    # transmettre le idul au serveur et recevoir l'état initial du jeu
    newboard = api.débuter_partie(comm.idul)
    # petit mot de bienvenu (tout est dans les détails après tout)
    print('\n' + '~' * 39)
    print("BIENVENU DANS QUORIDOR!")
    print('~' * 39 + '\n')
    # afficher le jeu initial
    afficher_damier_ascii(newboard['état'])
    # créer un fichier où stocker le id de la partie
    fich = open('id_holder.txt', 'w')
    fich.write(newboard['id'])
    # fermer le fichier pour la bonne mesure
    fich.close()
    # demander au joueur de jouer son prochain coup
    prompt_prochaine_action()


'''
Summary line. 
def analyser_commande(commande)
Description:
    Une fonction qui permet au joueur d'intéragir avec le jeu
    en entrant des commandes dans le terminal
Input:
    None
Return:
    Un objet argparse.ArgumentParser contenant la réponse du joueur
'''
def analyser_commande():
    parser = argparse.ArgumentParser(
        description="Jeu de quoridor"
    )
    # indiquer au joueur d'entrer son nom
    parser.add_argument('idul',
                        default='nom_du_joueur',
                        help="Nom du joueur")
    parser.add_argument('--actions',
                        dest='lister',
                        type=str,
                        nargs=3)
    # écouter le terminal
    args = parser.parse_args()
    # Si des actions ont étées spécifiées, aller aux actions
    if args.lister:
        boucler(args)
    # si c'est le premier tout et que seul un IDUL a été spécifié, débuter la partie
    else:
        debuter(args)
    # kill the parsing
    parser.exit()
    # envoyer le coup au serveur et retourner le nouveau tableau
    # de jeu (requis dans l'ennoncé mais pas utilisé)
    return args


# initialiser un nouveau tableau de jeu
analyser_commande()