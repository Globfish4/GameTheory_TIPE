import random as rd
import numpy as np
import matplotlib.pyplot as plt



""" MUTATION """

## les stratégies sont renomées player, une classe définira un individu.

""" FIN MUTATION """




""" CLASSES DES INDIVIDUS """






class joueur :
    
    
    players_created = 0
    
    def __init__(self, type_joueur, strat, stratname) :   #type_joueur définit si le joueur sera un player ou une fonction stratégie
        """
            #si type_joueur vaut 0, player, si type_joueur vaut 1, 
            #alors c'est un barycentre de fonctions stratégies
        """
        self.type_joueur = type_joueur
        
        if type_joueur == 0 :
    
            joueur.players_created += 1
            self.strategy = 0
            self.stratname = '#player_'+ str(joueur.players_created)
            self.gain = 0
            self.adversary = 0 #gain de l'adversaire
            self.memory = [[], []]
            self.param = [0,0,0] # [taux de gentillesse, taux de mechanceté, rancune]
            
        elif type_joueur == 1 :
            
            self.strategy = strat
            self.stratname = stratname
            self.gain = 0
            self.adversary = 0 #gain de l'adversaire
            self.memory = [[],[]] #il se verra toujours comme un J1
            self.param = [] #paramètre qui est défini et utilisé dans les fonctions stratégie
        
        elif type_joueur == 2 :
            pass
    
    
    
    def play(self) :
        
        if self.type_joueur == 0 :
            
            r = 0
            l = len(self.memory[0])
            if l == 0 :
                l = 1
            else :
                if self.memory[1][-1] == True :
                    r = 1
                else :
                    r = -1
            b = self.param[0] - (l-counter_true(self.memory[1])) * self.param[1] / l + r * self.param[2]
            if b > 0 :
                return True
            else :
                return False

        elif self.type_joueur == 1 :
            
            return self.strategy(self.memory, self.param)
    
    
    
    def reset(self) :
        
        if self.type_joueur == 0 :
            self.memory = [[], []]
        
        elif self.type_joueur == 1 :
            self.memory = [[], []]
            self.param = []
            self.adversary = 0
    
    
    
    
    def define_param_randomly(self) : #prend en paramètre une liste de player et définit leurs paramètres avec des random
        if self.type_joueur == 0 :
            self.param[0] = rd.random() * 7 
            self.param[1] = rd.random() * 6
            self.param[2] = rd.random() * 6





class fusion :
    
    """
        classe des individus formés d'un couple de stratégies
    """
    
    def vectors(S,Snom) :
        pass
                
    
    def __init__(self, ) :
        pass
    



""" FIN CLASSE DES INDIVIDUS """ 




""" STRATEGIES """



## chaque stratÃ©gie a la liste des gains et la liste des coups de tous les tours prÃ©cÃ©dents.
## mais toutes les stratÃ©gies ne s'en serviront pas forcÃ©ment.



def gentille(coups, param) : #all_c
    return True



def mechante(coups, param) : #all_t
    return False



def tit_for_tat(coups, param) :
    if len(coups[0]) == 0 :
           return True
    else :
        return coups[1][-1]



def mefiante(coups, param) : # joue pÃ©riodiquement tc en commencant par t
    if len(coups[0]) % 2 == 0 :
        return False
    else :
        return True



def indecise(coups, param) : # joue pÃ©riodiquement ct en commencant par c
    if len(coups[0]) % 2 == 0 :
        return True
    else :
        return False



def random(coups, param) : #joue alÃ©atoirement
    a = rd.randint(1,2)
    if a == 1 :
        return True
    else :
        return False



def soft_majo(coups, param) : #joue ce que l'autre a jouÃ© en majoritÃ©, et joue c au premier coup ou en cas d'Ã©galitÃ©
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



def spiteful(coups, param) : #joue c jusqu'Ã  ce que l'autre trahisse, puis trahit tout le temps
    if counter_true(coups[1]) != len(coups[0]) :
        return False
    else :
        return True



def sondeur(coups, param) : # aux 3 premiers coups il joue tcc, puis t tout le temps si l'adversaire a coopÃ©rÃ© aux tours 2 et 3, donnant donnant sinon
    l = len(coups[0])
    if l == 0 :
        return False
    if l == 1 or l == 2 :
        return True
    if coups[1][1] and coups[1][2] :
        return False
    else :
        return tit_for_tat(coups, param)



def periodic_cct(coups, param) : #joue cooperer cooperer trahir pÃ©riodiquement
    l = len(coups[0])%3
    if l == 0 or l == 1:
        return True
    else :
        return False



def periodic_ttc(coups, param) : #joue trahir trahir coopÃ©rer pÃ©riodiquement
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



def fake_pavlov(coups, param) : #coopÃ¨re au premier coup puis coopÃ¨re seulement si les deux stratÃ©gies ont jouÃ© la mÃªme chose
    if len(coups[0]) == 0 :
        return True
    elif coups[-1] == [True,True] or coups[-1] == [False,False] :
        return True
    else :
        return False



def pavlov(coups, param) :
    l = len(coups[0])
    if l == 0 :
        return True
    last_played = coups[0][-1]
    last_earned = dilemme([last_played, coups[1][-1]])[0]
    if last_earned >= 3 :
        return last_played #s'il a gagné plus que 3, il rejoue pareil qu'au tour précédent
    else :
        return (last_played+1)%2 #s'il a gagné moins que 3, il joue l'autre coup : le XOR de son coup +1







def gradual(coups, param) :
    """
        param[0] est une liste des coups qu'il a prévu de renvoyer, 
        il renvoie la donnÃ©e qui est en premier dans la liste.
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




def suspicious_tft(coups, param) :
    l = len(coups[0])
    if l == 0 :
        return False
    else :
        return coups[1][-1]



def ca_strat(coups, param) : #coopère jusqu'à  ce que l'autre trahisse n fois, n augmente de 50 % à  chaque fois que l'autre coopère
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



def so_strat(coups, param) : #trahit 50 fois, puis coopère une fois, si l'autre coopère, elle coopère tout le temps, sinon elle trahit tout le temps
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
        param.extend([0,0,0,0]) #resp nombre de C après (C,C), (T,T), (T,C), (C,T)
        return True
    else :
        def stats(coups, param) :
            
            pass
#strat qui lit les deux derniers coups qu'elle a joué, elle regarde ce que son adversaire 
# a joué en réaction à ces deux coups, fait des stats de ces données et joue en prévoyant le coup
#suivant de son adversaire. elle essaie de jouer ce que son adversaire va jouer
#clem_strat






def counter_true(coups) : #compte le nombre de cooperations de l'adversaire
    c = 0
    for k in coups :
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


    


""" FIN STRATEGIES """




""" DILEMME ITERE DU PRISONNIER """



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
    


def tournoi(n, players_list) : #fait s'affronter une liste d'individus la fonction prend une liste d'individus en paramètre ainsi que le nombre de parties par match
    m = len(players_list)
    for k in range(m) : #on fixe un joueur
        for l in range(k+1, m) : #on le fait affronter tous les joueurs qui sont après lui dans la liste
            match(n, players_list[k], players_list[l])
    


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



def classement(Ltot, Players) : #renvoie la liste des noms des stratégies triée dans l'orde du plus petit gain au plus grand
    """
        Shows a ranking of strategies at the end of the tournament
    """
    ranking = Hoare_class(Players) #utilise la fonction de tri pour ordonner les stratégies
    rank = [p.stratname for p in ranking] #récupère de ranking uniquement les noms des stratégies dans l'ordre
    return rank



def Hoare_class(L) : #L est une liste d'objets d'une classe contenant un attribu gain
    l = len(L)
    if l == 0 or l == 1 :
        return L
    else :
        pivot = L[-1]
        xhaut = [x for x in L[:-1] if x.gain >= pivot.gain]
        xbas = [x for x in L if x.gain < pivot.gain]
        return Hoare_class(xhaut) + [pivot] + Hoare_class(xbas)



def generate_strategy(S,Snom) :
    """
        crée une liste d'individus de la classe strategy
    """
    players_list = []
    for s in range(len(S)) :
        players_list.append(joueur(1, S[s], Snom[s]))
    return players_list



def generate_player(n) : #n = nombre d'individus que je veux créer dans cette classe
    """
        crée une liste d'individus de la classe player
    """
    players_list = []
    for k in range(n) :
        players_list.append(joueur(0, 0, 0))
        players_list[k].define_param_randomly()
    return players_list
    


def generate_individuals(S,Snom, player_number, fusion_number) :
    """
        crée une liste d'individus de toutes classes condondues
    """
    individuals_list = []
    for i in range(len(S)) :
        individuals_list.append(joueur(1, S[i], Snom[i]))
    for i in range(player_number) :
        individuals_list.append(joueur(0, 0,0))    #########
    for i in range(fusion_number) :
        individuals_list.append(fusion())
    return individuals_list



def total(n, players_list) : #joue un tournoi en affichant l'histogramme et le classement
    tournoi(n,players_list) #joue le tournoi une fois
    Ltot = [] #récupère une liste des gains dans le même ordre que players_list
    for p in players_list :
        Ltot.append(p.gain)
    print(classement(Ltot, players_list)) #puis il affiche le classement et l'histogramme du tournoi
    histogramme(Ltot, players_list)


""" FIN DILEMME ITERE DU PRISONNIER """







""" EVOLUTION """




class team :
    """
        classe qui permet de gérer les équipes d'individus
    """
    
    def __init__(self, strat, joueur, stratname, Nindiv, param) :
        self.strategy = strat #utile si le type de l'équipe est strategy
        self.type_joueur = joueur #c'est le type de joueur (ie strategy ou player (ie 0 ou 1))
        self.stratname = stratname #nom du joueur
        self.individuals = Nindiv #nombre d'individus dans le groupe
        self.gain = 0 #gain total de l'équipe, cumulé après une génération et qui permet de déterminer le nouveau self.individuals
        self.indiv_list = [] #liste d'individus qui seront des objets de classe type joueur différents (mais avec le même nom, strategie/paramètre)
        self.trace = 0 #pour le graph à la fin
        self.parametre = param



    def modulate_indiv_list(self) : #avant l'utilisation de cette méthode, il faut que le nouveau nombre d'individus ait été défini pour chaque objet
        """
            méthode qui va modifier la liste des individus d'une même équipe, elle va 
            tuer des individus ou faire naitre des individus, pour limiter la créatiopn d'objets
        """
        
        old_Nindiv = len(self.indiv_list)
        if old_Nindiv > self.individuals : #si il doit perdre des individus, 
            for k in range(self.individuals, old_Nindiv) : #on les fait pop en partant de la fin
                self.indiv_list.pop()
        if old_Nindiv < self.individuals : #s'il doit gagner des individus, 
            for k in range(old_Nindiv, self.individuals) : #on les fait naitre avec type(self.indiv_list[0]())
                self.indiv_list.append(joueur(self.type_joueur, self.strategy, self.stratname))
                self.indiv_list[-1].param = self.parametre
        #si le nombre d'individus doit rester constant, il ne fait rien



    def repop(self, gaintot) : #les repop_k mettent à jour l'attribut individuals et remettent gain = 0
        self.individuals = int(self.gain * Ntot / gaintot)
        self.gain = 0





## on nomme 'personnalité' une même stratégie issue d'une même classe avec plus ou moins les mêmes paramètres

def generate_personalities(S,Snom, player_number, fusion_number) :
    """
        crée une liste d'individus de toutes classes condondues
    """
    personality_list = []
    for i in range(len(S)) :
        personality_list.append(joueur(1 ,S[i], Snom[i]))
    for i in range(player_number) :
        personality_list.append(joueur(0, 0,0))
        personality_list[-1].define_param_randomly()
    for i in range(fusion_number) :
        personality_list.append(fusion())
    return personality_list #liste des "joueurs" qui vont définir les caractéristiques de l'équipe



def creation_team(N, personality_list) : #N est le nombre d'individus par stratégie, fixe au début de la simulation
    teamL = [] #fonction qui fabrique une liste de teams à partir d'une liste de personnalités
    for k in personality_list :
        teamL.append(team(k.strategy, k.type_joueur, k.stratname, N, k.param))
    global Ntot #on déclare le nombre total et constant des individus de la simulation
    Ntot = len(personality_list) * N
    return teamL #liste des équipes




def filling_team(teamL, personality_list) : #il y a un bug : les classes ne prennent pas exactement les mêmes paramètres en indice
    for k in range(len(teamL)) : #pour chaque équipe, 
        teamL[k].modulate_indiv_list()
        




def create_indivlist(teamL) :
    """
        elle fabrique une liste de tous les individus de la génération, 
        simplement en faisant une concaténation
    """
    population = []
    for k in teamL :
        population += k.indiv_list
    return population
    
#à ce stade on a donc une grande liste d'individus, une population composée d'objets 
#strategy, player, ou encore fusion.




def define_new_Nindiv(teamL, gaintot) :
    for g in teamL :
        g.repop(gaintot) #redefinit indiv_list
        g.modulate_indiv_list() #modifie sa liste selon la méthode de la classe team
        for h in g.indiv_list :
            h.gain = 0 #remet à 0 les gains de tous les joueurs (même les nouveaux)




def generation(niter, teamL) :
    indivL = create_indivlist(teamL)
    tournoi(niter, indivL)
    gaintot = count_gain(teamL)
    define_new_Nindiv(teamL, gaintot)
#crée la liste de tous les individus, leur fait jouer un tournoi, somme tous les gains et les donne à 
#teamL.gain, et enfin définit le nouveau nombre d'équipiers, sans modifier la liste de l'équipe.
#il remet aussi à 0 le gain de chaque équipe


def count_gain(teamL) :
    l = len(teamL) #nombre de 'personnalités'
    gaintot = 0 #gain total sur une génération
    for e in range(l) :
        teamL[e].gain = sum([teamL[e].indiv_list[k].gain for k in range(len(teamL[e].indiv_list))]) #somme des gains de chaque membre d'équipe
        gaintot += teamL[e].gain
    return gaintot




def Evolution(niter, Nindiv, Ngene, S, Snom, player_number, fusion_number) :
    players = generate_personalities(S,Snom, player_number, fusion_number) #qui participera à la simulation
    teamL = creation_team(Nindiv, players) #chaque participant on lui attribue une classe d'inscription
    filling_team(teamL, players) #on remplit son équipe
    demography = [] #liste qui va retenir les listes des individus de chaque team, au fil des générations
    for k in range(Ngene) :
        demography.append([k.individuals for k in teamL])
        generation(niter, teamL)
        print([k.individuals for k in teamL])
    graph(Ngene, demography, teamL)





def graph(Ngene,demography,teamL) : #trace toutes les courbes à la fin de la simulation
    X = np.linspace(1,Ngene,Ngene)
    
    for k in range(len(teamL)) :
        Y = [y[k] for y in demography]
        teamL[k].trace = plt.plot(X,Y, label = teamL[k].stratname)
    plt.legend(loc = 'upper left')
    plt.xlabel('generations')
    plt.ylabel('populations')
    plt.show()




""" FIN EVOLUTION """





""" GENETIQUE """

#il s'agit de créer des players, de les faire s'affronter dans un tournoi, ne garder que les meilleurs d'entre eux et 
#de les faire fusionner selon un barycentre de paramètres aléatoire.
#on en créée 100 avec des paramètres de bases permettant d'avoir les mêmes caractéristiques que les fonctions stratégie basique
#(ie gentille, mechante, tit_for_tat, spiteful etc..) et puis les meilleurs voient leur paramètre fusionné avec un barycentre
#compris entre -0.5 et 1.5 (pour permettre les mutations)

#ensuite, on fera s'affronter les évolués (au bout de plusieurs générations) contre des players random, et contre des fonctions stratégie.



def imitation() : #a partir des paramètres, fabrique des joueurs de type 0 tels qu'ils jouent comme gentille, mechante, tit_for_tat, spiteful, periodic etc...
    imitateurs = []
    imitateurs.append(joueur(0,0,0))
    imitateurs[-1].param = [10,0,0]
    imitateurs[-1].stratname = 'gentille_copy'
    
    imitateurs.append(joueur(0,0,0))
    imitateurs[-1].param = [-10,0,0]
    imitateurs[-1].stratname = 'mechante_copy'
    
    imitateurs.append(joueur(0,0,0))
    imitateurs[-1].param = [1,20,0]
    imitateurs[-1].stratname = 'spiteful_copy'
    
    imitateurs.append(joueur(0,0,0))
    imitateurs[-1].param = [1,0,20]
    imitateurs[-1].stratname = 'tit_for_tat_copy'
    
    return imitateurs




def pop(n_player) :
    pop = imitation()
    poprandom = generate_player(n_player-len(pop))
    return poprandom + pop



def fusionne(heros) : #fusionne va donner une fusion des héros, et peut être aussi laisser les anciens héros pour voir s'ils survivent
    couples = []
    for k in range(int(len(heros)/2)) :
        couples.append([heros[k], heros[-1-k]])
    for k in range(len(couples)) :
        heros.append(joueur(0,0,0))
        barycenter(heros[-1].param, couples[k][0].param, couples[k][1].param)
        
        



def barycenter(paramachanger, param1, param2) :
    t = rd.random()*2 - 0.5
    t = rd.random() #pour essayer
    for k in range(len(paramachanger)) :
        paramachanger[k] = t*param1[k] + (1-t)*param2[k]




def choix_heros(G, Nheros) : #G liste classée par gain des joueurs
    k = 0
    n = 0 #nombre de héros sélectionnés
    heroes = []
    while n < Nheros :
        if G[k].type_joueur == 0 :
            heroes.append(G[k])
            n+=1
        k+=1
    return heroes
    #faire attention à ce qu'il y ait assez de joueurs de type 0



def mutation(Nevol, Npop, Nheros) :
    """
        fonction qui va orchestrer les tournois et les évolutions des joueurs
    """
    
    popu = pop(Npop) #crée la population de random type0
    for n in range(Nevol) : #pour le nombre d'évolutions demandées
        tournoi(100, popu) #il joue le tournoi avec ma population, 
        classement = Hoare_class(popu) #il les classe par gain
        heroes = choix_heros(classement, Nheros) #récupère les héros qui sont forcément type0
        parameter(popu) #affiche les graphes des gains et des paramètres de chaque individu
        plt.show()
        for k in range(Nheros) : #pour chaque héros,
            heroes[k].stratname = '#heroe_'+str(k) #il renomme le joueur et remet ses gains à 0
            heroes[k].gain = 0
        fusionne(heroes) #ensuite il rend une liste contenant les héros et leurs 'enfants'
        popu = heroes #+ pop(Npop - Nheros) #il redéfinit la population puis refait le même procédé
        
    return heroes #pour récupérer leurs paramètres


""" FIN GENETIQUE """






"""ETUDE DES PARAMETRES"""


def parameter(G) :
    
    Ltot = []
    for p in G :
        Ltot.append(p.gain)
        
    fig,axs = plt.subplots(2,2)
    
    
    s = len(G)
    x = [k for k in range(s)]
    width = 0.3
    axs[0][0].bar(x, Ltot, width, color='blue' )
    
    
    
    
    
    Y = [k.gain for k in G]
    
    X1 = [k.param[0] for k in G]
    #axs[0][1].title("Param 1 = taux de gentillesse")
    
    X2 = [k.param[1] for k in G]
    #axs[1][0].title('Param 2 = rancune')
    
    X3 = [k.param[2] for k in G]
    #axs[1][1].title('Param 2 = réactivité')
   
    axs[0][1].scatter(X1,Y, color = 'red')
    axs[1][0].scatter(X2,Y, color = 'purple')
    axs[1][1].scatter(X3,Y, color = 'green')
    
    
    #plt.show()






""" EXECUTION """
    
S = [gentille, mechante, tit_for_tat, mefiante, indecise, spiteful, periodic_cct, soft_majo, gradual]
Snom = ['gentille','mechante','tit_for_tat','mefiante','indecise', 'spiteful', 'periodic_cct', 'soft_majo', 'gradual']
#Evolution(100, 20, 30, S,Snom, 0,0)



    
S = [gentille,mechante,tit_for_tat,mefiante,indecise]
Snom = ['gentille','mechante','tit_for_tat','mefiante','indecise']
#Evolution(100, 10, 20, S, Snom, 0,0)

S2 = [gradual, ca_strat, mechante]
S2nom = ['gradual', 'ca_strat', 'mechante']


#G = generate_strategy(S2,S2nom)
#total(5,G)

S2 = [gentille, mechante]
S2nom = ['gentille', 'mechante']
#Evolution(100, 20,20,S2,S2nom, 0,0)

""" FIN EXECUTION """





S = [tit_for_tat, gradual, pavlov, hard_majo, soft_majo, mechante, spiteful, suspicious_tft ,gentille]
Snom = ['tit_for_tat', 'gradual', 'pavlov', 'hard_majo', 'soft_majo', 'mechante', 'spiteful', 'suspicious_tft', 'gentille']
Evolution(100, 25, 30, S, Snom, 0,0)





