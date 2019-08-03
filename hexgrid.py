import hexutils
from PIL import Image, ImageDraw, ImageFont

DRAFT_SCHEME = {
    'background': '#faecd7',
    'hexes': '#4da9a3',
    'subsectors': '#b93533'
}


def drawGrid(draw, x, y, hexSize, scheme, blank):
    for row in range(0, y):
        for column in range(0, x):
            drawHex(draw, column, row, hexSize, scheme, blank)


def drawHex(draw, x, y, hexSize, scheme, blank=False):
    colour = scheme['hexes']
    # Draw the hex outline
    origin = hexutils.getPosition(x, y, hexSize)
    vertices = hexutils.getVertices(hexSize, origin)
    draw.line(vertices, fill=colour, width=2)
    # Write the hex coordinates
    if not blank:
        fnt = ImageFont.truetype('Arial.ttf', size=int(hexSize / 10))
        coords = "%02d%02d" % (x+1, y+1)
        size = fnt.getsize(coords)
        position = ((hexutils.widthBlock(hexSize) * 2) - int(size[0]/2) + origin[0], origin[1] + 3)
        draw.text(position, coords, font=fnt, fill=colour)


def drawSubsectorGrid(draw, size, subsectors, hexSize, scheme):
    colour = scheme['subsectors']
    xcoord = 0
    ycoord = 0
    for x in range(1, subsectors):
        xcoord += 8 * 3 * hexutils.widthBlock(hexSize)
        xactual = int(xcoord + (0.5 * hexutils.widthBlock(hexSize)))
        draw.line([(xactual, 0), (xactual, size[1])], fill=colour, width=3)
    for y in range(1, subsectors):
        ycoord += 10 * 2 * hexutils.heightBlock(hexSize)
        yactual = int(ycoord + (0.5 * hexutils.heightBlock(hexSize)))
        draw.line([(0, yactual), (size[0], yactual)], fill=colour, width=3)


def drawSubsector(draw, hexSize, scheme, blank):
    drawGrid(draw, 8, 10, hexSize, scheme, blank)


def drawSector(draw, hexSize, scheme, blank):
    size = hexutils.getImageSize(32, 40, hexSize)
    drawGrid(draw, 32, 40, hexSize, scheme, blank)
    if not blank:
        drawSubsectorGrid(draw, size, 4, hexSize, scheme)


def getSubsectorCanvas(hexSize):
    size = hexutils.getImageSize(8, 10, hexSize)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    return draw, img


def getSectorCanvas(hexSize):
    size = hexutils.getImageSize(32, 40, hexSize)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    return draw, img


def createSectorGrid(filename, hexSize=256, blank=False):
    draw, img = getSectorCanvas(hexSize)
    drawSector(draw, hexSize, DRAFT_SCHEME, blank)
    img.save(filename)


def createSubsectorGrid(filename, hexSize=256, blank=False):
    draw, img = getSubsectorCanvas(hexSize)
    drawSubsector(draw, hexSize, DRAFT_SCHEME, blank)
    img.save(filename)