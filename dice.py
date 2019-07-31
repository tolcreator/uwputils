import random

def roll(numdice, sides):
    random.seed()
    total = 0
    for x in range(numdice):
        total += random.randint(1, sides)
    return total

class Dice:
    def __init__(self):
        random.seed()

    def roll(self, numdice, sides):
        total = 0
        for x in range(numdice):
            total += random.randint(1, sides)
        return total
