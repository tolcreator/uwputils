import dice
import uwp
import trade
import stellar

SUBSECTORS = [
    ['A', 'B', 'C', 'D'],
    ['E', 'F', 'G', 'H'],
    ['I', 'J', 'K', 'L'],
    ['M', 'N', 'O', 'P']
]


def parseLine(line):
    line = line.strip()
    if getIsBlank(line):
        return {'type': 'blank'}
    if getIsComment(line):
        return {'type': 'comment', 'comment': line}

    # Make a special case where only the hex number is provided.
    if len(line) == 4:
        hexNumber = line[:4]
        name = ""
    else:
        name = line[:13].strip()
        hexNumber = line[14:18]
    uwpString = line[19:28]
    base = line[29:30]
    trade = line[31:47]
    zone = line[48:49]
    p = line[51:52]
    b = line[52:53]
    g = line[53:54]
    allegiance = line[55:57]
    stellar = line[58:]

    return {
        'type': 'system',
        'name': name,
        'hex': hexNumber,
        'uwpString': uwpString,
        'base': base,
        'trade': trade,
        'zone': zone,
        'p': p,
        'b': b,
        'g': g,
        'allegiance': allegiance,
        'stellar': stellar,
    }


def getIsBlank(line):
    line = line.strip()
    if not line:
        return True
    return False


def getIsComment(line):
    if line[0] in ['#']:
        return True
    return False


def systemToString(system):
    if system['type'] == 'blank':
        return ""
    if system['type'] == 'comment':
        return system['comment']
    out = ""
    out += system['name'].ljust(13) + ' '
    out += system['hex'] + ' '
    out += system['uwpString'] + ' '
    out += system['base'] + ' '
    out += system['trade'].ljust(16) + ' '
    out += system['zone'] + '  '
    out += system['p'] + system['b'] + system['g'] + ' '
    out += system['allegiance'] + ' '
    out += system['stellar']
    return out


def autocomplete(filename, write=False, update=False, show=False):
    systems = []
    with open(filename, 'r') as file:
        for line in file:
            parsed = parseLine(line)
            if parsed:
                systems.append(parsed)

    completedSystems = []
    for system in systems:
        if system['type'] == 'system':
            completed = autocompleteSystem(system, update)
        else:
            completed = system
        completedSystems.append(completed)

    if show:
        for system in completedSystems:
            print systemToString(system)

    if write:
        with open(filename, 'w') as file:
            for system in completedSystems:
                file.write(systemToString(system) + '\n')

def autocompleteSystem(system, update):
    # All about names
    if not system['hex']:
        raise ValueError
    if not system['name']:
        system['name'] = generateNameFromHex(system['hex'])

    # All about UWP
    if not system['uwpString']:
        s = uwp.generate()
        system['uwpString'] = uwp.uwpToStr(s)
    else:
        s = uwp.strToUwp(system['uwpString'])

    if not system['base'] or update:
        system['base'] = generateBase(s)
    if not system['trade'] or update:
        system['trade'] = trade.generate(s)
    if not system['zone'] or update:
        system['zone'] = generateZone(s)
    if not system['p'] or update:
        system['p'] = generatePopulationMultiplier(s)
    if not system['b'] or update:
        system['b'] = generateBelts(s)
    if not system['g'] or update:
        system['g'] = generateGasGiants(s)
    if not system['allegiance'] or update:
        system['allegiance'] = 'Na'
    if not system['stellar'] or update:
        system['stellar'] = stellar.generate(s)
    return system


def generateNameFromHex(hexNumber):
    sanityCheckHexNumber(hexNumber)

    x = int(hexNumber[:2])
    y = int(hexNumber[2:])

    subsector = getSubsectorFromCoordinates(x, y)
    return subsector + hexNumber


def sanityCheckHexNumber(hexNumber):
    if len(hexNumber) != 4:
        raise ValueError
    x = int(hexNumber[:2])
    y = int(hexNumber[2:])
    if x < 0 or x > 32:
        raise ValueError
    if y < 0 or y > 40:
        raise ValueError


def getSubsectorFromCoordinates(x, y):
    if x < 9:
        column = 0
    elif x < 17:
        column = 1
    elif x < 25:
        column = 2
    else:
        column = 3
    if y < 11:
        row = 0
    elif y < 21:
        row = 1
    elif y < 31:
        row = 2
    else:
        row = 3
    return SUBSECTORS[row][column]


def generateBase(uwp):
    naval = False
    scout = False
    pirate = False

    roll = dice.roll(2, 6)
    if uwp['Starport'] in ['A', 'B'] and roll > 7:
        naval = True

    roll = dice.roll(2, 6)
    dm = {'C': -1, 'B': -2, 'A': -3}.get(uwp['Starport'], 0)
    roll += dm
    if uwp['Starport'] in ['A', 'B', 'C', 'D'] and roll > 6:
        scout = True

    roll = dice.roll(2, 6)
    if uwp['Starport'] not in ['A'] and not naval and roll == 12:
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
