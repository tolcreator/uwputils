import hexgrid
import hexutils
import uwp
import sector
import trade
import traderoute
import political
from PIL import ImageFont
import math

DRAFT_SCHEME = {
    'worlds': {
        'asteroid': {'outline': '#000000', 'fill': '#808080'},
        'vacuum': {'outline': '#000000', 'fill': '#808080'},
        'garden': {'outline': '#000000', 'fill': '#87a21a'},
        'desert': {'outline': '#000000', 'fill': '#b6945d'},
        'water': {'outline': '#000000', 'fill': '#0040cc'},
        'fluidocean': {'outline': '#000000', 'fill': '#b65da6'},
        'ocean': {'outline': '#000000', 'fill': '#009ccc'},
        'ice': {'outline': '#000000', 'fill': '#ffffff'},
    },
    'name': {
        'colour': '#000000',
        'hipop': {
            'font': 'Comic Sans MS Bold.ttf',
            'size': 6
        },
        'regular': {
            'font': 'Comic Sans MS Bold.ttf',
            'size': 8
        }
    },
    'starport' : {'colour': '#000000', 'font': 'Comic Sans MS Bold.ttf', 'size': 6},
    'uwp': {'colour': '#000000', 'font': 'Arial.ttf', 'size': 8},
    'gasgiant': {'colour': '#000000'},
    'base': {'colour': '#000000'},
    'demographics': {'fill': '#000000', 'outline': '#ffffff'}
}


def drawSystem(draw, origin, system, hexSize, scheme):
    s = uwp.strToUwp(system['uwpString'])
    drawDot(draw, origin, s, hexSize, scheme)
    drawName(draw, origin, system['name'], s['Population'], hexSize, scheme)
    drawStarport(draw, origin, s['Starport'], hexSize, scheme)
    drawUwp(draw, origin, system['uwpString'], hexSize, scheme)
    drawGasGiant(draw, origin, system['g'], hexSize, scheme)
    drawBase(draw, origin, system['base'], hexSize, scheme)

def drawDot(draw, origin, s, hexSize, scheme):
    # Draw Dot
    coords = hexutils.getCenter(origin, hexSize)
    offset = int(hexSize / 10)
    box = [coords[0] - offset, coords[1] - offset, coords[0] + offset, coords[1] + offset]
    if s['Size'] in ['0']:
        dotScheme = scheme['worlds']['asteroid']
    elif s['Hydrosphere'] in ['0']:
        if s['Atmosphere'] in ['0']:
            dotScheme = scheme['worlds']['vacuum']
        else:
            dotScheme = scheme['worlds']['desert']
    elif s['Atmosphere'] in ['5', '6', '8']:
        if s['Hydrosphere'] in ['A']:
            dotScheme = scheme['worlds']['ocean']
        else:
            dotScheme = scheme['worlds']['garden']
    elif s['Atmosphere'] in ['0', '1']:
        dotScheme = scheme['worlds']['ice']
    elif s['Atmosphere'] in ['2', '3', '4', '7', '9']:
        dotScheme = scheme['worlds']['water']
    else:
        dotScheme = scheme['worlds']['fluidocean']
    draw.ellipse(box, fill=dotScheme['fill'], outline=dotScheme['outline'], width=2)


def drawName(draw, origin, name, population, hexSize, scheme):
    coords = hexutils.getCenter(origin, hexSize)
    underline = False
    if population in ['9', 'A']:
        typeface = scheme['name']['hipop']['font']
        fontsize = scheme['name']['hipop']['size']
        output = name.upper()
        underline = True
    else:
        typeface  = scheme['name']['regular']['font']
        fontsize = scheme['name']['regular']['size']
        output = name
    fnt = ImageFont.truetype(typeface, size=int(hexSize / fontsize))
    size = fnt.getsize(output)
    xoff = int(size[0]/2)
    yoff = int(2*hexSize / 7)
    coords = (coords[0] - xoff, coords[1] + yoff)
    draw.text(coords, output, font=fnt, fill=scheme['name']['colour'])
    if underline:
        line = [
            (coords[0], coords[1] + size[1] + int(hexSize / 100)),
            (coords[0] + size[0], coords[1] + size[1] + int(hexSize / 100))
        ]
        draw.line(line, fill=scheme['name']['colour'], width=int(hexSize / 50))


def drawStarport(draw, origin, starport, hexSize, scheme):
    coords = hexutils.getCenter(origin, hexSize)
    typeface = scheme['starport']['font']
    fontsize = scheme['starport']['size']
    fnt = ImageFont.truetype(typeface, size=int(hexSize / fontsize))
    size = fnt.getsize(starport)
    xoff = int(size[0]/2)
    yoff = size[1] + int(hexSize / 7)
    coords = (coords[0] - xoff, coords[1] - yoff)
    draw.text(coords, starport, font=fnt, fill=scheme['starport']['colour'])


def drawUwp(draw, origin, uwpString, hexSize, scheme):
    coords = hexutils.getCenter(origin, hexSize)
    typeface = scheme['uwp']['font']
    fontsize = scheme['uwp']['size']
    fnt = ImageFont.truetype(typeface, size=int(hexSize / fontsize))
    size = fnt.getsize(uwpString)
    xoff = int(size[0]/2)
    yoff = int(hexSize / 7)
    coords = (coords[0] - xoff, coords[1] + yoff)
    draw.text(coords, uwpString, font=fnt, fill=scheme['uwp']['colour'])


def drawGasGiant(draw, origin, giant, hexSize, scheme):
    if giant not in ['0', ' ']:
        coords = hexutils.getCenter(origin, hexSize)
        xoff = hexutils.widthBlock(hexSize)
        yoff = int(hexutils.heightBlock(hexSize) / 2)
        coords = (coords[0] + xoff, coords[1] - yoff)
        offset = int(hexSize / 25)
        box = [(coords[0] - offset, coords[1] - offset), (coords[0] + offset, coords[1] + offset)]
        draw.ellipse(box, fill=scheme['gasgiant']['colour'])


# Don't draw pirates!
def drawBase(draw, origin, base, hexSize, scheme):
    scout = False
    naval = False
    if base in ['S', 'A', 'G']:
        scout = True
    if base in ['N', 'A']:
        naval = True
    if scout:
        drawScoutBase(draw, origin, hexSize, scheme)
    if naval:
        drawNavalBase(draw, origin, hexSize, scheme)


def drawScoutBase(draw, origin, hexSize, scheme):
    coords = hexutils.getCenter(origin, hexSize)
    xoff = hexutils.widthBlock(hexSize)
    coords = (coords[0] - xoff, coords[1])
    height = hexSize / 12
    xoff = int(height / math.sqrt(3))
    yoff = int(height)
    vertices = [
        (coords[0], coords[1]),
        (coords[0] - xoff, coords[1] + yoff),
        (coords[0] + xoff, coords[1] + yoff),
        (coords[0], coords[1])
    ]
    draw.polygon(vertices, fill=scheme['base']['colour'])


def drawNavalBase(draw, origin, hexSize, scheme):
    coords = hexutils.getCenter(origin, hexSize)
    xoff = hexutils.widthBlock(hexSize)
    yoff = int(hexutils.heightBlock(hexSize) / 2)
    coords = (coords[0] - xoff, coords[1] - yoff)
    height = hexSize / 12
    pentagon = []
    for n in range(0, 5):
        x = height * math.cos(math.radians(270+n*72))
        y = height * math.sin(math.radians(270+n*72))
        pentagon.append((int(x), int(y)))
    vertices = [
        coords[0] + pentagon[0][0], coords[1] + pentagon[0][1],
        coords[0] + pentagon[2][0], coords[1] + pentagon[2][1],
        coords[0] + pentagon[4][0], coords[1] + pentagon[4][1],
        coords[0] + pentagon[1][0], coords[1] + pentagon[1][1],
        coords[0] + pentagon[3][0], coords[1] + pentagon[3][1],
        coords[0] + pentagon[0][0], coords[1] + pentagon[0][1],
    ]
    draw.polygon(vertices, fill=scheme['base']['colour'])
    height = int(height/4)+1
    box = [(coords[0] - height, coords[1] - height), (coords[0] + height, coords[1] + height)]
    draw.ellipse(box, fill=scheme['base']['colour'])


def drawSystemDemographics(draw, origin, system, hexSize, colour):
    coords = hexutils.getCenter(origin, hexSize)
    s = uwp.strToUwp(system['uwpString'])
    circleTable = {
        '0': {'base': 0, 'max': 0},
        '1': {'base': 0.015125, 'max': 0.03125},
        '2': {'base': 0.03125, 'max': 0.0625},
        '3': {'base': 0.0625, 'max': 0.125},
        '4': {'base': 0.125, 'max': 0.25},
        '5': {'base': 0.25, 'max': 0.5},
        '6': {'base': 0.5, 'max': 1},
        '7': {'base': 1, 'max': 2},
        '8': {'base': 2, 'max': 4},
        '9': {'base': 4, 'max': 8},
        'A': {'base': 8, 'max': 16},
    }
    base = int(hexSize * circleTable[s['Population']]['base'])
    if system['p'] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        max = int(hexSize * circleTable[s['Population']]['max'])
        range = max - base
        mod = int(int(system['p']) * range/10)
    else:
        mod = 0
    radius = int((base + mod) / 2)
    box = [(coords[0] - radius, coords[1] - radius), (coords[0] + radius, coords[1] + radius)]
    draw.ellipse(box, fill=colour, outline='#ffffff', width=int(radius/10))


def drawSystemEconomics(draw, origin, wtn, hexSize, colour):
    coords = hexutils.getCenter(origin, hexSize)
    # WTN is a whole non negative integer.
    circleTable = [
        0,
        0.09375,
        0.0625,
        0.1875,
        0.125,
        0.25,
        0.375,
        0.5,
        0.75,
        1,
        1.5,
        2,
        # Anything beyond here is probably impossible.
        3, 4, 6, 8, 12, 16
    ]
    radius = int(hexSize * circleTable[wtn])
    box = [(coords[0] - radius, coords[1] - radius), (coords[0] + radius, coords[1] + radius)]
    draw.ellipse(box, fill=colour, outline="#ffffff", width=int(radius / 10))

def drawSector(input, output, hexSize=256, scheme=DRAFT_SCHEME):
    systems = sector.readSystemsFromFile(input)
    draw, img = hexgrid.getSectorCanvas(hexSize)
    for system in (system for system in systems if system['type'] == 'system'):
        x, y = sector.getCoords(system)
        # x,y coords start from 1
        origin = hexutils.getPosition(x-1, y-1, hexSize)
        drawSystem(draw, origin, system, hexSize, scheme)
    img.save(output)


def drawDemographics(input, output, hexSize=256, scheme=DRAFT_SCHEME):
    systems = sector.readSystemsFromFile(input)
    politicalPalette = political.constructPalette(systems)
    demographics = []
    for system in systems:
        if system['type'] == 'system':
            s = uwp.strToUwp(system['uwpString'])
            demographic = (int(s['Population'], 16), int(system['p']))
            demographics.append({'demographics': demographic, 'system': system})
    demographics.sort(key = lambda i: i['demographics'][0], reverse=True)
    draw, img = hexgrid.getSectorCanvas(hexSize)
    for entry in demographics:
        system = entry['system']
        x, y = sector.getCoords(system)
        # x,y coords start from 1
        origin = hexutils.getPosition(x-1, y-1, hexSize)
        drawSystemDemographics(draw, origin, system, hexSize, politicalPalette[entry['system']['allegiance']])
    img.save(output)


def drawWorldTradeNumber(input, output, hexSize=256, scheme=DRAFT_SCHEME):
    systems = sector.readSystemsFromFile(input)
    politicalPalette = political.constructPalette(systems)
    economics = []
    for system in systems:
        if system['type'] == 'system':
            wtn = trade.getWorldTradeNumber(uwp.strToUwp(system['uwpString']))
            economics.append({'wtn': wtn, 'system': system})
    economics.sort(key = lambda i: i['wtn'], reverse=True)
    draw, img = hexgrid.getSectorCanvas(hexSize)
    for entry in economics:
        system = entry['system']
        x, y = sector.getCoords(system)
        # x,y coords start from 1
        origin = hexutils.getPosition(x-1, y-1, hexSize)
        drawSystemEconomics(draw, origin, entry['wtn'], hexSize, politicalPalette[entry['system']['allegiance']])
    img.save(output)


def drawTradeRoutes(input, output, hexSize=256, scheme=DRAFT_SCHEME):
    routes = traderoute.readFromFile(input)

    draw, img = hexgrid.getSectorCanvas(hexSize)
    routes.sort(key = lambda i: i['btn'])
    for route in routes:
        drawTradeRoute(draw, route, hexSize, scheme)
    img.save(output)


def drawTradeRoute(draw, route, hexSize, scheme):
    colour = traderoute.getColourForBtn(int(route['btn']))
    size = traderoute.getSizeForBtn(int(route['btn']))

    for i in range(0, len(route['nodes'])-1):
        source = sector.getCoordsFromHex(route['nodes'][i])
        dest = sector.getCoordsFromHex(route['nodes'][i+1])
        s = hexutils.getCenter(hexutils.getPosition(source[0]-1, source[1]-1, hexSize), hexSize)
        d = hexutils.getCenter(hexutils.getPosition(dest[0]-1, dest[1]-1, hexSize), hexSize)
        draw.line([s, d], fill=colour, width=size)



