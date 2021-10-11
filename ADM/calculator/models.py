class Serie:
    def __init__(self, module, multiplier, increment, seed):
        self.module = module
        self.multiplier = multiplier
        self.increment = increment
        self.seed = seed
        self.numbers = self.numbers_generator()

    def numbers_generator(self):
        numbers = [self.seed]
        x = self.seed
        x = (self.multiplier * x + self.increment) % self.module
        
        while x != self.seed:
            numbers.append(x)
            x = (self.multiplier * x + self.increment) % self.module

        return numbers


