from collections import namedtuple
from random import shuffle
import re


def getValeur(cartes):
    """"Retourne la valeur du jeu passé en paramètre """
    score = 0
    nbAs = 0
    for carte in cartes:
        if carte.valeur in list('JQK'):
            score += 10
        elif carte.valeur == 'A':
            nbAs += 1
        else:
            score += carte.valeur
    for _ in range(nbAs):#La valeur des As sont ajoutés à la fin pour gérer s'ils valent 1 ou 11
        if score > 10:
            score += 1
        else:
            score += 11
    return score

def format_main(cartes):
    """Un jeu est passé en paramètre  et il est mis en forme pour son affichage"""
    tab={'2': ':two:','3': ':three:','4': ':four:','5': ':five:','6': ':six:','7': ':seven:','8': ':eight:',
         '9': ':nine:','10': ':keycap_ten:','J': ':regional_indicator_j:','Q': ':regional_indicator_q:',
         'K': ':regional_indicator_k:','A': ':regional_indicator_a:'}
    return ", ".join(f"{tab[str(carte.valeur)]}{carte.couleur}" for carte in cartes)

def nouveauDeck(nombreJeu):
    """Forme un nouveau sabot avec le nombres de jeux passé en paramètre"""
    valeurs = [n for n in range(2, 11)] + list('JQKA')
    couleurs = [':spades:',':hearts:',':clubs:',':diamonds:']

    Carte = namedtuple('Carte', ['valeur', 'couleur'])
    Carte.__str__ = lambda self: "{self.valeur}{self.couleur}"

    jeu_de_cartes = [Carte(valeur, couleur)
                     for couleur in couleurs
                     for valeur in valeurs
                     for _ in range(nombreJeu)]

    shuffle(jeu_de_cartes)

    return jeu_de_cartes

def getResultat(banque, joueur, jeuCarte):
    """Donne le verdict en fonction d'un jeu et du résultat de la banque qui est gérée également"""
    scoreBanque = getValeur(banque)
    scoreJoueur = getValeur(joueur)
    resultat = "Perdu"

    if scoreJoueur == 21 and len(joueur) == 2:
        resultat = "Blackjack"
        if scoreBanque >= 10 and len(banque) == 1:
            banque.append(jeuCarte.pop())

        if scoreBanque == 21 and len(banque) == 2:
            resultat = "Egalité"
    elif scoreJoueur <= 21:
        while scoreBanque < 17:
            banque.append(jeuCarte.pop())
            scoreBanque = getValeur(banque)
        if scoreBanque > 21 or scoreJoueur > scoreBanque:
            resultat = "Gagné"
        elif scoreBanque == scoreJoueur:
            resultat = "Egalité"

    return resultat

class demarrageJeu:
    """Initialisation du jeu et démarrage de la partie"""
    def __init__(self, game):
        self.game=game

    def run(self, texte):
        if texte == 'start game':
            self.game.jeu_de_cartes = nouveauDeck(6)
            self.game.somme = 100
            self.game.etape = choixMise(self.game)
            return f"Somme de départ : {self.game.somme}\n\nChoisissez votre mise (2-500 nombre pair)"
        else:
            return "Pour commencer une partie de Blackjack taper 'start game'"

class choixMise:
    """Verification de la mise"""
    def __init__(self, game):
        self.game = game

    def run(self, texte):
        expression = r"^[1-9][0-9]*$"
        if re.search(expression, texte):
            self.game.choixMise = int(texte)
        else:
            return "Entrée incorrect\n\nChoisissez votre mise (2-500 nombre pair)"
        if self.game.choixMise > 500:
            return "Somme dépassant la limite de la table\n\nChoisissez votre mise (2-500 nombre pair)"
        elif self.game.choixMise < 2:
            return "La mise minimum est de 2 jeton\n\nChoisissez votre mise (2-500 nombre pair)"
        elif self.game.choixMise % 2 == 1:
            self.game.choixMise -= 1
        tirer=tirerCartes(self.game)
        return tirer.run()

class tirerCartes:
    """Tirage des cartes"""
    def __init__(self, game):
        self.game = game

    def run(self):
        if (self.game.somme - self.game.choixMise) >= 0:
            self.game.somme -= self.game.choixMise
            self.game.banque = [self.game.jeu_de_cartes.pop() for _ in range(1)]
            self.game.joueur = {1: [self.game.jeu_de_cartes.pop() for _ in range(2)]}
            self.game.etat = {1: True}
            self.game.mise = {1: self.game.choixMise}

            reponse = ""
            if self.game.joueur[1][0].valeur == self.game.joueur[1][1].valeur:
                if (self.game.somme - self.game.choixMise) >= 0:
                    reponse += f"Voulez-vous splitter? (oui/non)\n"
                    self.game.etape=split(self.game)
                else:
                    reponse += f"Somme insuffisante pour splitter\n"
                    reponse += f"Que voulez-vous faire ? (tirer,rester,doubler) "
                    self.game.etape = tourJoueur(self.game)
            else:
                reponse += f"Que voulez-vous faire ? (tirer,rester,doubler) "
                self.game.etape = tourJoueur(self.game)

            if getValeur(self.game.joueur[self.game.compteur]) > 20:
                resultat = gestionResultat(self.game)
                return resultat.run()

            else:
                return f"Banque :\n     Main : {format_main(self.game.banque)}\nJoueur :\n     Mise : {self.game.mise[1]}\n" \
                       f"     Main : {format_main(self.game.joueur[1])}\n" + reponse
        else:
            return "Somme insuffisante choisissez une autre mise (2-500 nombre pair)"

class split:
    """Gestion su split"""
    def __init__(self, game):
        self.game = game

    def run(self, texte):
        if texte == "oui":
            self.game.joueur[2] = [self.game.joueur[1].pop()]
            self.game.etat[2] = True
            self.game.mise[2] = self.game.choixMise
            self.game.somme -= self.game.choixMise
        elif texte != "non":
            return "Entrée incorrect"
        self.game.etape = tourJoueur(self.game)
        reponse = ""
        for key, value in self.game.joueur.items():
            reponse += f"Joueur jeu{key} :\n     Mise : {self.game.mise[key]}\n     Main : {format_main(value)}\n"
        return reponse + f'Que voulez-vous faire pour le jeu 1? (tirer, rester, doubler)'

class tourJoueur:
    """Gestion du tour du joueur"""
    def __init__(self, game):
        self.game = game

    def run(self, texte):
        if self.game.etat[self.game.compteur]:
            if getValeur(self.game.joueur[self.game.compteur]) > 20:
                self.game.etat[self.game.compteur] = False
            elif texte == "rester":
                self.game.etat[self.game.compteur] = False
            elif texte == "doubler" or texte == "tirer":
                self.game.joueur[self.game.compteur].append(self.game.jeu_de_cartes.pop())
                if texte == "doubler":
                    if (self.game.somme - self.game.choixMise) >= 0:
                        self.game.mise[self.game.compteur] *= 2
                        self.game.somme -= self.game.choixMise
                        self.game.etat[self.game.compteur] = False
                    else:
                        return f"Somme insuffisante pour doubler\n"
                if getValeur(self.game.joueur[self.game.compteur]) > 21:
                    self.game.etat[self.game.compteur] = False
            else:
                return "Entrée incorrect"
        reponse = ""
        for key, value in self.game.joueur.items():
            reponse += f"Joueur jeu{key} :\n     Mise : {self.game.mise[key]}\n     Main : {format_main(value)}\n"
        if True in self.game.etat.values():
            while True:
                self.game.compteur += 1
                if self.game.compteur > len(self.game.joueur):
                    self.game.compteur = 1
                if self.game.etat[self.game.compteur]:
                    return reponse + f"Que voulez-vous faire pour le jeu {self.game.compteur}? (tirer,rester,doubler) "
        else:
            resultat = gestionResultat(self.game)
            return resultat.run()


class gestionResultat:
    """Gestion du résultat du tour"""
    def __init__(self, game):
        self.game = game

    def run(self):
        reponse = ""
        reponse += "\nResultat du tour : \n"
        gain = 0
        miseTotal = 0
        for key, value in self.game.joueur.items():
            reponse += f"Joueur jeu{key} :\n     Mise : {self.game.mise[key]}\n     Main : {format_main(value)}\n"
            resultat = getResultat(self.game.banque, value, self.game.jeu_de_cartes)
            if resultat == "Gagné":
                gain += self.game.mise[key] * 2
            elif resultat == "Egalité":
                gain += self.game.mise[key]
            elif resultat == "Blackjack":
                gain += self.game.mise[key] * 2.5
            miseTotal += self.game.mise[key]

        reponse += f"Banque :\n Main: {format_main(self.game.banque)}\n\n"
        if gain - miseTotal >= 0:
            reponse += f"Vous avez gagné {gain-miseTotal} jetons\n"
        else:
            reponse += f"Vous avez perdu {miseTotal-gain} jetons\n"

        self.game.somme += gain
        self.game.compteur = 1
        if self.game.somme < 2:
            self.game.etape = demarrageJeu(self.game)
            return reponse + "Vous n'avez plus assez de jeton\n\nAu revoir"
        else:
            if len(self.game.jeu_de_cartes) < 52:
                self.game.jeu_de_cartes = nouveauDeck(6)
            self.game.etape = rejouer(self.game)
            return reponse + f"Somme actuelle : {self.game.somme}\n\nVoulez vous rejouer un tour? (oui/non)"

class rejouer:
    """Relancement d'un tour ou arrêt du jeu"""
    def __init__(self, game):
        self.game = game

    def run(self, texte):
        if texte == "oui":
            self.game.etape = choixMise(self.game)
            return f"Choisissez votre mise (2-500 nombre pair) "
        elif texte == "non":
            self.game.etape = demarrageJeu(self.game)
            return 'Au revoir'
        else:
            return "Entrée incorrect"

class Game:
    """Classe gérant le déroulement du jeu"""
    def __init__(self):
        self.jeu_de_cartes = []
        self.choixMise = 0
        self.somme = 100
        self.banque = []
        self.joueur = {}
        self.etat = {}
        self.mise = {}
        self.compteur = 1
        self.etape = demarrageJeu(self)

    def etapeSuivante(self, texte):
        """Envoie le texte à la prochaine étape"""
        return self.etape.run(texte)











