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
        if scoreBanque >= 10 and len(banque) == 1:
            banque.append(jeuCarte.pop())

        if scoreBanque == 21 and len(banque) == 2:
            resultat = "Egalité"
    elif scoreJoueur < 21:
        while scoreBanque < 17:
            banque.append(jeuCarte.pop())
            scoreBanque = getValeur(banque)
        if scoreBanque > 21 or scoreJoueur > scoreBanque:
            resultat = "Gagné"
        elif scoreBanque == scoreJoueur:
            resultat = "Egalité"

    return resultat

class Game:
    def __init__(self):
        self.jeu_de_cartes = []
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
            if texte == 'start game' and self.etape == 0:
                self.jeu_de_cartes = nouveauDeck(6)
                self.somme = 100
                self.etape = 1
                return f"Somme de départ : {self.somme}\n\nChoisissez votre mise (2-500 nombre pair)"
            else:
                return ""
        elif self.etape == 1:
            self.choixMise = int(texte)
            if self.mise > 500:
                return "Somme dépassant la limite de la table\n\nChoisissez votre mise (2-500 nombre pair)"
            elif self.mise % 2 == 1:
                self.mise -= 1
            if (self.somme - self.choixMise) >= 0:
                self.somme -= self.choixMise
                self.banque = [self.jeu_de_cartes.pop() for _ in range(1)]
                self.joueur = {1: [self.jeu_de_cartes.pop() for _ in range(2)]}
                self.etat = {1: True}
                self.mise = {1: self.choixMise}

                reponse = ""
                if self.joueur[1][0].valeur == self.joueur[1][1].valeur:
                    if (self.somme - self.choixMise) >= 0:
                        reponse += f"Voulez-vous splitter? (oui/non)\n"
                        self.etape = 2
                    else:
                        reponse += f"Somme insuffisante pour splitter\n"
                        reponse += f"Que voulez-vous faire ? (tirer,rester,doubler) "
                        self.etape = 3
                else:
                    reponse += f"Que voulez-vous faire ? (tirer,rester,doubler) "
                    self.etape = 3

                if getValeur(self.joueur[self.compteur]) > 20:
                    self.etape=4
                else:
                    return f"Banque :\n     Main : {format_main(self.banque)}\nJoueur :\n     Mise : {self.mise[1]}\n" \
                                                                  f"     Main : {format_main(self.joueur[1])}\n" + reponse
            else:
                return "Somme insuffisante choisissez une autre mise (2-500 nombre pair)"
        elif self.etape == 2:
            self.etape = 3
            if texte == "oui":
                self.joueur[2] = [self.joueur[1].pop()]
                self.etat[2] = True
                self.mise[2] = self.choixMise
                self.somme -= self.choixMise
            reponse = ""
            for key, value in self.joueur.items():
                reponse += f"Joueur jeu{key} :\n     Mise : {self.mise[key]}\n     Main : {format_main(value)}\n"

            return reponse + f'Que voulez-vous faire pour le jeu 1? (tirer, rester, doubler)'
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
                    if getValeur(self.joueur[self.compteur]) > 21:
                        self.etat[self.compteur] = False
            reponse = ""
            for key, value in self.joueur.items():
                reponse += f"Joueur jeu{key} :\n     Mise : {self.mise[key]}\n     Main : {format_main(value)}\n"
            if True in self.etat.values():
                while True:
                    self.compteur += 1
                    if self.compteur > len(self.joueur):
                        self.compteur = 1
                    if self.etat[self.compteur]:
                        return reponse + f"Que voulez-vous faire pour le jeu {self.compteur}? (tirer,rester,doubler) "
            else:
                self.etape=4
        elif self.etape==5:
            if texte == "oui":
                self.etape = 1
                return f"Choisissez votre mise (2-500 nombre pair) "
            else:
                self.etape = 0
                return 'Au revoir'
        reponse = ""
        if self.etape==4:
            reponse += "\nResultat du tour : \n"
            gain = 0
            miseTotal = 0
            for key, value in self.joueur.items():
                reponse += f"Joueur jeu{key} :\n     Mise : {self.mise[key]}\n     Main : {format_main(value)}\n"
                resultat = getResultat(self.banque, value, self.jeu_de_cartes)
                if resultat == "Gagné":
                    gain += self.mise[key] * 2
                elif resultat == "Egalité":
                    gain += self.mise[key]
                elif resultat == "Blackjack":
                    gain += self.mise[key] * 2.5
                miseTotal += self.mise[key]

            reponse += f"Banque : {format_main(self.banque)}\n\n"
            if gain - miseTotal >= 0:
                reponse += f"Vous avez gagné {gain-miseTotal} jetons\n"
            else:
                reponse += f"Vous avez perdu {miseTotal-gain} jetons\n"

            self.etape = 5
            self.somme += gain
            self.compteur=1
            if self.somme <= 0:
                self.etape = 0
                return "Maintenant tu as tout perdu :-)"
            else:
                return reponse + f"Somme actuelle : {self.somme}\n\nVoulez vous rejouer un tour? (oui/non)"