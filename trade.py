# Works off the dictionaries as generated in uwp.py

def getIsAgricultural(uwp):
    if uwp['Atmosphere'] in ['4', '5', '6', '7', '8', '9'] \
            and uwp['Hydrosphere'] in ['4', '5', '6', '7', '8'] \
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


def getIsGarden(uwp, version="Mongoose"):
    if version == "Cepheus":
        if uwp['Atmosphere'] in ['5', '6', '8'] \
                and uwp['Hydrosphere'] in ['4', '5', '6', '7', '8', '9'] \
                and uwp['Population'] in ['4', '5', '6', '7', '8']:
            return True

    # Default = Mongoose
    if uwp['Size'] in ['5', '6', '7', '8', '9', 'A'] \
            and uwp['Atmosphere'] in ['4', '5', '6', '7', '8', '9'] \
            and uwp['Hydrosphere'] in ['4', '5', '6', '7', '8', '9']:
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
    if uwp['Atmosphere'] in ['0', '1', '2'] \
            and uwp['Hydrosphere'] in ['0', '1', '2'] \
            and uwp['Population'] in ['6', '7', '8', '9', 'A']:
        return True


def getIsNonIndustrial(uwp):
    if uwp['Population'] in ['4', '5', '6']:
        return True


def getIsPoor(uwp):
    if uwp['Atmosphere'] in ['2', '3', '4', '5'] \
            and uwp['Hydrosphere'] in ['0', '1', '2', '3']:
        return True


def getIsRich(uwp):
    if uwp['Atmosphere'] in ['6', '8'] \
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


def generate(uwp):
    trade = ""
    for code in TRADE_CODES:
        if code['Checker'](uwp):
            trade += code['Code']
            trade += ' '
    return trade
