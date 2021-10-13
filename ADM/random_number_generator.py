from math import gcd

class Random_number_generator :
    
        def __init__(self, module, multiplier, increment, x_zero) :
            self.module = module
            self.multiplier = multiplier
            self.increment = increment
            self.x_zero = x_zero
            self.xn_random_numbers = self.generate_random_sequence()
            self.un_random_numbers = self.__convert_to_u_n()
            self.yn_random_numbers = self.__convert_to_y_n()


        '''@property
        @multiplier.setter
        def multiplier(self, multiplier):
            if multiplier >= 2 and multiplier < self.module:
                self.multiplier = multiplier

        @increment.setter
        def increment(self, increment):
            if increment >= 0 and increment < self.module:
                self.increment = increment

        @module.setter
        def module(self, module):
            if module >= 3:
                self.m = module
        
        @x_zero.setter
        def x_zero(self, x_zero):
            if x_zero >= 0 and x_zero < self.module:
                self.x_zero = x_zero'''
        

        
        def generate_random_sequence(self) :
            xn_random_numbers = []
            xn_random_numbers.append(self.x_zero)

            new_term = (self.multiplier * self.x_zero + self.increment) % self.module

            while new_term != self.x_zero :
                xn_random_numbers.append(new_term)
                prev_term = new_term
                new_term = (self.multiplier * prev_term + self.increment) % self.module

            return xn_random_numbers
        
        def display_random_sequence(self) :
            for nb in self.xn_random_numbers:
                print(nb)

        def period_length(self):
            return len(self.xn_random_numbers)

        def is_max_period_length(self) :
            if gcd(self.module, self.increment) != 1:
                return False
            
            if not all(map(lambda x : self.__is_multiple(self.multiplier - 1, x), self.__prime_factor(self.module))):
                return False

            if self.__is_multiple(self.module, 4):
                if not self.__is_multiple(self.multiplier - 1, 4):
                    return False
            
            return True

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
            return map(lambda x : x / self.module, self.xn_random_numbers)
        
        def __convert_to_y_n (self) : 
            return map(lambda x : int(x * 10), self.un_random_numbers)
            

test_1 = Random_number_generator(100, 13, 65, 35)
test_2 = Random_number_generator(16, 5, 3, 7)
test_3 = Random_number_generator(36, 13, 7, 7)
test_4 = Random_number_generator(100, 13, 65, 7)
test_5 = Random_number_generator(100, 13, 63, 7)
test_6 = Random_number_generator(63, 22, 4, 7)

print("Test 1")
print(test_1.is_max_period_length())
print(test_1.period_length())
print("Test 2")
print(test_2.is_max_period_length())
print(test_2.period_length())
print("Test 3")
print(test_3.is_max_period_length())
print(test_3.period_length())
print("Test 4")
print(test_4.is_max_period_length())
print(test_4.period_length())
print("Test 5")
print(test_5.is_max_period_length())
print(test_5.period_length())
print("Test 6")
print(test_6.is_max_period_length())
print(test_6.period_length())
