from collections import namedtuple
from random import shuffle


def getValeur(cartes):
    score = 0
    nbAs = 0
    for carte in cartes:
        if carte.valeur in list('JQK'):
            score += 10
        elif carte.valeur == 'A':
            nbAs += 1
        else:
            score += carte.valeur
    for _ in range(nbAs):
        if score > 10:
            score += 1
        else:
            score += 11
    return score


def format_main(cartes):
    return ", ".join(f"{carte.valeur}{carte.couleur}" for carte in cartes)


def nouveauDeck(nombreJeu):
    valeurs = [n for n in range(2, 11)] + list('JQKA')
    couleurs = '♠♣♡♢'

    Carte = namedtuple('Carte', ['valeur', 'couleur'])
    Carte.__str__ = lambda self: "{self.valeur}{self.couleur}"

    jeu_de_cartes = [Carte(valeur, couleur)
                     for couleur in couleurs
                     for valeur in valeurs
                     for _ in range(nombreJeu)]

    shuffle(jeu_de_cartes)

    return jeu_de_cartes


def getResultat(banque, joueur, jeuCarte):
    scoreBanque = getValeur(banque)
    scoreJoueur = getValeur(joueur)
    resultat = "Perdu"

    if scoreJoueur == 21 and len(joueur) == 2:
        resultat = "Blackjack"
    elif scoreJoueur < 21:
        while scoreBanque < 17:
            banque.append(jeuCarte.pop())
            scoreBanque = getValeur(banque)
        if scoreBanque > 21 or scoreJoueur > scoreBanque:
            resultat = "Gagné"
        elif scoreBanque == scoreJoueur:
            resultat = "Egalité"

    return resultat


def tour(jeuCartes, somme):
    choixMise = 0
    while True:
        choixMise = int(input("Choisissez votre mise? (1-100)"))
        if (somme - choixMise) >= 0:
            break
        else:
            print("Somme insuffisante choisissez une somme correcte")

    somme -= choixMise

    banque = [jeuCartes.pop() for _ in range(1)]
    joueur = {1: [jeuCartes.pop() for _ in range(2)]}
    etat = {1: True}
    mise = {1: choixMise}

    print(f"Banque :\n     Main : {format_main(banque)}")
    print(f"Joueur :\n     Mise : {mise[1]}\n     Main : {format_main(joueur[1])}")

    if joueur[1][0].valeur == joueur[1][1].valeur:
        if (somme - choixMise) >= 0:
            reponse = input("Voulez-vous splitter? (oui/non)")
            if reponse == "oui":
                joueur[2] = [joueur[1].pop()]
                etat[2] = True
                mise[2] = choixMise
                somme -= choixMise
        else:
            print("Somme insuffisante pour splitter")

    while (True in etat.values()):
        for key, value in joueur.items():
            if getValeur(value) > 20:
                etat[key] = False
            if etat[key]:
                print(f"Joueur jeu{key} :   Mise :{mise[key]} Main :{format_main(value)}")
                reponse = input("Que voulez-vous faire ? (tirer,rester,doubler) ")
                if reponse == "rester":
                    etat[key] = False
                else:
                    value.append(jeuCartes.pop())
                    if reponse == "doubler":
                        if (somme - choixMise) >= 0:
                            mise[key] *= 2
                            somme -= choixMise
                            etat[key] = False
                        else:
                            print("Somme insuffisante pour doubler")

    print("Resultat du tour : ")
    gain = 0
    miseTotal = 0
    for key, value in joueur.items():
        print(f"Joueur jeu{key} :   Mise :{mise[key]} Main :{format_main(value)}")
        resultat = getResultat(banque, value, jeuCartes)
        if resultat == "Gagné":
            gain += mise[key] * 2
        elif resultat == "Egalité":
            gain += mise[key]
        elif resultat == "Blackjack":
            gain += mise[key] * 2.5
        miseTotal += mise[key]

    print(f"Banque : {format_main(banque)}")
    if gain - miseTotal >= 0:
        print(f"Vous avez gagné {gain-miseTotal} jetons")
    else:
        print(f"Vous avez perdu {miseTotal-gain} jetons")

    return somme + gain


class Game:
    def __init__(self):
        self.jeu_de_cartes = nouveauDeck(4)
        self.choixMise = 0
        self.somme = 100
        self.banque = []
        self.joueur = {}
        self.etat = {}
        self.mise = {}
        self.etape = 0
        self.compteur = 1

    def etapeSuivante(self, texte):
        if texte == 'quit':
            return "quitter"
        elif self.etape == 0:
            if texte == 'start game':
                self.etape = 1
                return f"Somme de départ : {self.somme}\n\nChoisissez votre mise (1-100) "
            else:
                return ""
        elif self.etape == 1:
            self.choixMise = int(texte)
            if (self.somme - self.choixMise) > 0:
                self.somme -= self.choixMise
                self.banque = [self.jeu_de_cartes.pop() for _ in range(1)]
                self.joueur = {1: [self.jeu_de_cartes.pop() for _ in range(2)]}
                self.etat = {1: True}
                self.mise = {1: self.choixMise}

                str0 = ""
                if self.joueur[1][0].valeur == self.joueur[1][1].valeur:
                    if (self.somme - self.choixMise) >= 0:
                        str0 += f"Voulez-vous splitter? (oui/non)\n"
                        self.etape = 2
                    else:
                        str0 += f"Somme insuffisante pour splitter\n"
                        str += f"Que voulez-vous faire ? (tirer,rester,doubler) "
                        self.etape = 3
                else:
                    str0 += f"Que voulez-vous faire ? (tirer,rester,doubler) "
                    self.etape = 3

                if getValeur(self.joueur[self.compteur]) > 20:
                    self.etape=4
                else:
                    return f"Banque :\n     Main : {format_main(self.banque)}\nJoueur :\n     Mise : {self.mise[1]}\n" \
                                                                  f"     Main : {format_main(self.joueur[1])}\n" + str0
            else:
                return "Somme insuffisante choisissez une autre mise (1-100)"
        elif self.etape == 2:
            self.etape = 3
            if texte == "oui":
                self.joueur[2] = [self.joueur[1].pop()]
                self.etat[2] = True
                self.mise[2] = self.choixMise
                self.somme -= self.choixMise
            str2 = ""
            for key, value in self.joueur.items():
                str2 += f"Joueur jeu{key} :\n     Mise : {self.mise[key]}\n     Main : {format_main(value)}\n"

            return str2 + f'Que voulez-vous faire pour le jeu 1? (tirer,rester,doubler)'
        elif self.etape == 3:
            if self.etat[self.compteur]:
                if getValeur(self.joueur[self.compteur]) > 20:
                    self.etat[self.compteur] = False
                elif texte == "rester":
                    self.etat[self.compteur] = False
                else:
                    self.joueur[self.compteur].append(self.jeu_de_cartes.pop())
                    if texte == "doubler":
                        if (self.somme - self.choixMise) >= 0:
                            self.mise[self.compteur] *= 2
                            self.somme -= self.choixMise
                            self.etat[self.compteur] = False
                        else:
                            return f"Somme insuffisante pour doubler\n"
                self.compteur += 1
            str3 = ""
            for key, value in self.joueur.items():
                str3 += f"Joueur jeu{key} :\n     Mise : {self.mise[key]}\n     Main : {format_main(value)}\n"
            if True in self.etat.values():
                while True:
                    if self.compteur > len(self.joueur):
                        self.compteur = 1
                    if self.etat[self.compteur]:
                        return str3 + f"Que voulez-vous faire pour le jeu {self.compteur}? (tirer,rester,doubler) "
                    else:
                        self.compteur += 1
            else:
                self.etape=4
        elif self.etape==5:
            if texte == "oui":
                self.etape = 1
                return f"Choisissez votre mise (1-100) "
            else:
                return 'Au revoir'
        str3=""
        if self.etape==4:
            str3 += "\nResultat du tour : \n"
            gain = 0
            miseTotal = 0
            for key, value in self.joueur.items():
                str3 += f"Joueur jeu{key} :\n     Mise : {self.mise[key]}\n     Main : {format_main(value)}\n"
                resultat = getResultat(self.banque, value, self.jeu_de_cartes)
                if resultat == "Gagné":
                    gain += self.mise[key] * 2
                elif resultat == "Egalité":
                    gain += self.mise[key]
                elif resultat == "Blackjack":
                    gain += self.mise[key] * 2.5
                miseTotal += self.mise[key]

            str3 += f"Banque : {format_main(self.banque)}\n\n"
            if gain - miseTotal >= 0:
                str3 += f"Vous avez gagné {gain-miseTotal} jetons\n"
            else:
                str3 += f"Vous avez perdu {miseTotal-gain} jetons\n"

            self.etape = 5
            self.somme += gain
            self.compteur=1
            return str3 + f"Somme actuelle : {self.somme}\n\nVoulez vous rejouer un tour? (oui/non)"