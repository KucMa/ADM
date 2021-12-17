from math import gcd
import math
from os import listdir

FICHIER = open("test_carree_unite.txt","w")

class Random_number_generator :
        
    
        def __init__(self, module_m, multiplier_a, increment_c, x_zero) :
            self.module_m = module_m
            self.multiplier_a = multiplier_a
            self.increment_c = increment_c
            self.x_zero = x_zero
            self.xn_random_numbers = self.__generate_random_sequence()
            self.un_random_numbers = self.__convert_to_u_n()
            self.yn_random_numbers = self.__convert_to_y_n() 

        ##PRIVATE METHODS##

        def __generate_random_sequence(self) :
            xn_random_numbers = []
            xn_random_numbers.append(self.x_zero)

            new_term = (self.multiplier_a * self.x_zero + self.increment_c) % self.module_m

            while new_term != self.x_zero :
                xn_random_numbers.append(new_term)
                prev_term = new_term
                new_term = (self.multiplier_a * prev_term + self.increment_c) % self.module_m

            return xn_random_numbers

        def __prime_factor(self, nb) :
            result = []
            div = 2

            while nb % div == 0:
                result.append(div)
                nb = int(nb / div)
            div = 3

            while div <= nb:
                while nb % div == 0:
                    result.append(div)
                    nb = int(nb / div)

                div = div + 2
            return result

        def __is_multiple(self, multiple, nb):
            return multiple % nb == 0

        def __convert_to_u_n (self) :
            return list(map(lambda x : x / self.module_m, self.xn_random_numbers))
        
        def __convert_to_y_n (self) : 
            return list(map(lambda x : int(x * 10), self.un_random_numbers))
            
        ##PUBLIC METHODS##
        
        def display_xn(self) :
            for nb in self.xn_random_numbers:
                print(nb)
        
        def display_un(self) :
            for nb in self.un_random_numbers:
                print(nb)

        def display_yn(self) :
            for nb in self.yn_random_numbers:
                print(nb)

        def period_length(self):
            return len(self.xn_random_numbers)

        def is_max_period_length(self) :
            if gcd(self.module_m, self.increment_c) != 1:
                return False
            
            if not all(map(lambda x : self.__is_multiple(self.multiplier_a - 1, x), self.__prime_factor(self.module_m))):
                return False

            if self.__is_multiple(self.module_m, 4):
                if not self.__is_multiple(self.multiplier_a - 1, 4):
                    return False
            
            return True
        
        ##Carre unite
    
        def testCarréUnité (un):

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

            for i in range(0,len(un)-4,4):

                un1 = un[i]
                un2 = un[i+1]
                un3 = un[i+2]
                un4 = un[i+3]

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
                        tableauTest[i][2] = (math.pi*x)-((8/3)*(x**(3/2)))+((x**2)/2)
                    else:
                        tableauTest[i][2] = (1/3)+((math.pi-2)*x)+(4*(x-1)**(1/2))+((8/3)*(x-1)**3/2)-((x**2)/2)-(4*x*math.acos(1/(math.sqrt(x))))

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

        
        def carreUnite(self):
            liste_yn = self.yn_random_numbers

            self.display_yn(liste_yn)

            ##self.testCarreUnite(liste_yn)
                
        ##TESTING, DELETE WHEN DONE##

test_1 = Random_number_generator(100, 13, 65, 35)
test_2 = Random_number_generator(16, 5, 3, 7)
test_3 = Random_number_generator(36, 13, 7, 7)
test_4 = Random_number_generator(100, 13, 65, 7)
test_5 = Random_number_generator(100, 13, 63, 7)
test_6 = Random_number_generator(63, 22, 4, 7)


"""print("XN")
test_3.display_xn()
print("------")

print("YN")
test_3.display_yn()
print("------")

print("UN")
test_3.display_un()"""

test_3.carreUnite()