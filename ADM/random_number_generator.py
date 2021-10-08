from typing import Dict
from math import gcd as bltin_gcd

class random_number_generator :
    
        def __init__(self, a, c, m, x_zero) :
            self.a = a
            self.c = c
            self.m = m
            self.x_zero = x_zero
        
        def generate_random_sequence(self) :
            l_random_numbers = []
            l_random_numbers.append(self.x_zero)

            new_term = (self.a * self.x_zero + self.c) % self.m

            while new_term != self.x_zero :
                l_random_numbers.append(new_term)
                prev_term = new_term
                new_term = (self.a * prev_term + self.c) % self.m
        
        def display_random_sequence(self) :
            pass

        def hull_dobell_verification(self) :
            if (bltin_gcd(self.c, self.m) == 1) :
                pass



