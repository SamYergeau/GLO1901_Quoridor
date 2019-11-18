""" Quoridor.py
Module qui enferme les classes d'encapsulation
de la structure du jeu
contient les classes:
    - Quoridor
    - QuoridorError(Exception)
"""
import networkx as nx


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.

    :param joueurs: une liste des positions (x,y) des joueurs.
    :param murs_horizontaux: une liste des positions (x,y) des murs horizontaux.
    :param murs_verticaux: une liste des positions (x,y) des murs verticaux.
    :returns: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # retirer tous les arcs qui pointent vers les positions des joueurs
    # et ajouter les sauts en ligne droite ou en diagonale, selon le cas
    for joueur in map(tuple, joueurs):

        for prédécesseur in list(graphe.predecessors(joueur)):
            graphe.remove_edge(prédécesseur, joueur)

            # si admissible, ajouter un lien sauteur
            successeur = (2*joueur[0]-prédécesseur[0], 2*joueur[1]-prédécesseur[1])

            if successeur in graphe.successors(joueur) and successeur not in joueurs:
                # ajouter un saut en ligne droite
                graphe.add_edge(prédécesseur, successeur)

            else:
                # ajouter les liens en diagonal
                for successeur in list(graphe.successors(joueur)):
                    if prédécesseur != successeur and successeur not in joueurs:
                        graphe.add_edge(prédécesseur, successeur)

    # ajouter les noeuds objectifs des deux joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe


class QuoridorError(Exception):
    """QuoridorError    
    Classe pour gérer les exceptions survenue dans la classe Quoridor    
    Arguments:
        Exception {[type]} -- [description]
    """
    print("quoridorerror")


class Quoridor:

    def __init__(self, joueurs, murs=None):
        """
        __init__
        Initialisation de la classe Quoridor
        Arguments:
            joueurs {list}
                -- Une liste de 2 joueurs. chaque joueur est: (dict) ou (str)
                    - (str): nom du joueur
                    - (dict)
                        + 'nom' (str)   -- Nom du joueur
                        + 'murs' (int)  -- Nombre de murs que le joueur peut encore placer
                        + 'pos' (tuple) -- position (x, y) du joueur
        Keyword Arguments:
            murs {dict} (default: {None})
            -- 'horzontaux': [list of tuples]
                Une liste de tuples (x, y) représentant la position des différents
                murs horizontaux dans la partie
        """
        # définir les attribut de classes que nous allons utiliser
        self.joueurs = []
        self.murh = []
        self.murv = []
        # vérifier que joueurs est itérable et de longueur 2
        if len(joueurs) != 2:
            raise QuoridorError("Il n'y a pas exactement 2 joueurs!")
        # itérer sur chaque joueur
        for numero, joueur in enumerate(joueurs):
            # Vérifier s'il s'agit d'un string
            # Si le joueur est un string
            if isinstance(joueur, str):
                # créer un dictionnaire vide
                nouveaujoueur = {}
                # ajouter le nom au dictionnaire
                nouveaujoueur['nom'] = joueur
                # ajouter 10 murs à placer au joueur
                nouveaujoueur['murs'] = 10
                # placer le joueur au bon endroit sur le jeu
                if numero == 0:
                    nouveaujoueur['pos'] = (5, 1)
                else:
                    nouveaujoueur['pos'] = (5, 9)
                # créer le joueur dans l'objet de classe
                self.joueurs[numero] = nouveaujoueur #TODO: remplacer nouveaujoueur par juste self.player
            # Si le joueur fourni est un dictionnaire
            else:
                # vérifier que les murs sont legit
                if  0 < joueur['murs'] > 10:
                    raise QuoridorError("mauvais nombre de murs!")
                # Vérifier que la position du joueur est valide
                if 1 < joueur['pos'] > 9:
                    raise QuoridorError("position du joueur invalide!")
                # updater la valeur de joueur
                self.joueurs[numero] = joueur
        # vérifier si un dictionnaire de murs est présent
        if murs:
            # vérifier si murs est un tuple
            if not(isinstance(murs, dict)):
                raise QuoridorError("murs n'est pas un dictionnaire!")
            # itérer sur chaque mur horizontal
            for mur in murs['horizontaux']:
                # Vérifier si la position du mur est valide
                if 1 < mur[0] > 8 and 2 < mur[1] > 9:
                    raise QuoridorError("position du mur non-valide!")
                self.murh += mur
            # itérer sur chaque mur vertical
            for mur in murs['verticaux']:
                if 2 < mur[0] > 9 and 1 < mur[1] > 8:
                    raise QuoridorError("position du mur non-valide!")
                self.murv += mur
        # Vérifier que le total des murs donne 20
        if (len(self.murh) + len(self.murv) + self.joueurs[0]['murs'] + self.joueurs[1]['murs']) != 20:
            raise QuoridorError("mauvaise quantité totale de murs!")

        

