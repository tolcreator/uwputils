import hexgrid
import hexutils
import uwp
import sector
from PIL import ImageFont

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
    }
}

def drawSystem(draw, origin, system, hexSize, scheme):
    s = uwp.strToUwp(system['uwpString'])
    drawDot(draw, origin, s, hexSize, scheme)
    drawName(draw, origin, system['name'], s['Population'], hexSize, scheme)


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

def drawSector(filename, hexSize, scheme=DRAFT_SCHEME):
    systems = sector.readSystemsFromFile(filename)
    draw, img = hexgrid.getSectorCanvas(hexSize)
    for system in (system for system in systems if system['type'] == 'system'):
        x, y = sector.getCoords(system)
        # x,y coords start from 1
        origin = hexutils.getPosition(x-1, y-1, hexSize)
        drawSystem(draw, origin, system, hexSize, scheme)
    img.save('sector.png')



