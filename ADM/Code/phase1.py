from math import gcd, pi, acos, sqrt

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

def test_carré_unité(liste_yn):

    FICHIER.write("Test du Carrée unitée \n")
    FICHIER.write("H0 : \n")
    FICHIER.write("H1 : \n")
    FICHIER.write("Le teste va être réalisé avec un alpha de 5% \n")
            
    tableauTest = [
        [0.1,0.,0.,0.,0.],
        [0.2,0.,0.,0.,0.],
        [0.3,0.,0.,0.,0.],
        [0.4,0.,0.,0.,0.],
        [0.5,0.,0.,0.,0.],
        [0.6,0.,0.,0.,0.],
        [0.7,0.,0.,0.,0.],
        [0.8,0.,0.,0.,0.],
        [0.9,0.,0.,0.,0.],
        [1.0,0.,0.,0.,0.],
        [1.1,0.,0.,0.,0.],
        [1.2,0.,0.,0.,0.],
        [1.3,0.,0.,0.,0.],
        [1.4,0.,0.,0.,0.],
        [1.5,0.,0.,0.,0.],
        [1.6,0.,0.,0.,0.],
        [1.7,0.,0.,0.,0.],
        [1.8,0.,0.,0.,0.],
        [1.9,0.,0.,0.,0.],
        [2.0,0.,0.,0.,0.]
        ]

    n = 0
    ki2_obs = 0

    for i in range(0,len(liste_yn)-4,4):

        un1 = liste_yn[i]
        un2 = liste_yn[i+1]
        un3 = liste_yn[i+2]
        un4 = liste_yn[i+3]

        if un1 != None and un2 !=None and un3 != None and un4 !=None:
            ri = (un4 - un2) ** 2 + (un3 - un1) ** 2
                    
            if ri < 0.1:
                tableauTest[0][1] +=1
            elif ri < 0.2:
                tableauTest[1][1] +=1
            elif ri < 0.3:
                tableauTest[2][1] +=1
            elif ri < 0.4:
                tableauTest[3][1] +=1
            elif ri < 0.5:
                tableauTest[4][1] +=1
            elif ri <0.6:
                tableauTest[5][1] +=1
            elif ri <0.7:
                tableauTest[6][1] +=1
            elif ri <0.8:
                tableauTest[7][1] +=1
            elif ri <0.9:
                tableauTest[8][1] +=1
            elif ri <1.0:
                tableauTest[9][1] +=1
            elif ri <1.1:
                tableauTest[10][1] +=1
            elif ri <1.2:
                tableauTest[11][1] +=1
            elif ri <1.3:
                tableauTest[12][1] +=1
            elif ri <1.4:
                tableauTest[13][1] +=1
            elif ri <1.5:
                tableauTest[14][1] +=1
            elif ri <1.6:
                tableauTest[15][1] +=1
            elif ri <1.7:
                tableauTest[16][1] +=1
            elif ri <1.8:
                tableauTest[17][1] +=1
            elif ri <1.9:
                tableauTest[18][1] +=1
            else:
                tableauTest[19][1] +=1
            n +=1

        print(n)

        for i in range(len(tableauTest)):
            x = float(tableauTest[i][0])

            if x <= 1:
                tableauTest[i][2] = (pi*x)-((8/3)*(x**(3/2)))+((x**2)/2)
            else:
                tableauTest[i][2] = (1/3)+((pi-2)*x)+(4*(x-1)**(1/2))+((8/3)*(x-1)**3/2)-((x**2)/2)-(4*x*acos(1/(sqrt(x))))

            for y in range((i-1),-1,-1):
                tableauTest[i][2] -= tableauTest[y][2]
            
        for i in tableauTest:
            i[3] = n*i[2]

        FICHIER.write("Avant regroupement \n")
        FICHIER.write("[Fin intervalle, ri, pi, npi, (ri-npi)²/npi ]\n")

        for i in tableauTest:
            print(i)
            FICHIER.write(str(i) + "\n")


    for i in range(len(tableauTest)-1,-1,-1):
        if tableauTest[i][3] <= 5.0:
            tableauTest[i-1][1] += tableauTest[i][1]
            tableauTest[i-1][3] = tableauTest[i-1][2]*n
            del tableauTest[i]

    for i in range(len(tableauTest)):
        tableauTest[i][4] = ((tableauTest[i][1]-tableauTest[i][3])**2)/tableauTest[i][3]
        ki2_obs += tableauTest[i][4]

    FICHIER.write("---------------------\n")
    FICHIER.write("Après regroupement\n")
    FICHIER.write("[Fin intervalle, ri, pi, npi, (ri-npi)²/npi ]\n")

    for i in tableauTest:
        print(i)
        FICHIER.write(str(i) + "\n")

    FICHIER.write("n: " + str(n) + "\n")
    FICHIER.write("Ki2 Obs : " + str(ki2_obs) + "\n")
    FICHIER.write("Calcul du nombre de degrés de liberté : " + str(len(tableauTest)-1) + "\n")
    FICHIER.write("Il faut chercher le ki² avec le bon alpha et le bon degré de libérté dans la table\n")
    FICHIER.write("Conclusion : \n")
    print("Ki2 Obs : "+  str(ki2_obs))

        
def carre_unité(liste_yn):
    print(liste_yn)
    test_carré_unité(liste_yn)

if __name__ == "__main__":
    m = 1000
    a, c = valeurs_pour_périodes_max(m)
    carre_unité(yn(m, a, c, 5))
