from random import randint, shuffle
from copy import deepcopy
import re


NB_CARTES_MIN = 4
NB_CARTES_MAX = 30
NOMBRE_RANGEE_MATRICE = 2


def creation_plateau(nombre_max):
    """
    Crée une liste 2D de 2 lignes comprenant une série de chiffres mélangés, en double.
    :param nombre_max: int, nombre maximum de cartes qui constituera le jeu
    :return: list, liste 2D contenant les nombres du plateau de jeu
    """
    plateau = []
    liste = []

    for i in range(int(nombre_max / 2)):
        liste.append(i + 1)

    shuffle(liste)
    plateau.append(liste)

    liste2 = liste.copy()
    shuffle(liste2)
    plateau.append(liste2)

    return plateau


def creer_vue_plateau(plateau, positions):
    """
    Crée une vue du plateau actuel pour le joueur.
    Si aucune position n'est spécifiée (la liste positions est vide), la vue ne contiendra que des '*'.
    Si des positions sont spécifiées (e.g.: [(0, 0), (1, 1)]), les cartes se trouvant à ces positions seront révélées (leurs valeurs intégrées à la vue).
    :param plateau: liste, Liste 2D représentant le plateau de jeu.
    :param positions: liste, liste contenant les positions des cartes à révéler.
    :return: list, liste 2D dans laquelle chaque élément contient le symbole '*' ou les cartes révélées
    """

    plateau_comparaison = deepcopy(plateau)

    for counter, value in enumerate(plateau_comparaison):
        for counter2, value2 in enumerate(value):
            plateau_comparaison[counter][counter2] = '*'

    if positions != []:
        for i in positions:
            ligne = i[0]
            colonne = i[1]
            plateau_comparaison[ligne-1][colonne-1] = plateau[ligne-1][colonne-1]

    return plateau_comparaison

def valider_position_carte(position, axe, nombre_max = 2):
    """
    Vérifie que la valeur donnée par le joueur est un nombre entier compris entre 1 et le nombre d'éléments maximum pour un axe donné (ligne ou colonne).
    :param position: str: valeur saisie par l'utilisateur
    :param axe: str: 'ligne' ou 'colonne'
    :param nombre_max: int: nombre de cartes contenues dans le plateau de jeu
    :return: bool, True si le nombre est valide, False sinon.
    """
    if axe == 'ligne':
        if 1 < position < nombre_max:
            resultat = True
        else:
            resultat = False
    else:
        if 1 < position < 2:
            resultat = True
        else:
            resultat = False

    return resultat


plateau = creation_plateau(16)
positions = [(1,1),(1,2),(2,1),(2,2)]
print(creer_vue_plateau(plateau,positions))