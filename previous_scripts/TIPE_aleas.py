"""
ce fichier permet de tester des petits résultats
trouvés dans le diapo de Delahaye.
il n'y a plus de joueurs définis sur des paramètres, plus que des fonctions stratégies
et la réalisation d'un tournoi est fait beaucoup plus rapidement, en supposant que 
deux mêmes stratégies vont faire le même nombre de points face à une autre stratégie

en gros c'est le même programme que tipe_dilemme mais en beaucoup plus performant...
cependant il ne faut pas utiliser de stratégies probabilistes telles que random
"""



import random as rd
import numpy as np
import matplotlib.pyplot as plt




""" CLASSES DES INDIVIDUS """






class joueur :
    
    
    players_created = 0
    
    def __init__(self, strat, stratname, Nindiv) :   #type_joueur définit si le joueur sera un player ou une fonction stratégie
        """
            #si type_joueur vaut 0, player, si type_joueur vaut 1, 
            #alors c'est un barycentre de fonctions stratégies
        """
        self.strategy = strat
        self.stratname = stratname
        self.gain = 0
        self.gain_list = [0] * lenS # gain_liste[k] est son gain total contre la stratégie no k
        self.gain_final = 0
        self.adversary = 0 #gain de l'adversaire
        self.memory = [[],[]] #il se verra toujours comme un J1
        self.param = [] #paramètre qui est défini et utilisé dans les fonctions stratégie
        self.individuals = Nindiv #nombre d'individus dans le groupe
        self.trace = 0 #pour le graph à la fin





    def play(self) :
        return self.strategy(self.memory, self.param)
    
    
    
    def reset(self) :
        self.memory = [[], []]
        self.param = []
        self.adversary = 0


    def repop(self, gaintot) :
        self.individuals = int(self.gain_final * Ntot / gaintot)









""" DEBUT STRATEGIES """


def gentille(coups, param) : #all_c
    return True



def mechante(coups, param) : #all_t
    return False



def tit_for_tat(coups, param) :
    if len(coups[0]) == 0 :
           return True
    else :
        return coups[1][-1]



def mefiante(coups, param) : # joue périodiquement tc en commencant par t
    if len(coups[0]) % 2 == 0 :
        return False
    else :
        return True



def indecise(coups, param) : # joue périodiquement ct en commencant par c
    if len(coups[0]) % 2 == 0 :
        return True
    else :
        return False



def random(coups, param) : #joue aléatoirement
    a = rd.randint(1,2)
    if a == 1 :
        return True
    else :
        return False



def soft_majo(coups, param) : #joue ce que l'autre a joué en majorité, et joue c au premier coup ou en cas d'égalité
    def scount(coups) :
        c = 0
        for k in coups[1] :
            if k :
                c += 1
        if c >= (len(coups[1]))/2 :
            return True
        else :
            return False

    if len(coups[0]) == 0 or scount(coups) :
        return True
    elif not scount(coups) :
        return False



def spiteful(coups, param) : #joue c jusqu'Ãƒ  ce que l'autre trahisse, puis trahit tout le temps
    if counter_true(coups[1]) != len(coups[0]) :
        return False
    else :
        return True



def sondeur(coups, param) : # aux 3 premiers coups il joue tcc, puis t tout le temps si l'adversaire a coopÃƒÂ©rÃƒÂ© aux tours 2 et 3, donnant donnant sinon
    l = len(coups[0])
    if l == 0 :
        return False
    if l == 1 or l == 2 :
        return True
    if coups[1][1] and coups[1][2] :
        return False
    else :
        return tit_for_tat(coups, param)



def periodic_cct(coups, param) : #joue cooperer cooperer trahir pÃƒÂ©riodiquement
    l = len(coups[0])%3
    if l == 0 or l == 1:
        return True
    else :
        return False



def periodic_ttc(coups, param) : #joue trahir trahir coopÃƒÂ©rer pÃƒÂ©riodiquement
    l = len(coups[0])%3
    if l == 0 or l == 1:
        return False
    else :
        return True



def hard_majo(coups, param) : #trahit au premier coup ou si l'adversaire a majoritairement trahit. coopere sinon.
    def hcount(coups) :
        c = 0
        for k in coups[1] :
            if k :
                c += 1
        if c > (len(coups[1]))/2 :
            return True
        else :
            return False

    if len(coups[0]) == 0 or not hcount(coups) :
        return False
    elif hcount(coups) :
        return True



def pavlov(coups, param) : #coopÃƒÂ¨re au premier coup puis coopÃƒÂ¨re seulement si les deux stratÃƒÂ©gies ont jouÃƒÂ© la mÃƒÂªme chose
    if len(coups[0]) == 0 :
        return True
    elif coups[-1] == [True,True] or coups[-1] == [False,False] :
        return True
    else :
        return False




def gradual(coups, param) :
    """
        param[0] est une liste des coups qu'il a prévu de renvoyer, 
        il renvoie la donnée qui est en premier dans la liste.
    """
    l = len(coups[0])
    if l == 0 :
        param.extend([[],0])
        return True
    elif len(param[0]) != 0 :
        ans = param[0][0]
        del param[0][0]
        return ans
    elif len(param[0]) == 0 :
        c = l - counter_true(coups[1])
        if param[1] < c :
            param[1] = c
            param[0] = [False]*(c-1) + [True]*2
            return False
        elif param[1] == c :
            return True




def ca_strat(coups, param) : #coopÃ¨re jusqu'Ã   ce que l'autre trahisse n fois, n augmente de 50 % Ã   chaque fois que l'autre coopÃ¨re
    l = len(coups[1])
    if l == 0 :
        param.append(1) #threshold
        param.append(False) #reached_threshold
        param.append(0.5) #percent
        return True
    else :
        if param[1] :
            return False
        f = l - counter_true(coups[1]) # = counter_false
        if f >= param[0] :
            param[1] = True
            return False
    if coups[1][-1] :
        param[0] += param[0] * param[2]
    return True



def so_strat(coups, param) : #trahit 50 fois, puis coopÃ¨re une fois, si l'autre coopÃ¨re, elle coopÃ¨re tout le temps, sinon elle trahit tout le temps
    l = len(coups[0])
    if l < 50 :
        return False
    if l == 50 :
        return True
    return coups[1][50]



def cam_strat(coups, param) :
    l = len(coups[0])
    if l == 0 :
        param.extend([0,0])
        return True
    d = dilemme([coups[0][l-1], coups[1][l-1]])
    param[0] += d[0]
    param[1] += d[1]
    if l == 0 or l == 3 or l == 4 :
        return True
    elif l == 1 or l == 2 :
        return False 
    elif l < 40 :
        if not coups[1][0] :
            return False



def clem_strat(coups, param) :
    l = len(coups[0])
    if l == 0 or l == 1 :
        param.extend([0,0,0,0]) #resp nombre de C aprÃ¨s (C,C), (T,T), (T,C), (C,T)
        return True
    else :
        def stats(coups, param) :
            
            pass
#strat qui lit les deux derniers coups qu'elle a jouÃ©, elle regarde ce que son adversaire 
# a jouÃ© en rÃ©action Ã  ces deux coups, fait des stats de ces donnÃ©es et joue en prÃ©voyant le coup
#suivant de son adversaire. elle essaie de jouer ce que son adversaire va jouer
#clem_strat





def counter_true(coups) : #compte le nombre de cooperations de l'adversaire
    c = 0
    for k in coups :
        if k :
            c += 1
    return c



def counter_while_false(coups) : #compte le nombre de false de l'adversaire, tant que ses derniers coups sont des false
    k = len(coups[1]) #(au premier true, le compteur s'arrête)
    c = 0
    while not coups[0][k-1] :
        if k-1 >= 0 :
            c += 1
            k -= 1
    return c

    


""" FIN STRATEGIES """







""" DILEMME ITERE DU PRISONNIER """



def dilemme(coopere): #dÃ©finira le gain de chacun des deux joueurs. True=coopérer, False=trahir
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



def partie(player1, player2): #fait s'affronter deux stratégies une seule fois, en fonction du tour précédent.
    J1,J2 = player1.play(), player2.play() #on acquiert le coup que va jouer chaque joueur
    gain = dilemme([J1,J2]) #calcule le gain que leur coup implique
    player1.gain += gain[0] #distribue le gain à chacun
    player2.gain += gain[1]
    player1.adversary += gain[1] #distribue aussi le gain de l'autre
    player2.adversary += gain[0] #le gain est cumulé, il sera remis à zéro à la fin du tournoi
    player1.memory[0].append(J1) #la mémoire est aussi mise à jour
    player1.memory[1].append(J2)
    player2.memory[0].append(J2)  #l'inversion des listes se fait ici
    player2.memory[1].append(J1)



def match(n,player1,player2) : #n nombre de parties par affrontement. il retourne la liste des gains cumulés
    for k in range(n) : #n itérations du dilemme par match
        partie(player1,player2)
    player1.reset() #à la fin du match, on reset les attributs des joueurs
    player2.reset()
    


def tournoi_fast(n, teamL) : #ici y a une erreur à corriger, quand il s'affronte lui même il ne faut pas multiplier son gain par le nombre d'individus.
    for k in range(lenS) :
        for l in range(k, lenS) :
            if k == l :
                a = joueur(teamL[l].strategy, teamL[l].stratname, 1)
                match(n, teamL[k], a)
                
                teamL[k].gain_list[l] = teamL[k].gain * (teamL[l].individuals -1)
            if k != l :
                match(n, teamL[k], teamL[l])
                
                teamL[k].gain_list[l] = teamL[k].gain * teamL[l].individuals
                teamL[l].gain_list[k] = teamL[l].gain * teamL[k].individuals
                
            #divisé par deux car dans partie, le joueur incrémente deux fois son gain (au final son gain est deux fois ce qu'il devrait être)
            teamL[k].gain = 0
            teamL[l].gain = 0
        teamL[k].gain_final = sum(teamL[k].gain_list) * teamL[k].individuals       
#tournoi fast est comme tournoi, sauf que la liste qu'elle prend est compactée par équipes, et elle multiplie 
#les gains par le nombre d'individus





def histogramme(Ltot, Players) : #prend en paramètre une liste d'objets de classes
    """
        Shows a histogram of earnings at the end of the tournament
    """
    s = len(Players)
    x = [k for k in range(s)]
    width = 0.3
    BarName = [p.stratname for p in Players]
    plt.bar(x, Ltot, width, color='blue' )
    plt.xlim(-1,s)
    plt.ylim(min(Ltot)-100,max(Ltot)+100)
    plt.ylabel('Total des Points')
    plt.title('Résultats du tournoi')
    plt.xticks(x, BarName, rotation=26)
    plt.show()




def total(n, players_list) : #joue un tournoi en affichant l'histogramme et le classement
    tournoi_fast(n,players_list) #joue le tournoi une fois
    Ltot = [] #récupère une liste des gains dans le même ordre que players_list
    for p in players_list :
        Ltot.append(p.gain_final)
    histogramme(Ltot, players_list)



""" FIN DILEMME ITERE DU PRISONNIER """








""" EVOLUTION """




def generate_personalities(S,Snom, Nindiv) :
    """
        crée une liste des joueurs
    """
    global lenS
    lenS = len(S)
    teamL = []
    for i in range(lenS) :
        teamL.append(joueur(S[i], Snom[i], Nindiv[i]))
    global Ntot
    Ntot = sum(Nindiv)
    return teamL #liste des équipes, compactée en un individu qui jouera pour tous les autres




def define_new_Nindiv(teamL, gaintot) :
    for g in teamL :
        g.repop(gaintot) #redefinit individuals




def count_gain(teamL) : #à mieux écrire pour qu'elle s'"occupe de compter tous les gains
    gaintot = sum([k.gain_final for k in teamL]) #gain total sur une génération
    return gaintot





def generation(niter, teamL) :
    tournoi_fast(niter, teamL)
    gaintot = count_gain(teamL)
    define_new_Nindiv(teamL, gaintot)




def Evolution(niter, Nindiv, Ngene, S, Snom ,alea) : #alea est un booléen, l'utilisateur choisit s'il veut rajouter une aléa ou non
    teamL = generate_personalities(S,Snom, Nindiv) #initialisation de la liste des joueurs
    demography = [] #liste qui va retenir les listes des individus de chaque team, au fil des générations
    for k in range(Ngene) :
        demography.append([k.individuals for k in teamL])
        generation(niter, teamL)
        if alea :
            aleas([k for k in teamL if k.individuals > 0])
        print(demography[-1])
    graph(Ngene, demography, teamL)




def graph(Ngene,demography,teamL) : #trace toutes les courbes Ã  la fin de la simulation
    X = np.linspace(1,Ngene,Ngene)
    
    for k in range(lenS) :
        Y = [y[k] for y in demography]
        teamL[k].trace = plt.plot(X,Y, label = teamL[k].stratname) #marker = '0', linewidth = 0
    plt.legend(loc = 'upper left')
    plt.xlabel('generations')
    plt.ylabel('populations')
    plt.show()






def aleas(teamLnodeath) :
    for k in range(50) :
        a = rd.randint(0,len(teamLnodeath)-1)
        teamLnodeath[a].individuals -= 1
    for k in teamLnodeath :
        if k.individuals < 0 :
            k.individuals = 0
        




""" FIN EVOLUTION """





""" EXECUTION """




S = [gentille, mechante, tit_for_tat, mefiante, indecise, ca_strat, periodic_cct, soft_majo, so_strat, periodic_cct, hard_majo, gradual]
Snom = ['gentille','mechante','tit_for_tat','mefiante','indecise', 'ca_strat', 'periodic_cct', 'soft_majo', 'so_strat', 'periodic_cct', 'hard_majo','gradual']
#Evolution(100, [200]*14, 100, S,Snom, False)
#Evolution(100, [200]*12, 100, S, Snom, True)



#Evolution(10, [931, 69], 50, [mechante, tit_for_tat], ['mechante', 'tft'], False)
#invasion des méchantes par les tft


S3 = [periodic_cct, periodic_ttc, soft_majo]
S3nom = ['periodic_cct', 'periodic_ttc', 'soft_majo']
Evolution(1000, [45, 100, 10], 500, S3 ,S3nom, False) #une sinusoide amortie
#Evolution(1000, [300,200,100], 300, S3, S3nom, False) #une sinusoide non amortie














