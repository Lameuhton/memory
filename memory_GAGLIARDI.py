from random import randint, shuffle
from copy import deepcopy
import re


NB_CARTES_MIN = 4
NB_CARTES_MAX = 30
NOMBRE_RANGEE_MATRICE = 2


def saisir_nombre_cartes():
    """
    Acquiert et retourne un nombre de cartes valide (nombre pair entre 4 et 30)
    :return: int: le nombre de cartes max constituant le jeu
    """
    nb_carte = input("Entrez le nombre maximum de carte: ")

    expression = '^\d\d?$'
    resultat = re.match(expression, nb_carte)

    while resultat == None or (NB_CARTES_MIN > int(nb_carte) or int(nb_carte) > NB_CARTES_MAX) or int(
            nb_carte) % 2 != 0:
        nb_carte = input("Nombre incorrect, veuillez entrer un nombre ENTIER  et PAIR entre 4 et 30: ")
        resultat = re.match(expression, nb_carte)

    return nb_carte


def creation_plateau(nombre_max):
    """
    Crée une liste 2D de 2 lignes comprenant une série de chiffres mélangés, en double.
    :param nombre_max: int, nombre maximum de cartes qui constituera le jeu
    :return: list, liste 2D contenant les nombres du plateau de jeu
    """
    plateau = []
    liste = []
    temp = int(int(nombre_max)/2)

    for i in range(temp):
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
            ligne = int(i[0])
            colonne = int(i[1])
            plateau_comparaison[ligne - 1][colonne - 1] = plateau[ligne - 1][colonne - 1]

    return plateau_comparaison


def convertir_en_texte(liste2D):
    """
    Transforme une liste2D en un texte.
    :param liste2D: list, liste 2D
    :return: str, représentation textuelle de la matrice
    """
    matrice_convertie = ""

    for indexColonne in range(0,2):

        matrice_convertie = matrice_convertie + "| "

        for indexLigne in range(0,len(liste2D[0])):
            matrice_convertie = matrice_convertie + str(liste2D[indexColonne][indexLigne])
            matrice_convertie = matrice_convertie + " | "

        matrice_convertie = matrice_convertie + "\n"

    return matrice_convertie


def valider_position_carte(position, axe, nombre_max = 2):
    """
    Vérifie que la valeur donnée par le joueur est un nombre entier compris entre 1 et le nombre d'éléments maximum pour un axe donné (ligne ou colonne).
    :param position: str: valeur saisie par l'utilisateur
    :param axe: str: 'ligne' ou 'colonne'
    :param nombre_max: int: nombre de cartes contenues dans le plateau de jeu
    :return: bool, True si le nombre est valide, False sinon.
    """
    if axe == 'ligne':
        if int(position) == 1 or int(position) == 2:
            resultat = True
        else:
            resultat = False
    else:
        if 1 <= int(position) <= int(nombre_max/2):
            resultat = True
        else:
            resultat = False

    return resultat

#_____________________________________________________________________________________________________

def saisir_position_une_carte(vue_plateau):
    """
    Obtient le numéro de la ligne et le numéro de la colonne valides d'un joueur.
    Verifie que le numéro de ligne et le numéro de la colonne ne représente pas la position d'une carte déjà retournée
    :param vue_plateau: list, liste2D representant une vue du plateau de jeu
    :return: tuple;  contenant le numéro de la ligne et de la colonne.
    """
    nb_carte = len(vue_plateau[0]) + len(vue_plateau[1])

    carte_ligne = int(input("Numéro de ligne: "))

    while not valider_position_carte(carte_ligne, 'ligne', nb_carte) or carte_ligne == '*':
        carte_ligne = input("Veuillez entrer un numéro de ligne correct: ")

    carte_colonne = int(input("Numéro de colonne: "))

    while not valider_position_carte(carte_colonne,'colonne', nb_carte) or carte_colonne == '*':
        carte_colonne = input("Veuillez entrer un numéro de colonne correct: ")

    return (carte_ligne,carte_colonne)


def saisir_position_deux_cartes(vue_plateau):
    """
    Obtient la position de la première carte, puis la position de la deuxième carte.
    Verifie que le numéro de la position de la deuxième carte ne soit pas identique à la première.
    :param vue_plateau: list, liste2D representant une vue du plateau de jeu
    :return: positions: tuple; contenant la ligne et la colonne de la première carte, ainsi que la ligne et la colonne de la deuxième carte
    """
    print("\n>>>Première carte")
    carte1 = saisir_position_une_carte(vue_plateau)
    print("\n>>>Deuxième carte")
    carte2 = saisir_position_une_carte(vue_plateau)

    while carte1 == carte2:
        print("Cette carte est déjà retournée, saisissez une autre carte.")
        carte2 = saisir_position_une_carte(vue_plateau)

    return (carte1,carte2)


def jouer(plateau):
    """
    Fonction de jeu qui
    -	affichera le numéro du tour
    -	créera la vue du plateau en tenant compte des cartes déjà révélées (en utilisant creer_vue_plateau())
    -	affichera cette vue
    -	obtiendra les positions des deux cartes
    -	créera la vue du plateau en tenant compte des cartes déjà révélées et des positions des deux cartes (en utilisant creer_vue_plateau())
    -	affichera cette vue
    -	/!\ Si les deux cartes sont identiques, leurs positions seront ajoutées à la liste contenant les positions des cartes à révéler
    :param plateau: list, list2D représentant le plateau de jeu
    """
    tour = 0
    cartes_retourner = []
    nb_carte = len(plateau[0]) + len(plateau[1])

    while len(cartes_retourner) != nb_carte:

        tour += 1

        print("----------------------------------------")
        print(f"TOUR {tour}")
        print("----------------------------------------")
        print(convertir_en_texte(creer_vue_plateau(plateau,cartes_retourner)))

        #Demande les positions des deux cartes et les ajoute à la liste
        positions_cartes = saisir_position_deux_cartes(plateau)
        position_carte1 = positions_cartes[0]
        position_carte2 = positions_cartes[1]
        cartes_retourner.append(position_carte1)
        cartes_retourner.append(position_carte2)

        #Affiche le plateau avec les deux cartes retournées (+ les autres)
        print(convertir_en_texte(creer_vue_plateau(plateau, cartes_retourner)))

        #Vérifie si les deux cartes retournées sont identiques
        #Si oui: ne fais rien, si non: les enlève de la liste des cartes à retourner
        ligne_carte_1 = int(position_carte1[0])
        colonne_carte_1 = int(position_carte1[1])

        ligne_carte_2 = int(position_carte2[0])
        colonne_carte_2 = int(position_carte2[1])

        temp = plateau[ligne_carte_1-1]
        carte1 = temp[colonne_carte_1-1]

        temp = plateau[ligne_carte_2-1]
        carte2 = temp[colonne_carte_2-1]

        if carte1 != carte2:
            del cartes_retourner[-1]
            del cartes_retourner[-1]
        else:
            pass

    print(f"Bravo! Vous avez fini votre partie en {tour} tours!")
    pass


def _main():
    nbre_cartes = saisir_nombre_cartes()
    plateau = creation_plateau(nbre_cartes)
    jouer(plateau)


if __name__ == '__main__':
    _main()
