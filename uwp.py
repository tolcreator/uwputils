import dice

uwp = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def intToUwp(i):
    return uwp[i]

class Uwp:
    def __init__(self):
        self.starport = 'X'
        self.size = 0
        self.atmosphere = 0
        self.hydrosphere = 0
        self.population = 0
        self.government = 0
        self.lawlevel = 0
        self.techlevel = 0
 
    def generate(self):
        self.size = self.generateSize()
        self.atmosphere = self.generateAtmosphere(self.size)
        self.hydrosphere = self.generateHydrosphere(self.size, self.atmosphere)
        self.population = self.generatePopulation(self.size, self.atmosphere)
        self.starport = self.generateStarport(self.population)
        self.government = self.generateGovernment(self.population)
        self.lawlevel = self.generateLawLevel(self.population, self.government)
        self.techlevel = self.generateTechLevel(self.starport, self.size, self.atmosphere, self.hydrosphere, self.population, self.government)
    
    def __str__(self):
        return self.starport + intToUwp(self.size) + intToUwp(self.atmosphere) + intToUwp(self.hydrosphere) + intToUwp(self.population) + intToUwp(self.government) + intToUwp(self.lawlevel) + '-' + intToUwp(self.techlevel) +\
           "    " + self.getTradeCodes()

    def getTradeCodes(self):
        codes = ""
        if self.atmosphere in [4, 5, 6, 7, 8, 9] and self.hydrosphere in [4, 5, 6, 7, 8] and self.population in [5, 6, 7]:
            codes = codes + "Ag "
        if self.size == 0:
            codes = codes + "As "
        if self.population == 0:
            codes = codes + "Ba "
        if self.atmosphere >= 2 and self.hydrosphere == 0:
            codes = codes + "De "
        if self.atmosphere >= 10 and self.hydrosphere > 0:
            codes = codes + "Fl "
        if self.size >= 5 and self.atmosphere in [4, 5, 6, 7, 8, 9] and self.hydrosphere in [4, 5, 6, 7, 8]:
            codes = codes + "Ga "
        if self.population >= 9:
            codes = codes + "Hi "
        if self.techlevel >= 12:
            codes = codes + "Ht "
        if self.atmosphere in [0, 1] and self.hydrosphere > 0:
            codes = codes + "Fl "
        if self.atmosphere in [0, 1, 2, 4, 7, 9] and self.population >= 9:
            codes = codes + "In "
        if self.population <= 3:
            codes = codes + "Lo "
        if self.techlevel <= 5:
            codes = codes + "Lt "
        if self.atmosphere in [0, 1, 2, 3] and self.hydrosphere in [0, 1, 2, 3] and self.population >= 6:
            codes = codes + "Na "
        if self.population <= 6:
            codes = codes + "Ni "
        if self.atmosphere in [2, 3, 4, 5] and self.hydrosphere in [0, 1, 2, 3]:
            codes = codes + "Po "
        if self.atmosphere in [6, 8] and self.population in [6, 7, 8] and self.government in [4, 5, 6, 7, 8, 9]:
            codes = codes + "Ri "
        if self.atmosphere == 0:
            codes = codes + "Va "
        if self.hydrosphere > 9:
            codes = codes + "Wa "
        return codes

    def generateSize(self):
        return dice.roll(2, 6) - 2;

    def generateAtmosphere(self, size):
        if size in [0, 1, 2]:
            return 0
        atmo = dice.roll(2, 6) + size - 7;
        if atmo < 0:
            return 0
        if size in [3, 4]:  
            if atmo in [0, 1, 2]:
                return 0
            if atmo in [3, 4, 5]:
                return 1
            return 10
        return atmo

    def generateHydrosphere(self, size, atmo):
        if size in [0, 1]:
            return 0
        dm = 0
        if size in [3, 4] and atmo == 10:
            dm = -6
        if atmo in [0, 1]:
            dm = -6
        elif atmo in [2, 3, 11, 12]:
            dm = -4
        hydro = dice.roll(2, 6) + size - 7 + dm
        if hydro < 0:
            return 0
        if hydro > 10:
            return 10
        return hydro

    def generatePopulation(self, size, atmo):
        dm = 0
        if size in [0, 1, 2] or size > 10:
            dm = dm - 1
        if atmo in [5, 6, 8]:
            dm = dm + 1
        else:
            dm = dm - 1
        pop = dice.roll(2, 6) - 2 + dm
        if pop < 0:
            return 0
        return pop
        
    def generateGovernment(self, pop):
        if pop == 0:
            return 0
        gov = dice.roll(2, 6) - 7 + pop
        if gov < 0:
            return 0
        return gov

    def generateLawLevel(self, pop, gov):
        if pop == 0:
            return 0
        law = dice.roll(2, 6) - 7 + gov
        if law < 0:
            return 0
        return law

    def generateStarport(self, pop):
        if pop == 0:
            return 'X'
        if pop in [1, 2]:
            dm = -2
        if pop in [3, 4]:
            dm = -1
        if pop in [5, 6, 7]:
            dm = 0
        if pop in [8, 9]:
            dm = 1
        if pop > 9:
            dm = 2

        port = dice.roll(2, 6) + dm
        if port < 2:
            return 'X'
        if port < 5:
            return 'E'
        if port < 7:
            return 'D'
        if port < 9:
            return 'C'
        if port < 11:
            return 'B'
        return 'A'

    def generateTechLevel(self, port, size, atmo, hydro, pop, gov):
        if pop == 0:
            return 0        
        dm = 0
        if port == 'X':
            dm = dm - 4
        elif port == 'C':
            dm = dm + 2
        elif port == 'B':
            dm = dm + 4
        elif port == 'A':
            dm = dm + 6

        if size < 2:
            dm = dm + 2
        elif size < 5:
            dm = dm + 1

        if atmo < 4:
            dm = dm + 1
        elif atmo > 9:
            dm = dm + 1

        if hydro in [0, 9]:
            dm = dm + 1
        elif hydro == 10:
            dm = dm + 2

        if pop < 6:
            dm = dm + 1
        elif pop > 8:
            dm = dm + 1
        if pop > 9:
            dm = dm + 1
        if pop > 10:
            dm = dm + 1
        if pop > 11:
            dm = dm + 1

        if gov in [0, 5]:
            dm = dm + 1
        elif gov == 7:
            dm = dm + 2
        elif gov in [13, 14]:
            dm = dm - 2

        tech = dice.roll(1, 6) + dm
        if tech < 0:
            return 0
        return tech





















