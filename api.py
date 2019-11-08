import requests


# URL du server python à contacter
url_base = 'https://python.gel.ulaval.ca/quoridor/api/'
'''
def lister_parties(idul)
Desctiption:
    Fonction qui permet de demander au serveur une liste des 20 dernières parties jouée par le joueur
Input:
    idul (str):
        L'identifiant IDUL du joueur
Return:
    rep (list):
        Une liste des max 20 dernières parties jouées par le joueur
Note:
    - Si le serveur retourne un message, la fonction soulève une exception RuntimeError suivi de ce message.
'''
def lister_parties(idul):
    rep = requests.get(url_base+'lister/', params={'idul': idul})
    if rep.status_code == 200:
        # la requête s'est déroulée normalement; décoder le JSON
        rep = rep.json()
        # tester pour la présence d'un message dans la réponse
        if "message" in rep:
            raise RuntimeError(rep["message"])
    else:
        print(f"Le GET sur {url_base+'lister'} a produit le code d'erreur {rep.status_code}.")
    return rep


'''
def débuter_partie(idul)
Desctiption:
    Une fonction qui permet de contacter le serveur afin de débuter une partie
Input:
    idul (str)
        L'identifiant IDUL du joueur
Return:
    rep (dict)
        Un dictionnaire contenant:
            - 'id' (str):
                L'identifiant unique de la partie
            - 'état' (dict):
                Un dictionnaire contenant l'état initial de la partie
Note:
    - Si le serveur retourne un message, la fonction soulève une exception RuntimeError suivi de ce message.
'''
def débuter_partie(idul):
    rep = requests.post(url_base+'débuter/', data={'idul': idul})
    if rep.status_code == 200:
        # la requête s'est déroulée normalement; décoder le JSON
        rep = rep.json()
        # tester pour la présence d'un message dans la réponse
        if "message" in rep:
            raise RuntimeError(rep["message"])
    else:
        print(f"Le GET sur {url_base+'lister'} a produit le code d'erreur {rep.status_code}.")
    return rep