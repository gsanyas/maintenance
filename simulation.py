from bisect import insort
from random import random

def emulate(t,S):
    """[summary]

    Args:
        t ([int]): [nombre d'équipes disponibles à l'instant initial]
        S ([int]): [seuil de déterioration à partir duquel une équipe intervient sur une éolienne]

    Returns:
        [type]: [description]
    """

    ## ---------------------------------------------------------------------------
    ## Système à l'état initial

    ## Données initiales
    N = 365 # nombre de jours de simulation
    NE = 20 # nombre d'éoliennes
    CRM = 100 # coût fixe par équipe
    CM = 50 # coût fixe par maintenance
    s = [0]*NE # etat initial de chaque eolienne (varie entre 0 et 3)
    v = 0 # vent le premier jour
    m = [0]*NE # etat de maintenance initial de chaque eolienne

    ## Evolution du systeme
    V = [
        [0.2,0.73,0.07],
        [0.11,0.74,0.15],
        [0.04,0.61,0.35]
    ]
    P1 = [
        [0.95,0.05,0,0],
        [0,0.94,0.05,0.01],
        [0,0,86,0.14],
        [0,0,0,1]
    ]
    P2 = [
        [0.9,0.09,0.01,0],
        [0,0.87,0.11,0.02],
        [0,0,0.79,0.21],
        [0,0,0,1]
    ]
    P = [P1,P2]


    ## Variables de sortie
    r = 0 # production des éoliennes
    c = CRM*t # coût total (fixe et variable)


    ## ---------------------------------------------------------------------------
    ## Simulation
    for n in range(N):
        #print("-------------------------")
        #print("Jour : ",n)
        #print("Etat d vent : ",v)
        k = [] # liste contenant les éoliennes à réparer
        #print("Etat des eoliennes : ",s)
        for e in range(NE): # recherche des éoliennes à réparer
            if m[e]==0: # si l'éolienne n'est pas en maintenance
                if s[e] >= S: # si l'éolienne est plus abimée que le seuil
                    insort(k,(s[e],e)) # trie selon l'état de l'éolienne
            else: # si l'éolienne est déjà en maintenance ou en préparation
                if m[e] < 3 or v != 2: # si la maintenance peut progresser
                    m[e] = (m[e]+1) % 6 # elle avance d'un cran
                    if m[e]==0: # si la maintenance vient de se terminer
                        t+=1 # on libère une équipe
                        s[e] = 0
        j=0
        #print("Liste à réparer : ",k)
        #print("Nombre d'équipes disponibles : ",t)
        while j<t and j<len(k): # assignation des équipes aux éoliennes à réparer
            m[k[j][1]]=1
            j+=1
            c+=CM
        t = max(0,t-j)
        #print("Maintenance : ",m)
        #print("Nombre d'équipes disponibles ensuite : ",t)
        for e in range(NE): # dégradation des éoliennes et production
            if m[e]< 3 and s[e] < 3 and v > 0: # si l'éolienne peut être abimée
                if v != 2 or s[e]!=2: # si l'éolienne fonctionne
                    r += v # production
                j,rn,b = 0,random(),P[v-1][s[e]][0]
                while b < rn:
                    j+=1
                    b += P[v-1][s[e]][j]
                s[e] = j # dégradation de l'éolienne
        #print("Production actuellement : ",r)
        #print("Cout actuellement : ",c)
        j,rn,b = 0,random(),V[v][0]
        while b < rn:
            j+=1
            b += V[v][j]
        v=j # évolution du vent pour le jour suivant
    return r,c

def printDic(D):
    for d in D:
        print(d,D[d])

S = [2,3]
T = [1,2,3,4,5,6,7,8,9,10]
results = dict()

for p in [1+i/5 for i in range(15)]:
    print("p = ",p)
    for s in S:
        print("s = ",s)
        for t in T:
            rs,cs = 0,0
            for n in range(100):
                r,c = emulate(t,s)
                rs += r*p
                cs += c
            results[(s,t,p)] = rs/100,cs/100,(rs-cs)/100

printDic(results)
