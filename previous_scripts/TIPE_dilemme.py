"""" On peut ainsi résumer le jeu en : chaque joueur choisit une
stratégie, et la règle du jeu définit alors un gain pour chaque joueur. """


import random as rd
import numpy as np
import matplotlib.pyplot as plt



"""Match à n parties (DIP)"""

def dilemme(coopere): #définira le gain de chacun des deux joueurs. True=coopérer, False=trahir
#coopere[0] est l'action choisie par J1, coopere[1] est celle de J2, et le gain retourné est dans le même ordre : [gain J1, gain J2]
    if coopere[0] :
        if coopere[1] :
            return [3,3]
        else :
            return [0,5]
    else :
        if not coopere[1] :
            return [1,1]
        else :
            return [5,0]



def partie(strat1,strat2,gains,coups): #fait s'affronter deux stratégies une seule fois, en fonction du tour précédent.
    invG = inverser(gains.copy())
    invC = inverser(coups.copy())
    J1,J2 = strat1(gains,coups),strat2(invG,invC)
    coups[0].append(J1)
    coups[1].append(J2)
    return dilemme([J1,J2]), coups #me retourne le résultat de la partie (en gain) et les coups joués par les deux adversaires



def match(n,strat1,strat2) : #n nombre de parties par affrontement. il retourne la liste des gains cumulés
    gains = [[],[]] #gains contient toutes les données mises à jour après une partie.
    coups = [[],[]] #gains est mis à jour dans match, et coups est mis à jour dans partie
    for k in range(n) :
        game = partie(strat1,strat2,gains,coups)
        gains[0].append(game[0][0])
        gains[1].append(game[0][1])
        coups = game[1]
    return gains #la fonction retourne la liste complète des gains à la fin d'un match



def compte(n,strat1,strat2) : #traite la liste des gains envoyée par match
    points = match(n,strat1,strat2) #points ne retient que les gains cumulés, il oublie les coups des joueurs...
    s1,s2 = 0,0 #s1 et s2 sont respectivement le nombre de points accumulés des deux joueurs.
    for k in points[0] :
        s1 += k
    for k in points[1] :
        s2 += k
    return s1, s2 #la fonction retourne le total des points (séparément) des deux joueurs à l'issue d'un match



def inverser(L) : #permet de faire passer la liste des gains [j1,j2] à [j2,j1] pour implémenter toutes les stratégies comme si elles étaient j1
    a = L[0].copy()
    L[0] = L[1].copy()
    L[1] = a.copy()
    return L




def tournoi(n, S) : #fait s'affronter une liste de stratégies. chaque stratégie s'affronte une fois. la fonction prend une liste de stratégies en paramètre ainsi que le nombre de parties par match
    m = len(S)
    result = np.zeros((m,m),dtype = int) #result est un tableau carré de zéros, qui va se remplir case par case
    for k in range(m) :
        for l in range(k+1) :
            a = compte(n,S[k],S[l])
            result[k,l], result[l,k] = a[0], a[1]
    return result #au final on a le tableau à double entrée qui associe aux stratégies des lignes ses gains contre les stratégies des colonnes


""""
S = [gentille,mechante,tit_for_tat,mefiante,random,soft_majo,spiteful]
tournoi(10)
array([[30,  0, 30, 15,  9, 30, 30],
       [50, 10, 14, 30, 26, 14, 14],
       [30,  9, 30, 25, 21, 30, 30],
       [40,  5, 25, 20, 12, 25,  9],
       [44,  6, 26, 27, 24, 28, 10],
       [30,  9, 30, 25, 23, 30, 30],
       [30,  9, 30, 29, 25, 30, 30]])

on a bien gentille a 30 points contre gentille, mechante a 50 points contre gentille, ou encore spiteful marque 9 points
contre mechante alors que mechante en marque 14
"""


def total(n, S) : #permet de compter le total des points à l'isssue du tournoi
    result = tournoi(n,S)
    m = len(result)
    Ltot = [0]*m
    for k in range(m) :
        for i in range(m) :
            Ltot[k] += result[k,i]
    return Ltot #retourne une liste des gains, dans le même ordre des stratégies que S



def histogramme(n, S, Snom) : #prend en paramètre une liste de stratégies
    """
        Shows an histogram of earnings at the end of the tournament
    """
    Ltot = total(n,S) #liste des gains cumulés sur 1 tournoi entier
    s = len(S)

    x = [k for k in range(s)]
    width = 0.3
    BarName = Snom.copy()
    plt.bar(x, Ltot, width, color='blue' )
    plt.xlim(-1,s)
    plt.ylim(min(Ltot)-100,max(Ltot)+100)
    plt.ylabel('Total des Points')
    plt.title('Résultats du tournoi')
    plt.xticks(x, BarName, rotation=26)
    plt.show()



def classement(n,S,Snom) : #renvoie la liste des noms des stratégies triée dans l'orde du plus petit gain au plus grand
    """
        Shows a ranking of strategies at the end of the tournament
    """
    Ltot = total(n,S) #récupère la liste des gains
    Stl = [[Ltot[k], Snom[k]] for k in range(len(S))] #crée une liste de la forme [[G1,S1],[G2,S2],[G3,S3],[G4,S4]...]
    ranking = Hoare(Stl) #utilise la fonction de tri pour ordonner les stratégies
    rank = [k[1] for k in ranking] #récupère de ranking uniquement les noms des stratégies dans l'ordre
    return rank






"""stratégies"""

## chaque stratégie a la liste des gains et la liste des coups de tous les tours précédents.
## mais toutes les stratégies ne s'en serviront pas forcément.


def gentille(gains, coups) : #all_c
    return True



def mechante(gains, coups) : #all_t
    return False



def tit_for_tat(gains, coups) :
    if len(gains[0]) == 0 :
           return True
    else :
        return coups[1][-1]



def mefiante(gains,coups) : # joue périodiquement tc en commencant par t
    if len(gains[0]) % 2 == 0 :
        return False
    else :
        return True



def indecise(gains,coups) : # joue périodiquement ct en commencant par c
    if len(gains[0]) % 2 == 0 :
        return True
    else :
        return False



def random(gains, coups) : #joue aléatoirement
    a = rd.randint(1,2)
    if a == 1 :
        return True
    else :
        return False



def soft_majo(gains, coups) : #joue ce que l'autre a joué en majorité, et joue c au premier coup ou en cas d'égalité
    def scount(coups) :
        c = 0
        for k in coups[1] :
            if k :
                c += 1
        if c >= (len(coups[1]))/2 :
            return True
        else :
            return False

    if len(gains[0]) == 0 or scount(coups) :
        return True
    elif not scount(coups) :
        return False



def spiteful(gains, coups) : #joue c jusqu'à ce que l'autre trahisse, puis trahit tout le temps
    if counter_true(coups) != len(coups[0]) :
        return False
    else :
        return True



def sondeur(gains, coups) : # aux 3 premiers coups il joue tcc, puis t tout le temps si l'adversaire a coopéré aux tours 2 et 3, donnant donnant sinon
    l = len(gains[0])
    if l == 0 :
        return False
    if l == 1 or l == 2 :
        return True
    if coups[1][1] and coups[1][2] :
        return False
    else :
        return tit_for_tat(gains, coups)



def periodic_cct(gains, coups) : #joue cooperer cooperer trahir périodiquement
    l = len(gains[0])%3
    if l == 0 or l == 1:
        return True
    else :
        return False



def periodic_ttc(gains, coups) : #joue trahir trahir coopérer périodiquement
    l = len(gains[0])%3
    if l == 0 or l == 1:
        return False
    else :
        return True



def hard_majo(gains, coups) : #trahit au premier coup ou si l'adversaire a majoritairement trahit. coopere sinon.
    def hcount(coups) :
        c = 0
        for k in coups[1] :
            if k :
                c += 1
        if c > (len(coups[1]))/2 :
            return True
        else :
            return False

    if len(gains[0]) == 0 or not hcount(coups) :
        return False
    elif hcount(coups) :
        return True



def pavlov(gains, coups) : #coopère au premier coup puis coopère seulement si les deux stratégies ont joué la même chose
    if len(gains[0]) == 0 :
        return True
    elif coups[-1] == [True,True] or coups[-1] == [False,False] :
        return True
    else :
        return False




def gradual(gains, coups) :
    """
        seq est une liste des coups qu'il a prévu de renvoyer, 
        il renvoie la donnée qui est en premier dans la liste.
    """
    l = len(coups[0])
    if l == 0 :
        global seq
        seq = [[],0]
        return True
    elif len(seq[0]) != 0 :
        ans = seq[0][0]
        del seq[0][0]
        return ans
    elif len(seq[0]) == 0 :
        c = l - counter_true(coups)
        if seq[1] < c :
            seq[1] = c
            seq[0] = [False]*(c-1) + [True]*2
            return False
        elif seq[1] == c :
            return True




def probability_gradual(gains, coups) :
    """
        même stratégie que gradual, sauf qu'elle arrête de punir 
        son adversaire avec une probabilité 1/n
    """
    l = len(coups[0])
    if l == 0 :
        global seq
        seq = [[],0]
        return True
    elif len(seq[0]) != 0 :
        ans = seq[0]
        del seq[0]
        return ans
    elif len(seq[0]) == 0 :
        c = l - counter_true(coups)
        if seq[1] < c :
            seq[1] = c
            seq[0] = [False]*(c-1) + [True]*2
            return False
        elif seq[1] == c :
            return True





def ca_strat(gains, coups) : #coopère jusqu'à ce que l'autre trahisse n fois, n augmente de 50 % à chaque fois que l'autre coopère
    l = len(coups[1])
    percent = 0.5
    
    if l == 0 :
        global threshold
        threshold = 1
        global reached_threshold
        reached_threshold = False
        return True
    else :
        if reached_threshold :
            return False
        f = l - counter_true(coups) # = counter_false
        if f >= threshold :
            reached_threshold = True
            return False
    if coups[1][-1] :
        threshold += threshold * percent
    return True



def so_strat(gains, coups) : #trahit 50 fois, puis coopère une fois, si l'autre coopère, elle coopère tout le temps, sinon elle trahit tout le temps
    l = len(gains[0])
    if l < 50 :
        return False
    if l == 50 :
        return True
    return coups[1][50]



def cam_strat(gains, coups) :
    l = len(gains[0])
    if l == 0 or l == 3 or l == 4 :
        return True
    elif l == 1 or l == 2 :
        return False 
    elif l < 40 :
        if not coups[1][0] :
            return False
        
        
#et après 60 je regarde les moyennes des gains, et j'adapte ma stratégie en fonction
        


#strat qui lit les deux derniers coups qu'elle a joué, elle regarde ce que son adversaire 
# a joué en réaction à ces deux coups, fait des stats de ces données et joue en prévoyant le coup
#suivant de son adversaire.
#clem_strat
    






Sdebase = [gentille,mechante,tit_for_tat,mefiante,indecise,random,soft_majo,spiteful,sondeur,periodic_cct,gradual]
Snomdebase = ['gentille','mechante','tit_for_tat','mefiante','indecise','random','soft_majo','spiteful','sondeur','periodic_cct','gradual']


Sfam = [ca_strat,so_strat]
Sfamnom = ['ca_strat', 'so_strat']



"""
gagner un match signifie marquer plus de points à la fin du match, les points sont les gains cumulés
sur n parties.
match nul = autant de points
perdre = moins de points



Robert Axelrod a fait un tournoi informatique dans lequel chaque stratégie affronte les autres
dans un match avec mille itérations.
"""







"""fonctions pour m'aider à implémenter le programme"""




def counter_true(coups) : #compte le nombre de cooperations de l'adversaire
    c = 0
    for k in coups[1] :
        if k :
            c += 1
    return c


def counter_while_false(coups) :
    k = len(coups[1])
    c = 0
    while not coups[0][k-1] :
        if k-1 >= 0 :
            c += 1
            k -= 1
    return c



def somme(L) :
    s = 0
    for k in L :
        s += k
    return s



def Hoare(L) : #L est une liste de couples de la forme [gain,stratégie]
    l = len(L) #Hoare est une fonction de quicksorting par récursion
    if l == 1 or l == 0 :
        return L
    else :
        pivot = L[-1]
        xhaut = [x for x in L[:-1] if x[0] >= pivot[0]]
        xbas = [x for x in L if x[0] < pivot[0]]
        return Hoare(xhaut) + [pivot] + Hoare(xbas) #j'inverse l'ordre de la liste
    


def Hoare_class(L) : #L est une liste d'objets d'une classe contenant un attribu gain
    l = len(L)
    if l == 0 or l == 1 :
        return L
    else :
        pivot = L[-1]
        xhaut = [x for x in L[:-1] if x.gain >= pivot.gain]
        xbas = [x for x in L if x.gain < pivot.gain]
        return Hoare_class(xhaut) + [pivot] + Hoare_class(xbas)

    







"""Début de la Génétique """





class strategy :

    """classe des stratégies. """


    def __init__(self, strat, stratname, Nindiv) :
        self.strat = strat
        self.stratname = stratname
        self.individuals = Nindiv
        self.gain = 0
        self.trace = 0 #pour le graph à la fin


    def repop_1(self, Gtot) : #les repop_k mettent à jour l'attribut individuals et remettent gain = 0
        self.individuals = int(self.gain * Ntot / Gtot)
        self.gain = 0





def stratlist(N, S, Snom) : #N est le nombre d'individus par stratégie, fixe au début de la simulation
    stratL = [] #fonction qui créée une liste d'objets strategy
    for k in range(len(S)) :
        stratL.append(strategy(S[k], Snom[k], N))
    global Ntot
    Ntot = len(S)*N
    return stratL



def indivlist(stratL) : # a partir de stratlist, crée une liste de d'individus (et la liste des noms qui va avec)
    indivL, indivLnom = [], []
    for s in stratL :
        indivL += [s.strat]*s.individuals
        indivLnom += [s.stratname] * s.individuals
    return indivL, indivLnom



def attribution_gain(Ntournoi,niter,stratL) : #distribue les gains en faisant jouer Ntournois aux individus
    indivL, indivLnom = indivlist(stratL)
    for k in range(Ntournoi) :
        Ltot = total(niter,indivL)
        somme_gain(Ltot, stratL, indivL)



def somme_gain(Ltot, stratL, indivL) : #pour donner les gains aux objets strategy sans faire trop de boucles
    SL = death(stratL)
    n = 0
    SL[n].gain += Ltot[0]
    for k in range(1, len(Ltot)) :
        if indivL[k] != indivL[k-1] :
            n+=1
        SL[n].gain += Ltot[k]



def death(L) :
    S = []
    for s in L :
        if s.individuals != 0 :
            S.append(s)
    return S



def repopulation(stratL) :
    indivtot = 0
    gaintot = 0
    for s in stratL :
        gaintot += s.gain
    for s in stratL :
        s.repop_1(gaintot)
        indivtot += s.individuals
    #r = Ntot - indivtot
    #d = death(stratL)
    #for k in range(r) :
     #   stratL[k].individuals +=1



def generation(N, Ngene, Ntournoi, niter, S, Snom) : #simule toutes les générations
    """
        Simulates the iteration of generations
    """
    stratL = stratlist(N,S,Snom)
    Lindiv = []
    for k in range(Ngene) :
        L = [ss.individuals for ss in stratL]
        Lindiv.append(L)
        print(L)
        attribution_gain(Ntournoi, niter, stratL)
        repopulation(stratL)
    graph(Ngene,Lindiv,stratL)






def graph(Ngene,Lindiv,stratL) : #trace toutes les courbes à la fin de la simulation
    X = np.linspace(1,Ngene,Ngene)
    
    for k in range(len(stratL)) :
        Y = [y[k] for y in Lindiv]
        stratL[k].trace = plt.plot(X,Y, label = stratL[k].stratname)
    plt.legend(loc = 'upper left')
    plt.xlabel('generations')
    plt.ylabel('populations')
    plt.show()
    
    
    
    
    
S2 = [gentille,mechante,hard_majo,mefiante,indecise,random,soft_majo,ca_strat,sondeur,periodic_cct]
S2nom = ['gentille','mechante','hard_majo','mefiante','indecise','random','soft_majo','ca_strat','sondeur','periodic_cct']

S3 = [gentille,mechante,mefiante,indecise,random,soft_majo,ca_strat,periodic_ttc]
S3nom = ['gentille','mechante','mefiante','indecise','random','soft_majo','ca_strat','periodic_ttc']


S4 = [tit_for_tat, gradual, indecise, sondeur, periodic_cct, soft_majo]
S4nom = ['tit_for_tat', 'gradual', 'indecise', 'sondeur', 'periodic_cct', 'soft_majo']



S = [gentille,mechante,tit_for_tat,mefiante,indecise,soft_majo,spiteful,sondeur,periodic_cct]
Snom = ['gentille','mechante','tit_for_tat','mefiante','indecise','soft_majo','spiteful','sondeur','periodic_cct']



#generation(20,60,1,100,S2,S2nom)

S3 = [gentille, mechante, tit_for_tat]
S3nom = ['g',' m', 't']
