"""
ici on va rajouter une règle au jeu du dilemme itéré du prisonnier :
    - chaque stratégie a le droit de 'renoncer' en plus de coopérer et de trahir
    en faisant cela au cours d'un match, elle impose que durant le reste du match, ie pendant
    toutes les prochaines parties, les deux stratégies adversaires gagneront 2 points chacune.

on conserve avec cette règle la propriété de jeu à somme non constante, car dans le cas de renonciation, 
les deux stratégies emportent au total 4 points (contre 2, 5, 6 dans les autres cas).
cette règle est intéressante car : 
    elle peut être assimilée à un des joueurs qui abandonne et qui s'écarte de son adversaire car 
    il n'a plus envie de l'affronter, sécurisant ainsi quelques points.
    
    il est toujours mieux de trouver un compromis stable [C,C] que de renoncer trop vite car cela 
    rapporte plus de points.
    cependant il est plus intéressant de renoncer plutôt que de laisser son adversaire trahir trop souvent
    car on remporte 2 points plutot que 1
"""



import matplotlib.pyplot as plt
import numpy as np
import random as rd
#from matplotlib import animation

import strategies as t






class joueur :
    
    
    players_created = 0
    
    def __init__(self, strat, stratname, Nindiv) :   #type_joueur définit si le joueur sera un player ou une fonction stratégie
        """
            classe des équipes, un seul individu de l'équipe affrontera les autres et après
            ses gains sont multipliés par le nombre d'individus dans l'équipe
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
        self.trace = 0 #pour le graph
        
        self.renonciation = False #False : il n'a pas renoncé, True : il a renoncé
        self.position = [0,0]




    def play(self) :
        return self.strategy(self.memory, self.param)
    
    
    
    def reset(self) :
        self.memory = [[], []]
        self.param = []
        self.adversary = 0


    def repop(self, gaintot) :
        self.individuals = int(self.gain_final * Ntot / gaintot)












""" DILEMME ITERE DU PRISONNIER """



def dilemme(coopere): #définira le gain de chacun des deux joueurs. True=coopérer, False=trahir, 2 = renoncer
#coopere[0] est l'action choisie par J1, coopere[1] est celle de J2, et le gain retourné est dans le même ordre : [gain J1, gain J2]
    if coopere[0] == 2 :   #[R, (T, C, ou R)]
        return [2,2]
    elif coopere[0] :
        if coopere[1] == 2 :  #[C,R]
            return [2,2]
        elif coopere[1] :    #[C,C]
            return [3,3]
        elif not coopere[1] :   #[C,T]
            return [0,5]
    else :
        if coopere[1] == 2 :   #[T,R]
            return [2,2]
        elif coopere[1] :   #[T,C]
            return [5,0]
        elif not coopere[1] :   #[T,T]
            return [1,1]



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



def renonciation(n, player1, player2) : 
    """
        en cas de renonciation d'un des joueurs, cette fonction termine le 
        match automatiquement en donnant 2*nbdetoursrestants points aux deux joueurs
    """
    points_renoncement = (n - len(player1.memory[0])) * 2
    player1.gain += points_renoncement
    player2.gain += points_renoncement



def match(n,player1,player2) : #n nombre de parties par affrontement. il retourne la liste des gains cumulés
    k = 0
    while k < n :
        k += 1
        partie(player1,player2)
        if player1.memory[0][-1] == 2 : #si j1 a renoncé :
            renonciation(n, player1, player2)
            player1.renonciation = True
        if player2.memory[0][-1] == 2 : #si j2 a renoncé
            renonciation(n, player1, player2)
            player2.renonciation = True #on change l'attribu de renonciation qui servira plus tard
            k = n #en cas de renonciation, on arrête la boucle de force.
    player1.reset() #à la fin du match, on reset les attributs des joueurs
    player2.reset()
    


def tournoi_fast(n, teamL) : #ici y a une erreur à corriger, quand il s'affronte lui même il ne faut pas multiplier son gain par le nombre d'individus.
    l = len(teamL)
    for k in range(l) :
        for m in range(k, l) :
            if k == m :
                a = joueur(teamL[m].strategy, teamL[m].stratname, 1)
                match(n, teamL[k], a)
                
                teamL[k].gain_list[m] = teamL[k].gain * (teamL[m].individuals -1)
            if k != m :
                match(n, teamL[k], teamL[m])
                
                teamL[k].gain_list[m] = teamL[k].gain * teamL[m].individuals
                teamL[m].gain_list[k] = teamL[m].gain * teamL[k].individuals
                
            #divisé par deux car dans partie, le joueur incrémente deux fois son gain (au final son gain est deux fois ce qu'il devrait être)
            teamL[k].gain = 0
            teamL[m].gain = 0
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




def generate_teams(S,Snom, Nindiv) :
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



def Evolution(niter, Nindiv, Ngene, S, Snom) : #alea est un booléen, l'utilisateur choisit s'il veut rajouter une aléa ou non
    teamL = generate_teams(S,Snom, Nindiv) #initialisation de la liste des joueurs
    demography = [] #liste qui va retenir les listes des individus de chaque team, au fil des générations
    for k in range(Ngene) :
        demography.append([k.individuals for k in teamL])
        generation(niter, teamL)
        print(demography[-1])
    graph(Ngene, demography, teamL)



def graph(Ngene,demography,teamL) : #trace toutes les courbes à la fin de la simulation
    X = np.linspace(1,Ngene,Ngene)
    
    for k in range(lenS) :
        Y = [y[k] for y in demography]
        teamL[k].trace = plt.plot(X,Y, label = teamL[k].stratname)
    plt.legend(loc = 'upper left')
    plt.xlabel('generations')
    plt.ylabel('populations')
    plt.show()



""" FIN EVOLUTION """







""" DEBUT JEU DE PLATEAU """

"""
on met en pratique la règle de renonciation :
    dans un grand terrain on place aléatoirement des équipes de stratégies appelées 'tribus'
    le rayon de détection d'une tribu est proportionnel à son Nindiv.
    lorsque deux tribus sont suffisament proches (ie dans leurs rayons de détection), elles 
    s'affrontent dans le jeu d'évolution

a l'issue du tournoi, il y a plusieurs cas possibles :
    -la mort d'une équipe, auquel cas l'autre maintient sa position en ayant 'mangé' les
    individus de la tribu vaincue
    -un nouvel équilibre stable est atteint par les équipes lors du tournoi, auquel cas 
    les deux équipes restent à leur position, elles vivent en harmonie avec leurs nouveaux 
    Nindiv.
    -il y a stabilité entre les tribus, mais l'une d'elles (ou les deux) a renoncé lors 
    de l'affrontement, auquel cas l'équipe ayant renoncé doit se déplacer sur le terrain, 
    s'écarter de son adversaire, ce qui provoquera éventuellement une nouvelle rencontre.
    -si plus de deux tribus sont au même endroit, elles s'affrontent toutes dans l'évolution,
    et les mêmes règles que plus haut s'appliquent
    
on modélise ici la présence de plusieurs tribus de chasseurs qui tentent de survivre dans 
la nature.
lorsque deux tribus se rencontrent, soit elles décident de coopérer pour maximiser leur
butin (6) et le partager également entre les deux équipes. Soit une des équipes trahit
l'autre en lui volant une partie du butin, la traitre gagne 5 et l'autre 0. Soit les deux 
équipes se trahissent mutuellement et leur butin est médiocre. Soit l'une des tribus 
préfère s'écarter de son adversaire, pour ne pas risquer la trahison, les deux tribus vont
alors chasser séparément et ne gagner que deux points chacunes car privées de l'aide de
l'autre équipe qui lui aurait rapporté un point en plus.
"""




def coord(tribuL) :
    for e in tribuL :
        e.position = [rd.random(), rd.random()]



def distance(pos1, pos2) : #calcule la distance euclidienne entre deux points
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5



def voisins(tribuL) : #crée un tableau dans l'ordre de tribuL, avec les indices des tribus qui sont assez proches
    """
        on part du principe qu'une tribu adverse est voisine si elle est dans le disque 
        de centre la position de la tribu qu'on traite et de rayon son nombre d'individus
        que multiplie 10E-4 (pour une remise à l'échelle)
    """
    l = len(tribuL)
    d = [[]]*l
    for k in range(l) :
        d[k] = [m for m in range(k, l) if distance(tribuL[k].position, tribuL[m].position) < tribuL[k].individuals*10e-4]
    return d




def rencontre(tribuL, d) : #munie d'une liste des tribus voisines pour chaque tribu, cette fonction
    #s'occupe de faire jouer les voisins dans un jeu d'évolution
    l = len(tribuL)
    for k in range(l) :
        voisins = [tribuL[m] for m in d[k] if tribuL[m].individuals != 0]
        for m in range(30) :
            generation(500, voisins)
    



def trajectoire(depart, arrivee, n) :
    x = arrivee[0] - depart[0]
    y = arrivee[1] - depart[1]
    return [depart[0] + x*n, depart[1] + y*n]




def deplacement(L ,tribuL) : # L est la liste des équipes qui ont renoncé et qui doivent donc se déplacer.
    l = len(tribuL)
    for k in L :
        arrivee = [k.position[0] + rd.random()*0.2, k.position[1] + rd.random()*0.2]
        n = 0
        while n < 5 :
            n+=1
            pos = trajectoire(k.position, arrivee, n)
            for m in range(l) :
                if distance(k.position, tribuL[m].position) < k.individuals*10e-4 and k != tribuL[m]:
                    n = 5
                    break
            k.position = pos
    



def enlever_renonciation(tribuL) :
    for k in tribuL :
        k.renonciation = False





def tour(tribuL) : #fait un tour de la liste tribuL pour les faire s'affronter, déplacer etc
    d = voisins(tribuL)
    rencontre(tribuL, d)
    deplacement([k for k in tribuL if k.renonciation], tribuL)
    enlever_renonciation(tribuL)
    




def survival(S, Snom, Nindiv, tours) :
    tribuL = generate_teams(S, Snom, Nindiv)
    coord(tribuL)
    for k in range(tours) :
        plt.close()
        #terrain(tribuL)
        plt.show()
        tour([k for k in tribuL if k.individuals != 0])
        
        print(k)



"""
def terrain(tribuL) : #pour afficher le terrain avec les positions des tribus
    theta = np.linspace(0, 2*np.pi, 100)
    for k in tribuL :
        x1 = k.individuals * 10e-4 * np.cos(theta) + k.position[0]
        x2 = k.individuals * 10e-4 * np.sin(theta) + k.position[1]
        k.trace = plt.plot(x1, x2, label = k.stratname)
    
    X = [k.position[0] for k in tribuL]
    Y = [k.position[1] for k in tribuL]
    plt.plot(X, Y, marker = 'o', linewidth = 0, color = 'black')
    
    plt.grid(linestyle='--')
    plt.xlim(-0.5,1.5)
    plt.ylim(-0.5,1.5)
    plt.legend(loc = 'upper left')
    
    plt.show()
"""






"""
def init():
    line.set_data([],[])
    return line,





def animate(i) :
    tour([k for k in tribuL if k.individuals != 0])
    x = [k.position[0] for k in tribuL]
    y = [k.position[1] for k in tribuL]
    line.set_data(x, y)
    return line,

"""


def animation(S, Snom, tours, N_init) :
    tribuL = generate_teams(S, Snom, [N_init]*len(S))
    coord(tribuL)
    plt.xlim(-1, 2)
    plt.ylim(-1, 2)
    for i in range(tours) :
        x = [k.position[0] for k in tribuL]
        y = [k.position[1] for k in tribuL]
        
        theta = np.linspace(0, 2*np.pi, 100)
        for k in tribuL :
            
            a = [k.individuals * 10e-4 * np.cos(th) + k.position[0] for th in theta]
            b = [k.individuals * 10e-4 * np.sin(th) + k.position[1] for th in theta]
            
        tour(tribuL)
        if i == 0 :
            line, = plt.plot(x, y, marker = 'o' , linewidth = 0, color = 'black')
            for k in tribuL :
                k.trace = plt.plot(a, b)
        else:
            line.set_ydata(y)
            line.set_xdata(x)
            
            plt.pause(4) # pause avec duree en secondes

























#il y a un bug au niveau de l'affichage, je voudrais qu'il m'affiche les images à chaque tour, et pas seulement à la fin
#l'ordre d'affrontement des tribus n'est pas logique, il faut le modifier
#il faut arranger la définition du rayon de détection



S = [t.gentille, t.mechante, t.tit_for_tat, t.dure, t.tft_w_threshold, t.indulgente]
Snom = ['gentille','mechante','tit_for_tat','dure','tft_w_threshold', 'indulgente']
#Evolution(100, [200]*6, 100, S,Snom)


S2 = [t.prudence, t.mechante]
S2nom = ['indulgente', 'tft']
#total(100, generate_personalities(S2, S2nom, [1]*2))














