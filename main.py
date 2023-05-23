import random as rd
import numpy as np
import matplotlib.pyplot as plt



""" CLASSES DES INDIVIDUS """


class strategies :
    
    
    def __init__(self, strat, stratname, Nindiv, lenS) :

        self.strategy = strat
        self.stratname = stratname
        
        self.gain = 0
        self.gain_list = [0] * lenS # gain_liste[k] est son gain total contre la stratégie no k
        self.gain_final = 0
        
        self.memory = [[],[]] #il se verra toujours comme un J1
        self.param = [] #paramètre qui est défini et utilisé dans les fonctions stratégie
        self.individuals = Nindiv #nombre d'individus dans le groupe



    def play(self) :
        return self.strategy(self.memory, self.param) #appelle une des fonctions stratégies définies plus loin
    
    
    def reset(self) :
        self.memory = [[], []] #après chaque match, dans match(), remet à 0 la mémoire et le paramètre
        self.param = []


    def repop(self, gaintot) : #pour redéfinir la population (self.Nindiv) du joueur
        self.individuals = int(self.gain_final * Ntot / gaintot)




class ZD :
    
    last_game = [[True, True], [True, False], [False, True], [False, False]] #initialisation des 4 issues possibles
    players_created = 0 #pour nommer les stratégies sur leur numéro de création (de manière unique)
    
    def __init__(self, parameters, stratname, Nindiv, lenS) :
        ZD.players_created +=1
        
        self.strategy = parameters
        self.stratname = '#zd_'+str(ZD.players_created)
        
        self.gain = 0
        self.gain_list = [0]*lenS
        self.gain_final = 0
        
        self.memory = [[],[]]
        self.individuals = Nindiv
        
        
    def recognize(self, coopere) : #coopere est de la forme [dernier coup de zd, dernier coup de l'autre]
        for k in range(4) : # 4 = len(ZD.last_game)
            if ZD.last_game[k] == coopere :
                return self.strategy[k] #renvoie la probabilité de coopérer en fonction du dernier tour

        
    def play(self) :
        if len(self.memory[0]) == 0 : #si c'est le premier tour, joue la coopération
            return True
        last_play = [self.memory[0][0], self.memory[1][0]] #on sauvegarde le dernier tour joué par les adversaires
        self.memory = [[], []] #et on supprime le reste
        p = rd.random() #on tire au sort un coup qui va être joué
        pk = self.recognize(last_play) #on reconnait l'issue du dernier tour et on récupère la proba qui correspond
        if p > pk : #si p > pk, alors il trahit, sinon il coopère
            return False
        else :
            return True

    
    def reset(self) :
        self.memory = [[],[]]
 
    
    def repop(self, gaintot) :
        self.individuals = int(self.gain_final * Ntot / gaintot) 




class player :
    
    players_created = 0
    
    def __init__(self, vector, stratname, Nindiv, lenS) : #vector est un array numpy ((1,3))
        player.players_created +=1
        
        self.strategy = vector
        self.stratname = '#player_'+str(player.players_created)
        
        self.gain = 0
        self.gain_list = [0] * lenS # gain_liste[k] est son gain total contre la stratégie no k
        self.gain_final = 0
        
        self.memory = [[],[]] #il se verra toujours comme un J1
        self.individuals = Nindiv #nombre d'individus dans le groupe
        
        self.marker = 0 #dans l'algorithme génétique, sert à voir combien de boucles une stratégie passe
        
    
    
    def play(self) :
        l = len(self.memory[0])
        if l == 0 :
            b = self.strategy[0]
        else :
            if self.memory[1][-1] :
                r = 1
            else : 
                r = -1
            b = self.strategy[0] - (l-counter_true(self.memory[1])) * self.strategy[1] / l + r * self.strategy[2]
        if b > 0 :
            return True
        else :
            return False
    


    def reset(self) :
        self.memory = [[], []] #après chaque match, dans match(), remet à 0 la mémoire et le paramètre


    def repop(self, gaintot) : #pour redéfinir la population (self.Nindiv) du joueur
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



def spiteful(coups, param) : #joue c jusqu'à ce que l'autre trahisse, puis trahit tout le temps
    if counter_true(coups[1]) != len(coups[0]) :
        return False
    else :
        return True



def sondeur(coups, param) : # aux 3 premiers coups il joue tcc, puis t tout le temps si l'adversaire a coopéré aux tours 2 et 3, donnant donnant sinon
    l = len(coups[0])
    if l == 0 :
        return False
    if l == 1 or l == 2 :
        return True
    if coups[1][1] and coups[1][2] :
        return False
    else :
        return tit_for_tat(coups, param)



def periodic_cct(coups, param) : #joue cooperer cooperer trahir périodiquement
    l = len(coups[0])%3
    if l == 0 or l == 1:
        return True
    else :
        return False



def periodic_ttc(coups, param) : #joue trahir trahir coopérer périodiquement
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



def probe(coups, param) : #coopère au premier coup puis coopère seulement si les deux stratégies ont joué la mme chose
    if len(coups[0]) == 0 :
        return True
    elif coups[-1] == [True,True] or coups[-1] == [False,False] : #analyse les deux derniers coups
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



def suspicious_tft(coups, param) :
    l = len(coups[0])
    if l == 0 :
        return False
    else :
        return coups[1][-1]




def ca_strat(coups, param) : #coopère jusqu'à ce que l'autre trahisse n fois, n augmente de 50 % à chaque fois que l'autre coopère
    l = len(coups[1])
    if l == 0 :
        param.append(5) #threshold
        param.append(False) #reached_threshold
        param.append(0.1) #percent
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



def random_9(coups, param) :
    coup = rd.random()
    if coup <= 0.9 :
        return True
    else : 
        return False




def dog(coups, param) :
    l = len(coups[0])
    if l <= 2 :
        return False
    if coups[1][0] and not coups[1][1] :
        param.append(False)
    else :
        param.append(True)
    return param[0]





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
    player2.gain += gain[1] #le gain est cumulé, il sera remis à zéro à la fin du tournoi
    player1.memory[0].append(J1) #la mémoire est aussi mise à jour
    player1.memory[1].append(J2)
    player2.memory[0].append(J2) #l'inversion des listes se fait ici
    player2.memory[1].append(J1)



def match(n,player1,player2) : #n nombre de parties par affrontement.
    for k in range(n) : #n itérations du dilemme par match
        partie(player1,player2)
    player1.reset() #à la fin du match, on reset les attributs des joueurs
    player2.reset()
    


def tournoi_fast(n, teamL) :
    lenS = len(teamL)
    for k in range(lenS) : #chaque individu de la liste va affronter tous les autres (même lui)
        for l in range(k, lenS) :
            if k == l : #s'il s'affronte lui même
                a = type(teamL[k])(teamL[k].strategy, teamL[k].stratname, 1, 1) #on crée un joueur qui aura la même stratégie qui lui
                match(n, teamL[k], a) #et on les fait s'affronter
                
                teamL[k].gain_list[l] = teamL[k].gain * (teamL[l].individuals) ###########gain de lui même contre tous les autres membres de son équipe
            if k != l : #si il affronte une autre équipe
                match(n, teamL[k], teamL[l]) #on les fait s'affronter lors du match
                
                teamL[k].gain_list[l] = teamL[k].gain * teamL[l].individuals #on multiplie le gain de l'équipe k par le nombre d'individus de l'équipe l
                teamL[l].gain_list[k] = teamL[l].gain * teamL[k].individuals #vice versa
                
            teamL[k].gain = 0 #on remet ensuite leurs gains de match à 0
            teamL[l].gain = 0
        teamL[k].gain_final = sum(teamL[k].gain_list) * teamL[k].individuals #enfin, on additionne le gain total d'un individu de l'équipe, et on 
                                                    #le multiplie par le nombre d'individus de l'équipe




def trier_Hoare(L) : #trie la liste d'équipes en se basant sur leurs gains du tournoi précédent
#algorithme de tri sur le principe du quicksort
#Il range la liste dans l'ordre décroissant. les meilleures se retrouvent au début de la liste
    l = len(L)
    if l == 0 or l == 1 :
        return L
    else :
        pivot = L[-1]
        xhaut = [x for x in L[:-1] if x.gain_final >= pivot.gain_final]
        xbas = [x for x in L if x.gain_final < pivot.gain_final]
        return trier_Hoare(xbas) + [pivot] + trier_Hoare(xhaut)




def histogramme(Ltot, Players) : #prend en paramètre une liste d'objets de classes
    """
        histogramme des gains à la fin d'un tournoi
    """
    s = len(Players)
    x = [k for k in range(s)]
    width = 0.4
    BarName = [p.stratname for p in Players]
    plt.barh(x, Ltot, width, color='blue' )
    plt.ylim(-1,s)
    plt.xlim(min(Ltot)-100,max(Ltot)+100)
    plt.ylabel('Total des Points', size = 20)
    plt.title('Résultats du tournoi', size = 20)
    plt.yticks(x, BarName, size = 12)
    plt.show()




def total(n, players_list) : #joue un tournoi en affichant l'histogramme et le classement
    tournoi_fast(n,players_list) #joue le tournoi une fois
    P = trier_Hoare(players_list)
    Ltot = [p.gain_final for p in P] #récupère une liste des gains dans le même ordre que players_list
    histogramme(Ltot, P)



""" FIN DILEMME ITERE DU PRISONNIER """




""" EVOLUTION """




def generate_personalities(S,Snom, Nindiv, zd_parameters, p_parameters) : #zd et players paramaters sont des vecteurs de paramètres, contenus dans une liste
    """
        fonction pour créer la liste des équipes, chaque membre d'équipe ayant la même stratégie.
        cette fonction doit être utilisée aussi bien pour l'évolution que pour le tournoi
    """
    lenS = len(S) + len(zd_parameters) + len(p_parameters)
    teamL = []
    for i in range(len(S)) :
        teamL.append(strategies(S[i], Snom[i], Nindiv[i], lenS))
    for i in range(len(zd_parameters)) :
        teamL.append(ZD(zd_parameters[i], None, Nindiv[len(S) +i], lenS ))
    for i in range(len(p_parameters)) :
        teamL.append(player(p_parameters[i], None, Nindiv[len(S)+len(zd_parameters)+i], lenS))
    global Ntot
    Ntot = sum(Nindiv)
    print('teamL created')
    return teamL #liste des équipes, compactée en un individu qui jouera pour tous les autres
#zd_parameters contient des sous listes de 4 nombres définissant p1, p2, p3, p4
#n_players est le nombre de players qui vont être créés




def repopulation(teamL) :
    lenS = len(teamL)
    gaintot = sum([k.gain_final for k in teamL if k.individuals > 0]) #gain total sur une génération
    for g in teamL :
        if g.individuals > 0 :
            g.repop(gaintot) #redefinit individuals
            g.gain_list = [0]*lenS #on remet à 0 sa liste de gains, pour ne pas lui compter des points en plus dans la discrétisation



def generation(niter, teamL) :
    tournoi_fast(niter, [k for k in teamL if k.individuals != 0])
    repopulation(teamL)




def Evolution(niter, Nindiv, Ngene, S, Snom, zd_parameters, p_parameters) : #crée la liste d'équipes à l'intérieur
    teamL = generate_personalities(S,Snom, Nindiv, zd_parameters, p_parameters) #initialisation de la liste des joueurs
    demography = [] #liste qui va retenir les listes des individus de chaque team, au fil des générations
    for k in range(Ngene) :
        demography.append([k.individuals for k in teamL])
        generation(niter, teamL)
        print(demography[-1])
    graph(Ngene, demography, teamL)
    return teamL #je l'ai rajouté car j'en ai besoin pour la discrétisation des paramètres




def Evolution_2(teamL, niter, Ngene) : #autre version qui prend la liste en param
    demography = [] #liste qui va retenir les listes des individus de chaque team, au fil des générations
    for k in range(Ngene) :
        demography.append([k.individuals for k in teamL])
        generation(niter, teamL)
    #graph(Ngene, demography, teamL)
#cette fonction est la même que celle au dessus, mais je l'ai adaptée à l'algorithme génétique.




def graph(Ngene,demography,teamL) : #trace toutes les courbes à la fin de la simulation
    X = np.linspace(1,Ngene,Ngene)
    
    style = ['-']
    couleur = ['black','gray','blue','green','red','navy','aquamarine','lime','gold','chocolate','lightseagreen','purple','magenta','deeppink','orange','indigo', 'mediumslateblue', 'lightblue', 'olive', 'crimson', 'palegreen', 'teal']
    s,c = len(style)-1, len(couleur)-1
    
    for k in range(len(teamL)) :
        Y = [y[k] for y in demography]
        plt.plot(X,Y, label = teamL[k].stratname, color = couleur[rd.randint(0, c)], linestyle = style[rd.randint(0, s)])
    plt.legend(loc = 'upper right', )
    plt.xlabel('générations')
    plt.ylabel('populations')
    plt.show()



""" FIN EVOLUTION """




""" DEBUT EVOLUTION ET MUTATION DES PARAMÈTRES """



def vector_L(n_players) :
    #choisit n_players vecteurs au hasard dans le cube
    L = []
    for k in range(n_players) :
        L.append(np.array((2*rd.random()-1, 2*rd.random()-1, 2*rd.random()-1)))
    return L



def trier_gains(L) : #trie la liste d'équipes en se basant sur leurs gains du tournoi précédent
#algorithme de tri sur le principe du quicksort
#Il range la liste dans l'ordre décroissant. les meilleures se retrouvent au début de la liste
    l = len(L)
    if l == 0 or l == 1 :
        return L
    else :
        pivot = L[-1]
        xhaut = [x for x in L[:-1] if x.individuals >= pivot.individuals]
        xbas = [x for x in L if x.individuals < pivot.individuals]
        return trier_gains(xhaut) + [pivot] + trier_gains(xbas)



def premier_quart(teamL) : #les 25% meilleures, on leur augmente leur marqueur
    for k in teamL :
        k.marker += 1


def fusion(teamL, winners) : # fait une fusion des meilleures équipes
    l = len(teamL)
    fusions = [[rd.randint(0, l-1), rd.randint(0,l-1)] for k in range(l)] #une liste de couples de stratégies
    for k in range(l) :
        teamL[k].strategy = (winners[fusions[k][0]].strategy + winners[fusions[k][1]].strategy)/2 #on fait la moyenne arithmétique
        teamL[k].marker = 0 #toutes les autres, on leur remet leur marqueur à 0
        

def mutation(teamL, n) : #ne modifie qu'une seule coordonnée légèrement du paramètre
    for k in teamL :
        pk = rd.randint(0,2)
        k.strategy[pk] += rd.random()/(n+1)-1/(2*n+2)
        k.marker = 0


def naissance(teamL) : #on supprime les moins bonnes et on les remplace par des toutes nouvelles (mais on garde l'objet pour éviter de recréer une équipe)
    for k in teamL :
        for l in range(3) : #on sait qu'il y a 3 paramètres par équipe, c'est un vecteur 
            k.strategy[l] = rd.random()*2-1
        k.marker = 0



def redefinir(teamL, k) :
    lt = len(teamL)//4
    premier_quart(teamL[:lt])
    mutation(teamL[lt:2*lt], k) #on fusionne des couples créés sur le meilleur quart pour donner des nouvelles stratégies.
    fusion(teamL[2*lt:3*lt], teamL[:lt])
    naissance(teamL[3*lt:])




def genetique(Nindiv, n_players, niter, Ngene, Nevol) :
    """
    Nindiv est un entier, n_players le nombre d'équipes dans la liste, niter le nombre d'itérations du dilemme
    Ngene le nombre de generations du jeu d'évolution, Nevol le nombre de fois que l'algo genetique va tourner

    la liste de stratégie subit plusieures modifications génétiques :
        1/4 de la population suivante est constituée des meilleures de la population précédente
        1/4 sont des fusions 
        1/4 sont des mutations (des paramètres fixes et un autre modifié randomly)
        1/4 sont des nouvelles stratégies
    """
    vectorL = vector_L(n_players) #on initialise une liste de paramètres random
    teamL = generate_personalities([],[],[Nindiv]*n_players, [], vectorL) #crée une liste d'équipes
    for n in range(Nevol) : #on va répéter le tournoi n fois
        print(str(n*100/Nevol)+'%')
        print([k.marker for k in teamL])
        for k in teamL : #on met à 0 leurs populations a la fin de chaque tour
            k.individuals = Nindiv
        Evolution_2(teamL, niter, Ngene)
        teamL = trier_gains(teamL) #on fait un rang des équipes en fonction de leur population
        print([k.individuals for k in teamL])
        redefinir(teamL, n) #fonction qui réalise les 4 types d'évolution génétique
        
    print('100%')  
    
    #test(teamL)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.set_xlabel('p1')
    ax.set_ylabel('p2')
    ax.set_zlabel('p3')
    #plt.scatter([k.strategy[1] for k in teamL if k.individuals !=0], [k.strategy[2] for k in teamL if k.individuals !=0], s=30, c=[k.individuals for k in teamL if k.individuals !=0], cmap = 'Spectral')
    im = ax.scatter([k.strategy[0] for k in teamL], [k.strategy[1] for k in teamL], [k.strategy[2] for k in teamL], s=25, c=[k.individuals for k in teamL], cmap = 'magma_r')

    fig.colorbar(im, ax=ax)
    plt.show()
    
    return teamL



def test(teamL) :
    S = [tit_for_tat, gradual, pavlov, hard_majo, soft_majo, mechante, spiteful, suspicious_tft ,gentille, ca_strat]
    Snom = ['tit_for_tat', 'gradual', 'pavlov', 'hard_majo', 'soft_majo', 'mechante', 'spiteful', 'suspicious_tft', 'gentille', 'carlos']
    stratL = generate_personalities(S, Snom, [100]*(10 + len(teamL)), [], [k.strategy for k in teamL])
    total(100,stratL)


""" FIN EVOLUTION ET MUTATION DES PARAMÈTRES """




""" DEBUT DISCRETISATION DES PARAMETRES """



def select(precision, Nteam) :
    val = np.linspace(-1, 1, precision+1) #on découpe [0,1] en précision intervales réguliers
    l = len(val)
    L_param = []
    for k1 in range(l) : #on regarde chaque vecteur de la grille
        for k2 in range(l) :
            for k3 in range(l) :
                bol = True
                vect = np.array((val[k1], val[k2], val[k3]))
                for k in L_param : #on le garde s'il n'y a pas déjà de vecteur proportionnel
                    if (k[0]*vect[1]-vect[0]*k[1] == 0) and (k[0]*vect[2]-vect[0]*k[2] == 0) :
                        bol = False
                        break
                if bol == True :#and abs(vect[0]) + abs(vect[1]) >= abs(vect[2]) : #on exclue aussi les tit_for_tat
                    #if abs(vect[0]) <= abs(vect[1]) + abs(vect[2]) : #et les naives (méchantes et gentilles)
                    L_param.append(vect) ###########modification temporaire du code
    param = [L_param[rd.randint(0,len(L_param)-1)] for k in range(Nteam)]
    param.append(np.array((0.2, 0.2, 0.8))) #tit_for_tat
    param.append(np.array((0.001, 1, 0))) #spiteful
    
    print('param defined')
    return L_param



def player_discretisation(niter, precision, Ngene, Nteam) :
    param = select(precision, Nteam)
                
    teamL = generate_personalities([], [], [100]*len(param), [], param)
    Evolution_2(teamL, niter, Ngene)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    #plt.scatter([k.strategy[1] for k in teamL if k.individuals !=0], [k.strategy[2] for k in teamL if k.individuals !=0], s=30, c=[k.individuals for k in teamL if k.individuals !=0], cmap = 'Spectral')
    im = ax.scatter([k.strategy[0] for k in teamL], [k.strategy[1] for k in teamL], [k.strategy[2] for k in teamL], s=30, c=[k.individuals for k in teamL], cmap = 'magma_r')

    fig.colorbar(im, ax=ax)    
    plt.show()
    
    return teamL
 



def convergence_player() :
    teamL = player_discretisation(100, 20, 30, 400) #on joue une fois la discrétisation
    winner = [k for k in teamL if k.individuals > 0] #on garde que celles qui ont survécu
    win_cop = len(winner) + 1
    print('discretisation terminée')
    
    while win_cop != len(winner) : #tant que on arrive à en sélectionner,
        win_cop = len(winner)
        print(win_cop)
        for k in winner :  
            k.individuals = 100
        Evolution_2(winner, 100, 30) #on joue l'évolution pour retirer celles qui meurent
        winner = [k for k in winner if k.individuals > 0]
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.scatter([k.strategy[0] for k in winner], [k.strategy[1] for k in winner], [k.strategy[2] for k in winner], s=30, cmap = 'magma_r')
    
    plt.show()
    
    return winner




def plot_plans(teamL) :
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.scatter([k.strategy[0] for k in teamL], [k.strategy[1] for k in teamL], [k.strategy[2] for k in teamL], c =[k.individuals for k in teamL], s=30, cmap = 'magma_r')
    
    
    X = np.linspace(-1, 1, 2)
    Y = np.linspace(-1, 1, 2)
    X,Y = np.meshgrid(X, Y)
    Z = 1*X/1.2 - Y/1.1 
    #Y2 = X-Z
    plt.gca().plot_surface(X, Y, Z)
    #plt.gca().plot_surface(X, Y2, Z)

    plt.show()




def player_discretisation_zoom(precision) :
    val1 = np.linspace(-1,1, precision+1)
    val2 = np.linspace(-1, 1, precision+1) #[-1,1] découpé en précision intervales de même longueur
    val3 = np.linspace(-1, 1, precision+1)
    l = len(val1)
    
    vector = vector_L(0)
    
    L_param = [] #liste de tous les paramètres possibles
    for k1 in range(l) :
        for k2 in range(l) :
            for k3 in range(l) :
                L_param.append(np.array((val1[k1], val2[k2], val3[k3])))
                
    teamL = Evolution(100, [100]*len(L_param+vector), 40, [], [], [], L_param + vector)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    #plt.scatter([k.strategy[1] for k in teamL if k.individuals !=0], [k.strategy[2] for k in teamL if k.individuals !=0], s=30, c=[k.individuals for k in teamL if k.individuals !=0], cmap = 'Spectral')
    im = ax.scatter([k.strategy[0] for k in teamL], [k.strategy[1] for k in teamL], [k.strategy[2] for k in teamL], s=30, c=[k.individuals for k in teamL], cmap = 'magma_r')

    fig.colorbar(im, ax=ax)
    plt.show()
    
    return teamL





def zd_discretisation(niter, precision, Ngene, Nteam) :
    
    val1 = np.linspace(0, 1, precision+1)
    val2 = np.linspace(0, 1, precision+1) #[-1,1] découpé en précision intervales de même longueur
    val3 = np.linspace(0, 1, precision+1)
    val4 = np.linspace(0, 1, precision+1)
    l = len(val1)
    L_param = [] #liste de tous les paramètres possibles
    for k1 in range(l) :
        for k2 in range(l) :
            for k3 in range(l) :
                for k4 in range(l) :
                    L_param.append(np.array((val1[k1], val2[k2], val3[k3], val4[k4])))
    
    ll = len(L_param)-1
    param = [L_param[rd.randint(0,ll)] for k in range(Nteam)]
                
    teamL = Evolution(niter, [100]*len(param), Ngene, [], [], param, [])
    
    return teamL




def etude_liste_zd(teamL) :
    d = trier_gains(teamL)
    E = [k for k in d if k.individuals > 0]
    F = [k for k in d if k.individuals == 0]
    e, f = len(E), len(F)
    G = []
    p1 = 0
    q1 = 0
    for k in range(e) :
        G.append(E[k].strategy[1] + E[k].strategy[2] + E[k].strategy[3])
        if E[k].strategy[0] == 1 :
            p1 += 1
    for k in range(f) :
        if F[k].strategy[0] == 1 :
            q1 += 1
    X = [k for k in range(e)]
    plt.plot(X, G, color = 'black', linewidth = 1)
    plt.xlabel('rang')
    plt.ylabel('p2+p3+p4')
    return G, p1/e, q1/f




""" FIN DISCRETISATION DES PARAMETRES"""




""" EXECUTION """



def norme(vector) :
    return np.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)



def winner(teamL) :
    win = [k for k in teamL if k.individuals > 0]
    param = [k.strategy for k in win]
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    
    ax.set_zlim(-1, 1)
    ax.xaxis.set_ticklabels(['-1', '', '-0.5', '', '0', '', '0.5', '', '1'])
    ax.yaxis.set_ticklabels(['-1', '', '-0.5', '', '0', '', '0.5', '', '1'])
    ax.zaxis.set_ticklabels(['-1', '', '-0.5', '', '0', '', '0.5', '', '1'])
    
    X = np.linspace(-1, 1, 2)
    Y = np.linspace(-1, 1, 2)
    X,Y = np.meshgrid(X, Y)
    Z = 1*X - Y
    plt.gca().plot_surface(X, Y, Z, cmap = "magma_r")
    
    im = ax.scatter([k[0] for k in param], [k[1] for k in param], [k[2] for k in param], c = [k.individuals for k in teamL if k.individuals > 0], s=30, cmap = 'magma_r')
    
    fig.colorbar(im, ax=ax)
    plt.show()


def barycentre(param) :
    l = len(param)
    xg = sum([k[0] for k in param])/l
    yg = sum([k[1] for k in param])/l
    zg = sum([k[2] for k in param])/l
    return np.array((xg, yg, zg))
    





#S = [tit_for_tat, gradual, pavlov, hard_majo, soft_majo, mechante, spiteful, suspicious_tft ,gentille, ca_strat]
#Snom = ['tit_for_tat', 'gradual', 'pavlov', 'hard_majo', 'soft_majo', 'mechante', 'spiteful', 'suspicious_tft', 'gentille', 'carlos']
#Evolution(1000, [200]*14, 100, S,Snom)
#Evolution(100, [200]*11, 30, S, Snom, [], [[1,1,1,1]])





#Evolution(10, [931, 69], 50, [mechante, tit_for_tat], ['mechante', 'tft'])
#invasion des méchantes par les tft


#S3 = [periodic_cct, periodic_ttc, soft_majo]
#S3nom = ['periodic_cct', 'periodic_ttc', 'soft_majo']
#Evolution(1000, [450, 1000, 100], 500, S3 ,S3nom, [],[]) #une sinusoide amortie
#Evolution(1000, [300,200,100], 300, S3, S3nom) #une sinusoide non amortie





#L =test_zd(10000, [2/3,0,2/3,1/3], S, Snom)
#egaliseur contre S, qui fixe leurs gains à 2



""" """


#T = [tit_for_tat, spiteful, sondeur, hard_majo, mechante, probe, pavlov, indecise, periodic_ttc, gentille]
#Tnom = ['donnant_d', 'rancunière', 'sondeur', 'hard_majo', 'méchante', 'probe', 'pavlov', 'indécise', 'per_ttc', 'gentille']
#total(100, generate_personalities(T, Tnom, [1]*11, [], []))

#Y = [gentille, mechante ,soft_majo, periodic_cct, sondeur, probe, mefiante, tit_for_tat, random, indecise, periodic_ttc, dog, random_9]
#Yn = ['gentille', 'méchante', 'soft_majo', 'per_cct', 'sondeur', 'probe', 'méfiante', 'donnant-d', 'lunatique', 'indécise', 'per_ttc', 'dog', 'random_9']
#total(100, generate_personalities(Y, Yn, [1]*13, [], []))


#u = [tit_for_tat, tit_for_tat, tit_for_tat, mechante, mechante, mechante, gentille, gentille, gentille, gentille]
#un = ['donnant_d','donnant_d','donnant_d','méchante','méchante','méchante', 'gentille','gentille','gentille','gentille']
#total(100, generate_personalities(u, un, [1]*10, [], []))


I = [tit_for_tat, spiteful, soft_majo, gentille, mechante, mefiante, indecise, sondeur, periodic_cct]
Inom = ['donnant_d', 'rancunière', 'soft_majo', 'gentille', 'méchante', 'méfiante', 'indécise', 'sondeur', 'periodic_cct']
Evolution(100, [100]*9, 30, I, Inom, [], [])


#O = [gentille, mechante, hard_majo, mefiante, indecise, random, soft_majo, ca_strat, periodic_cct]
#Onom = ['gentille', 'méchante', 'hard_majo', 'méfiante', 'indécise', 'lunatique', 'soft_majo', 'ca_strat', 'periodic_cct']
#Evolution(100, [100]*9, 100, O, Onom, [], [])


#P = [tit_for_tat, periodic_ttc, hard_majo, soft_majo, mechante, sondeur, random]
#Pnom = ['donnant_d', 'per_ttc', 'hard_majo', 'soft_majo', 'mechante', 'sondeur', 'random']
#Evolution(100, [200]*10, 30, P, Pnom, [[1, 0.2, 0, 0], [1, 0.4, 0.2, 0]], [])



#discret = player_discretisation_zoom(10)



