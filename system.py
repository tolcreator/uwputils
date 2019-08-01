import dice

UWP_FIELDS = ['Starport', 'Size', 'Atmosphere', 'Hydrosphere', 'Population', 'Government', 'Law', 'Technology']


def strToUWP(suwp):
    suwp = suwp.replace('-', '')
    uwp = {}
    for i in range(len(suwp)):
        uwp[UWP_FIELDS[i]] = suwp[i]
    return uwp


def parseLine(line):
    line = line.strip()
    if not line:
        return None
    if line[0] in ['#']:
        return None
    name = line[:13].strip()
    hex = line[14:18]
    uwp = line[19:28]
    base = line[29:30]
    trade = line[31:47]
    if trade:
        tradeCodes = trade.split()
    else:
        tradeCodes = []
    zone = line[48:49]
    p = line[51:52]
    b = line[52:53]
    g = line[53:54]
    allegiance = line[55:57]
    stellar = line[58:]
    if stellar:
        stars = stellar.split()
    else:
        stars = []
    return {
        'name': name,
        'hex': hex,
        'uwpString': uwp,
        'uwp': strToUWP(uwp),
        'base': base,
        'tradeString': trade,
        'tradeCodes': tradeCodes,
        'zone': zone,
        'p': p,
        'b': b,
        'g': g,
        'allegiance': allegiance,
        'stellarString': stellar,
        'stars': stars
    }

def parseFile(filename, edit=False):

    output = []
    with open(filename, 'r') as file:
        for line in file:
            parsed = parseLine(line)
            if parsed:
                out = parsed['name'].ljust(13) + ' '
                out += parsed['hex'] + ' '
                if not parsed['uwpString']:
                    print list(line)
                    print parsed
                    print "Oops"
                out += parsed['uwpString'] + ' '
                uwp = parsed['uwp']
                if not parsed['tradeString']:
                    parsed['tradeString'] = generateTradeCodes(uwp)
                    parsed['base'] = generateBase(uwp)
                out += parsed['base'] + ' '
                out += parsed['tradeString'].ljust(16) + ' '
                out += parsed['zone'].ljust(1) + '  '
                if not parsed['p'] or parsed['p'] == ' ':
                    parsed['p'] = generatePopulationMultiplier(uwp)
                if not parsed['b'] or parsed['b'] == ' ':
                    parsed['b'] = generateBelts(uwp)
                if not parsed['g'] or parsed['g'] == ' ':
                    parsed['g'] = generateGasGiants(uwp)
                out += parsed['p'] + parsed['b'] + parsed['g'] + ' '
                #out += parsed['allegiance'].ljust(2) + ' '
                out += 'Na '
                if not parsed['stellarString']:
                    parsed['stellarString'] = generateStars(uwp)
                out += parsed['stellarString']
                out += '\n'
                output.append(out)
            else:
                output.append(line)
    if edit:
        with open(filename, 'w') as file:
            for line in output:
                file.write(line)

def generateBase(uwp):
    naval = False
    scout = False
    pirate = False
    if uwp['Starport'] in ['A', 'B']:
        if dice.roll(2, 6) > 7:
            naval = True
    if uwp['Starport'] in ['A', 'B', 'C', 'D']:
        roll = dice.roll(2, 6)
        if uwp['Starport'] == 'C':
            roll -= 1
        if uwp['Starport'] == 'B':
            roll -= 2
        if uwp['Starport'] == 'A':
            roll -= 3
        if roll > 6:
            scout = True
    if uwp['Starport'] not in ['A'] and not naval:
        if dice.roll(2, 6) == 12:
            pirate = True
    if scout and naval:
        return 'A'
    if scout and pirate:
        return 'G'
    if scout:
        return 'S'
    if naval:
        return 'N'
    if pirate:
        return 'P'
    return ' '


def getIsAgricultural(uwp):
    if uwp['Atmosphere'] in ['4', '5', '6', '7', '8', '9']\
            and uwp['Hydrosphere'] in ['4', '5', '6', '7', '8']\
            and uwp['Population'] in ['5', '6', '7']:
        return True


def getIsAsteroid(uwp):
    if uwp['Size'] in ['0']:
        return True


def getIsBarren(uwp):
    if uwp['Population'] in ['0']:
        return True


def getIsDesert(uwp):
    if uwp['Atmosphere'] not in ['0', '1'] and uwp['Hydrosphere'] == '0':
        return True


def getIsFluidOcean(uwp):
    if uwp['Atmosphere'] in ['A', 'B', 'C', 'D', 'E', 'F'] and uwp['Hydrosphere'] not in ['0']:
        return True


def getIsGarden(uwp):
    if uwp['Atmosphere'] in ['5', '6', '8']\
            and uwp['Hydrosphere'] in ['4', '5', '6', '7', '8', '9']\
            and uwp['Population'] in ['4', '5', '6', '7', '8']:
        return True


def getIsHighPopulation(uwp):
    if uwp['Population'] in ['9', 'A']:
        return True


def getIsHighTechnology(uwp):
    if uwp['Technology'] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B']:
        return True


def getIsIceCapped(uwp):
    if uwp['Atmosphere'] in ['0', '1'] and uwp['Hydrosphere'] not in ['0']:
        return True


def getIsIndustrial(uwp):
    if uwp['Atmosphere'] in ['0', '1', '2', '4', '7', '9'] and uwp['Population'] in ['9', 'A']:
        return True


def getIsLowPopulation(uwp):
    if uwp['Population'] in ['1', '2', '3']:
        return True


def getIsLowTechnology(uwp):
    if uwp['Technology'] in ['0', '1', '2', '3', '4', '5'] and uwp['Population'] not in ['0']:
        return True


def getIsNonAgricultural(uwp):
    if uwp['Atmosphere'] in ['0', '1', '2']\
            and uwp['Hydrosphere'] in ['0', '1', '2']\
            and uwp['Population'] in ['6', '7', '8', '9', 'A']:
        return True


def getIsNonIndustrial(uwp):
    if uwp['Population'] in ['4', '5', '6']:
        return True


def getIsPoor(uwp):
    if uwp['Atmosphere'] in ['2', '3', '4', '5']\
            and uwp['Hydrosphere'] in ['0', '1', '2', '3']:
        return True


def getIsRich(uwp):
    if uwp['Atmosphere'] in ['6', '8']\
            and uwp['Population'] in ['6', '7', '8']:
        return True


def getIsWaterWorld(uwp):
    if uwp['Hydrosphere'] in ['A']:
        return True


def getIsVacuum(uwp):
    if uwp['Atmosphere'] in ['0']:
        return True


TRADE_CODES = [
    {'Checker': getIsAgricultural, 'Code': 'Ag'},
    {'Checker': getIsAsteroid, 'Code': 'As'},
    {'Checker': getIsBarren, 'Code': 'Ba'},
    {'Checker': getIsDesert, 'Code': 'De'},
    {'Checker': getIsFluidOcean, 'Code': 'Fl'},
    {'Checker': getIsGarden, 'Code': 'Ga'},
    {'Checker': getIsHighPopulation, 'Code': 'Hi'},
    {'Checker': getIsHighTechnology, 'Code': 'Ht'},
    {'Checker': getIsIceCapped, 'Code': 'Ic'},
    {'Checker': getIsIndustrial, 'Code': 'In'},
    {'Checker': getIsLowPopulation, 'Code': 'Lo'},
    {'Checker': getIsLowTechnology, 'Code': 'Lt'},
    {'Checker': getIsNonAgricultural, 'Code': 'Na'},
    {'Checker': getIsNonIndustrial, 'Code': 'Ni'},
    {'Checker': getIsPoor, 'Code': 'Po'},
    {'Checker': getIsRich, 'Code': 'Ri'},
    {'Checker': getIsWaterWorld, 'Code': 'Wa'},
    {'Checker': getIsVacuum, 'Code': 'Va'}
]


def generateTradeCodes(uwp):
    tradeCodes = ""
    for tradeCode in TRADE_CODES:
        if tradeCode['Checker'](uwp):
            tradeCodes += tradeCode['Code']
            tradeCodes += ' '
    if len(tradeCodes) < 16:
        for i in range(16 - len(tradeCodes)):
            tradeCodes += ' '
    return tradeCodes


def generateZone(uwp):
    return ' '

def generatePopulationMultiplier(uwp):
    if uwp['Population'] in ['0']:
        return '0'
    mult = dice.roll(2, 6) - 2
    if mult < 1:
        mult = 1
    if mult > 9:
        mult = 9
    return str(mult)

def generateBelts(uwp):
    belt = False
    belts = 0
    if uwp['Size'] in ['0']:
        belt = True
    if dice.roll(2, 6) > 3:
        belt = True
    if belt:
        belts = dice.roll(1, 6) - 3
        if belts < 1:
            belts = 1
    return str(belts)

def generateGasGiants(uwp):
    giants = 0
    if dice.roll(2, 6) > 4:
        giants = dice.roll(1, 6) - 2
        if giants < 1:
            giants = 1
    return str(giants)

def generateStars(uwp):
    '''
    From TNE
    :param uwp:
    :return:
    '''
    roll = dice.roll(2, 6)
    stars = []
    numStars = 1
    if roll < 8:
        numStars = 2
    if roll == 12:
        numStars = 3

    typeRoll = dice.roll(2,6)
    if uwp['Atmosphere'] in ['4', '5', '6', '7', '8', '9']\
            or uwp['Population'] in ['8', '9', 'A']:
        typeRoll += 5
    type = ['X', 'X', 'A', 'M', 'M', 'M', 'M', 'M', 'K', 'G', 'G', 'F', 'F', 'F', 'F', 'F', 'F', 'F'][typeRoll]
    classRoll = dice.roll(2, 6)
    if classRoll == 4 and type == 'M':
        classRoll = 5
    luminosityClass = ['X', 'X', 'II', 'III', 'IV', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V'][classRoll]
    dec = dice.roll(1, 10) - 1
    dec = sanitiseDec(dec, type, luminosityClass)
    stars.append(type+str(dec)+luminosityClass)

    for i in range(numStars-1):
        stars.append(generateCompanion(typeRoll, classRoll))

    starString = ""
    for star in stars:
        starString += star + ' '
    return starString

def sanitiseDec(dec, type, luminosityClass):
    if type == 'K' and luminosityClass == 'IV' and dec > 4:
        return dec - 5
    if type == 'O' and dec < 5:
        return dec + 5
    return dec

def generateCompanion(typeRoll, classRoll):
    typeRoll = typeRoll + dice.roll(2, 6)
    classRoll = classRoll + dice.roll(2, 6)

    if typeRoll < 5:
        type = 'A'
    elif typeRoll < 7:
        type = 'F'
    elif typeRoll < 9:
        type = 'G'
    elif typeRoll < 11:
        type = 'K'
    else:
        type = 'M'

    if classRoll < 5:
        luminosityClass = 'II'
    elif classRoll < 6:
        luminosityClass = 'III'
    elif classRoll < 7:
        luminosityClass = 'IV'
    elif classRoll < 14:
        luminosityClass = 'V'
    elif dice.roll(1, 6) < 3:
        luminosityClass = 'V'
    else:
        luminosityClass = 'D'

    dec = dice.roll(1, 10) - 1
    dec = sanitiseDec(dec, type, luminosityClass)

    return type + str(dec) + luminosityClass
