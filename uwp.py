import dice

FIELDS = ['Starport', 'Size', 'Atmosphere', 'Hydrosphere', 'Population', 'Government', 'Law', 'Technology']

HEXES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
         'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
         'U', 'V', 'W', 'X', 'Y', 'Z']

NUMBERS = {
    '0': 0,  '1': 1,  '2': 2,  '3': 3,  '4': 4,  '5': 5,  '6': 6,  '7': 7,  '8': 8,  '9': 9,
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19,
    'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29,
    'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35
}


def sanityCheck(suwp):
    """
    Check that string suwp is in the format:
    X000000-0
    :param suwp:
    :return:
    """
    # Gotta be the right length
    if len(suwp) != 9:
        raise ValueError("Wrong Length")

    # Gotta have that dash
    if suwp[7] not in ['-']:
        raise ValueError("No Dash")

    starport = suwp[0]
    size = suwp[1]
    atmosphere = suwp[2]
    hydrosphere = suwp[3]
    population = suwp[4]
    government = suwp[5]
    law = suwp[6]
    tech = suwp[8]

    if starport not in ['A', 'B', 'C', 'D', 'E', 'X']:
        raise ValueError("Invalid Starport")
    if size not in HEXES[:11]:
        raise ValueError("Invalid Size")
    if atmosphere not in HEXES[:16]:
        raise ValueError("Invalid Atmosphere")
    if hydrosphere not in HEXES[:11]:
        raise ValueError("Invalid Hydrosphere")
    if population not in HEXES[:11]:
        raise ValueError("Invalid Population")
    # The rest of these can be arbitrarily high
    if government not in HEXES:
        raise ValueError("Invalid Government")
    if law not in HEXES:
        raise ValueError("Invalid Law")
    if tech not in HEXES:
        raise ValueError("Invalid Technology")


def strToUwp(suwp):
    """
    :param suwp: A string with proper UWP format
    :return: A dictionary of the UWP values with keys from FIELDS
    """
    try:
        sanityCheck(suwp)
    except ValueError as e:
        print "UWP error! %s" % str(e)
        print suwp
        return None
    suwp = suwp.replace('-', '')
    uwp = {}
    for i in range(len(suwp)):
        uwp[FIELDS[i]] = suwp[i]
    return uwp

def uwpToStr(uwp):
    ret = ""
    ret += uwp['Starport']
    ret += uwp['Size']
    ret += uwp['Atmosphere']
    ret += uwp['Hydrosphere']
    ret += uwp['Population']
    ret += uwp['Government']
    ret += uwp['Law']
    ret += '-'
    ret += uwp['Technology']
    return ret

def generate():
    """
    Generates a new UWP
    :return: A dictionary of the new UWP with keys from FIELDS
    """
    uwp = {}
    uwp['Size'] = generateSize()
    uwp['Atmosphere'] = generateAtmosphere(uwp)
    uwp['Hydrosphere'] = generateHydrosphere(uwp)
    uwp['Population'] = generatePopulation(uwp)
    uwp['Government'] = generateGovernment(uwp)
    uwp['Law'] = generateLaw(uwp)
    uwp['Starport'] = generateStarport(uwp)
    uwp['Technology'] = generateTechnology(uwp)
    return uwp


def generateSize():
    roll = dice.roll(2, 6) - 2
    return HEXES[roll]


def generateAtmosphere(uwp, spaceOpera=True):
    size = NUMBERS[uwp['Size']]
    roll = dice.roll(2, 6) + size - 7
    if roll < 0:
        roll = 0

    if spaceOpera:
        if size in [0, 1, 2]:
            return '0'
        if size in [3, 4]:
            if roll in [0, 1, 2]:
                return '0'
            elif roll in [3, 4, 5]:
                return '1'
            else:
                return 'A'

    return HEXES[roll]


def generateHydrosphere(uwp, spaceOpera=True):
    size = NUMBERS[uwp['Size']]

    if size in [0, 1]:
        return '0'

    atmosphere = NUMBERS[uwp['Atmosphere']]
    roll = dice.roll(2, 6) + size - 7

    dm = 0
    if atmosphere in [0, 1, 10, 11, 12]:
        dm = -4

    if spaceOpera:
        if size in [3,4] and atmosphere in [10]:
            dm += -6
        if atmosphere in [0, 1]:
            dm += -6
        if atmosphere in [2, 3, 11, 12]:
            dm += -4

    roll += dm
    if roll < 0:
        roll = 0
    if roll > 10:
        roll = 10
    return HEXES[roll]


def generatePopulation(uwp, hard=True):
    size = NUMBERS[uwp['Size']]
    atmosphere = NUMBERS[uwp['Atmosphere']]

    roll = dice.roll(2, 6) - 2
    dm = 0

    if hard:
        if size in [0, 1, 2, 10]:
            dm += -1
        if atmosphere in [5, 6, 8]:
            dm += 1
        else:
            dm += -1

    roll += dm
    if roll < 0:
        roll = 0
    return HEXES[roll]


def generateGovernment(uwp):
    population = NUMBERS[uwp['Population']]

    if population == 0:
        return '0'

    roll = dice.roll(2, 6) + population - 7
    if roll < 0:
        roll = 0
    return HEXES[roll]


def generateLaw(uwp):
    population = NUMBERS[uwp['Population']]
    government = NUMBERS[uwp['Government']]

    if population == 0:
        return '0'

    roll = dice.roll(2, 6) + government - 7
    if roll < 0:
        roll = 0
    return HEXES[roll]


def generateStarport(uwp, hard=False, mgt2e=True):
    population = NUMBERS[uwp['Population']]

    if population == 0:
        return 'X'

    roll = dice.roll(2, 6)
    dm = 0

    if hard:
        dm = population - 7
    if mgt2e:
        if population in [8, 9]:
            dm = 1
        elif population > 9:
            dm = 2
        elif population in [3, 4]:
            dm = -1
        elif population in [1, 2]:
            dm = -2

    roll += dm
    if roll > 10:
        return 'A'
    if roll > 8:
        return 'B'
    if roll > 6:
        return 'C'
    if roll > 4:
        return 'D'
    if roll > 2:
        return 'E'
    return 'X'


def generateTechnology(uwp, max=12):
    if uwp['Population'] in ['0']:
        return '0'
    dm = 0
    dm += {'A': 6, 'B': 4, 'C': 2}.get(uwp['Starport'], 0)
    dm += {'0': 2, '1': 2, '2': 1, '3': 1, '4': 1}.get(uwp['Size'], 0)
    if uwp['Atmosphere'] in ['0', '1', '2', '3', 'A', 'B', 'C', 'D', 'E', 'F']:
        dm += 1
    dm += {'A': 2, '9': 1, '0': 1}.get(uwp['Hydrosphere'], 0)
    if uwp['Population'] in ['1', '2', '3', '4', '5', '9']:
        dm += 1
    if uwp['Population'] in ['A']:
        dm += 2
    dm += {'0': 1, '5': 1, '7': 2, 'D': -2, 'E': -2}.get(uwp['Government'], 0)

    roll = dice.roll(1, 6)
    roll += dm
    if roll < 0:
        roll = 0
    if roll > max:
        if dm+1 > max:
            roll = dm+1
        else:
            roll = max
    return HEXES[roll]
