from math import gcd, pi, acos, sqrt
import pandas as pd
import numpy as np
import scipy.stats

# Changer les paramètres de la sequence aléatoire (a,c,m,x0) => ligne 195
# Alpha est obtenu via un input utilisateur (non validé), si besoin de le fixer : ligne 116

FICHIER = open("phase_1.txt","w")

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

def longueur_sequence (sequence) :
    return len(sequence)

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

def regroupement(tableau_continu):
    if (all(map(lambda x : x >= 5, tableau_continu["npi"]))):
        return tableau_continu
    n = sum(tableau_continu["ri"])
    i = 0
    while i < len(tableau_continu["npi"]) and tableau_continu["npi"][i] > 5:
        i += 1

    if i != 0 and i != len(tableau_continu["npi"]) - 1:
        index = tableau_continu["npi"].index(min(tableau_continu["npi"][i - 1], tableau_continu["npi"][i + 1]))
    elif i == 0:
        index = 1
    else:
        index = len(tableau_continu["npi"]) - 2

    tableau_continu["Xi"]["Début"][index] = tableau_continu["Xi"]["Début"][i] if i < index else tableau_continu["Xi"]["Début"][index]
    tableau_continu["Xi"]["Fin"][index] = tableau_continu["Xi"]["Fin"][i] if i > index else tableau_continu["Xi"]["Fin"][index]
    tableau_continu["ri"][index] += tableau_continu["ri"][i]
    tableau_continu["npi"][index] += tableau_continu["npi"][i]
    tableau_continu["pi"][index] += tableau_continu["pi"][i]
    tableau_continu["(ri-npi)²/npi"][index] = (tableau_continu["ri"][index] - tableau_continu["npi"][index])**2 / tableau_continu["npi"][index]
    tableau_continu["Xi"]["Début"].pop(i)
    tableau_continu["Xi"]["Fin"].pop(i)
    tableau_continu["ri"].pop(i)
    tableau_continu["pi"].pop(i)
    tableau_continu["npi"].pop(i)
    tableau_continu["(ri-npi)²/npi"].pop(i)

    regroupement(tableau_continu)

def test_carré_unité(un):

    FICHIER.write("Test du Carrée unitée \n")
    FICHIER.write("La longueur de la séquence est de " + str(longueur_sequence(un))+ "\n")
    FICHIER.write("H0 : La suite passe le test du carré unité\n")
    FICHIER.write("H1 : La suite ne passe pas le test du carré unité\n")
    alpha = int(input("Valeur pour alpha(%)"))
    FICHIER.write("Le test va être réalisé avec un alpha de " + str(alpha) + "%\n")

    tableau = {
        "Xi" : générer_intervalles(0.1, 0, 2),
        "ri" : [0 for _ in range(20)],
        "pi" : pi_test_carré_unité(),
        "npi" : [None for _ in range(20)],
        "(ri-npi)²/npi" : [None for _ in range(20)]
    }


    for i in range(0, len(un)-4, 4): 
        u0 = un[i]
        u1 = un[i + 1]
        u2 = un[i + 2]
        u3 = un[i + 3]

        if any(map(lambda x : x is None, [u0, u1, u2, u3])):
            break;

        dist = (u3 - u1)**2 + (u2 - u0)**2

        for y in range(len(tableau["ri"])):
            if dist >= tableau["Xi"]["Début"][y] and tableau["Xi"]["Fin"][y] > dist:
                tableau["ri"][y] += 1
                break;

    n = sum(tableau["ri"])
    for y in range(len(tableau["ri"])):
        tableau["npi"][y] = n * tableau["pi"][y]
        if tableau["npi"][y] != 0:
            tableau["(ri-npi)²/npi"][y] =  (tableau["ri"][y] - tableau["npi"][y])**2 / tableau["npi"][y]

    

    FICHIER.write("-" * 50)
    FICHIER.write("\n")
    FICHIER.write("---TABLEAU AVANT REGROUPEMENT---\n")
    save_tableau(tableau, FICHIER)
    regroupement(tableau)
    FICHIER.write("-" * 50)
    FICHIER.write("\n")
    FICHIER.write("---TABLEAU APRES REGROUPEMENT---\n")
    save_tableau(tableau, FICHIER)

    Ki2_obs = sum(tableau["(ri-npi)²/npi"])
    no_reject_zone = scipy.stats.chi2.ppf(1-(alpha/100), df = len(tableau["ri"])-1)
    is_ok = no_reject_zone > Ki2_obs

    FICHIER.write("-" * 50)
    FICHIER.write("\n")

    FICHIER.write("n: " + str(sum(tableau["ri"])) + "\n")
    FICHIER.write("Ki2 Obs : " + str(sum(tableau["(ri-npi)²/npi"])) + "\n")
    FICHIER.write("Calcul du nombre de degrés de liberté : " + str(len(tableau["ri"]) - 1) + "\n")
    FICHIER.write("Il faut chercher le ki² avec le bon alpha et le bon degré de libérté dans la table\n") #Automatiquement 
    FICHIER.write("Zone de non rejet : " + str(no_reject_zone) + "\n")
    if is_ok:
        FICHIER.write("Conclusion : Nous ne pouvons pas rejeter H0 avec" + str(100-alpha) +"% de certitude, la suite passe le test du carré unité\n") 
    else:
        FICHIER.write("Conclusion : Nous pouvons rejeter H0 avec " + str(100-alpha) + "% de certitude, la suite ne passe pas le test du carré unité.\n")
    FICHIER.close()



def save_tableau(tableau, fichier):
    df = pd.DataFrame()
    df.insert(0, "Début", tableau["Xi"]["Début"])
    df.insert(1, "Fin", tableau["Xi"]["Fin"])
    df.insert(2, "ri", tableau["ri"])
    df.insert(3, "pi", tableau["pi"])
    df.insert(4, "npi", tableau["npi"])
    df.insert(5, "(ri-npi)²/npi", tableau["(ri-npi)²/npi"])
    fichier.write(str(df) + "\n")

def carre_unité(un):
    test_carré_unité(un)

if __name__ == "__main__":
    m = 1500
    a = 23
    c = 82
    x0 = 21
    test_carré_unité(un(m, a, c, x0))

