import dice

def generate(uwp):
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
