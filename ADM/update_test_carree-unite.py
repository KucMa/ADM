from math import gcd, pi, acos, sqrt
import pandas as pd
import numpy as np

FICHIER = open("test_carree_unite.txt","w")

def xn(m, a, c, x0):
    xn = [x0]
    x1 = (a * x0 + c) % m
    while (x1 != x0):
        xn.append(x1)
        x1 = (a * x1 + c) % m
    return xn

def facteurs_premiers(nb):
    facteurs_premiers = []
    div = 2
    while nb % div == 0:
        facteurs_premiers.append(div)
        nb = int(nb / div)
    div = 3
    while div <= nb:
        while nb % div == 0:
            facteurs_premiers.append(div)
            nb = int(nb / div)
        div = div + 2
    return facteurs_premiers

un = lambda m, a, c, x0 : [x / m for x in xn(m, a, c, x0)]
yn = lambda m, a, c, x0 : [int(x * 10) for x in un(m, a, c, x0)]
est_multiple = lambda multiple_to_test, nb: multiple_to_test % nb == 0

def a_periode_max(a, c, m):
    if gcd(m, c) != 1:
        return False
    if not all(map(lambda x: est_multiple(a - 1, x), facteurs_premiers(m))):
        return False
    if est_multiple(m, 4) and not est_multiple(a - 1, 4):
        return False
    return True

def valeurs_pour_périodes_max(m):
    c = 2
    a = 2
    while c < m and not a_periode_max(a, c, m):
        while a < m and not a_periode_max(a, c, m):
            a += 1
        if not a_periode_max(a, c, m):
            c += 1
            a = 2
    return a, c

def générer_intervalles(step, début, fin):
    intervalles = {"Début" : [], "Fin" : []}
    for i in np.arange(début, fin, step):
        intervalles["Début"].append(round(i, 1))
        intervalles["Fin"].append(round(i + step, 1))

    return intervalles

def pi_test_carré_unité():
    probabilités = []

    for i in range(20):
        pri = (i + 1) / 10
        if pri <= 1:
            probabilités.append((pi * pri - ((8/3) * pri**(3/2)) + ((pri**2) / 2)) - sum(probabilités))
        else:
            probabilités.append(((1/3) + (pi - 2) * pri + 4*((pri - 1)**(1/2)) + (8/3) * ((pri - 1)**(3/2)) - ((pri**2) / 2) - 4 * pri * acos(1/sqrt(pri))) - sum(probabilités))

    return probabilités

def test_carré_unité(un):

    FICHIER.write("Test du Carrée unitée \n")
    FICHIER.write("H0 : \n")
    FICHIER.write("H1 : \n")
    FICHIER.write("Le teste va être réalisé avec un alpha de 5% \n")

    tableau = {
        "Xi" : générer_intervalles(0.1, 0, 2),
        "ri" : [0 for _ in range(20)],
        "pi" : pi_test_carré_unité(),
        "npi" : [None for _ in range(20)],
        "(ri-npi)²/npi" : [None for _ in range(20)]
    }

    n = 0
    ki2_obs = 0

    for i in range(0, len(un), 4):
        u0 = un[i]
        u1 = un[i + 1]
        u2 = un[i + 2]
        u3 = un[i + 3]

        if any(map(lambda x : x is None, [u0, u1, u2, u3])):
            break;

        dist = (u3 - u1)**2 + (u2 - u0)**2
        n += 1

        for y in range(len(tableau["ri"])):
            if dist >= tableau["Xi"]["Début"][y] and tableau["Xi"]["Fin"][y] > dist:
                tableau["ri"][y] += 1
                break;

    for y in range(len(tableau["ri"])):
        tableau["npi"][y] = tableau["ri"][y] * tableau["pi"][y]
        if tableau["npi"][y] != 0:
            tableau["(ri-npi)²/npi"][y] =  (tableau["ri"][y] - tableau["npi"][y])**2 / tableau["npi"][y]

    df = pd.DataFrame()
    
    df.insert(0, "Début", tableau["Xi"]["Début"])
    df.insert(1, "Fin", tableau["Xi"]["Fin"])
    df.insert(2, "ri", tableau["ri"])
    df.insert(3, "pi", tableau["pi"])
    df.insert(4, "npi", tableau["npi"])
    df.insert(5, "(ri-npi)²/npi", tableau["(ri-npi)²/npi"])

    FICHIER.write("TABLEAU AVANT REGROUPEMENT\n")
    FICHIER.write(str(df))

       

        
def carre_unité(un):
    #print(un)
    test_carré_unité(un)

if __name__ == "__main__":
    m = 1000
    a, c = valeurs_pour_périodes_max(m)
    carre_unité(un(m, a, c, 5))
