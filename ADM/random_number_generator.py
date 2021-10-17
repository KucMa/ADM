from math import gcd

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

        ##TESTING, DELETE WHEN DONE##

test_1 = Random_number_generator(100, 13, 65, 35)
test_2 = Random_number_generator(16, 5, 3, 7)
test_3 = Random_number_generator(36, 13, 7, 7)
test_4 = Random_number_generator(100, 13, 65, 7)
test_5 = Random_number_generator(100, 13, 63, 7)
test_6 = Random_number_generator(63, 22, 4, 7)


print("XN")
test_3.display_xn()
print("------")

print("YN")
test_3.display_yn()
print("------")

print("UN")
test_3.display_un()
