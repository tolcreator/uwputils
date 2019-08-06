import math


def heightBlock(hexSize):
    """
    A hex is 2 heightblocks high
    :param hexSize:
    :return: the size of a hex height-block
    """
    return int(hexSize/2)


def widthBlock(hexSize):
    """
    A hex is 4 width blocks wide
    :param hexSize:
    :return: The size of a hex width-block
    """
    return int(hexSize/(math.sqrt(3) * 2))


def getImageSize(x, y, hexSize):
    """
    :param hexSize:
    :param x:
    :param y:
    :return: The size of image needed to bound the given hexes
    """
    xcoord = widthBlock(hexSize) * ((x*3)+1)
    ycoord = heightBlock(hexSize) * ((y*2)+1)
    return (xcoord, ycoord)


def getPosition(x, y, hexSize):
    """
    :param x: Hex column
    :param y: Hex row
    :param hexSize:
    :return: x,y coordinates of box that bounds the hex
    """
    xcoord = x * widthBlock(hexSize) * 3
    ycoord = y * heightBlock(hexSize) * 2
    if x % 2:
        ycoord += heightBlock(hexSize)
    return (xcoord, ycoord)


def getCenter(origin, hexSize):
    return (origin[0] + widthBlock(hexSize) * 2, origin[1] + heightBlock(hexSize))


def getVertices(hexSize, origin):
    vertices = []
    vertices.append((origin[0] +  widthBlock(hexSize),      origin[1]))
    vertices.append((origin[0] + (widthBlock(hexSize) * 3), origin[1]))
    vertices.append((origin[0] + (widthBlock(hexSize) * 4), origin[1] +  heightBlock(hexSize)))
    vertices.append((origin[0] + (widthBlock(hexSize) * 3), origin[1] + (heightBlock(hexSize) * 2)))
    vertices.append((origin[0] +  widthBlock(hexSize),      origin[1] + (heightBlock(hexSize) * 2)))
    vertices.append((origin[0],                             origin[1] +  heightBlock(hexSize)))
    vertices.append((origin[0] +  widthBlock(hexSize),      origin[1]))
    return vertices


def calculateDistance(src, dest):
    """
    get_dist( int x1, int y1, int x2, int y2 ) {
        int     dx, dy;
        y1 = y1 * 2; if( !(x1 % 2) ) y1++;
        y2 = y2 * 2; if( !(x2 % 2) ) y2++;
        dy = y2 - y1; if( dy < 1 ) dy = -dy;
        dx = x2 - x1; if( dx < 1 ) dx = -dx;
        if( dx > dy ) return dx;
        return (dx+dy)/2;
    }
    :param src: Source coordinates in format "02%d02%d" % (x, y)
    :param des: Destination coordinates in format "02%d02%d" % (x, y)
    :return: Distance between them.
    """

    return calculateDistanceInt(int(src[:2]), int(src[2:]), int(dest[:2]), int(dest[2:]))


def calculateDistanceInt(x1, y1, x2, y2):
    '''
    x1 -= 1
    y1 -= 1
    x2 -= 1
    y2 -= 1
    '''
    y1 = y1 * 2
    if not (x1 % 2):
        y1 = y1 + 1
    y2 = y2 * 2
    if not (x2 % 2):
        y2 = y2 + 1
    dy = y2 - y1
    if dy < 1:
        dy = dy * -1
    dx = x2 - x1
    if dx < 1:
        dx = dx * -1
    if dx > dy:
        return dx
    return (dx + dy) / 2


def getNeighbours(src, systems, jumprange):
    """
    Returns a list of systems that are neighbours of the given system.
    :param src: Source system
    :param systems: All available systems
    :param jumprange: Jump range to be considered "Neighbours"
    :return:
    """
    neighbours = []
    if 'coords' not in src:
        src['coords'] = (int(src['hex'][:2]), int(src['hex'][2:]))
    x1 = src['coords'][0]
    y1 = src['coords'][1]
    for dest in systems:
        if 'coords' not in dest:
            dest['coords'] = (int(dest['hex'][:2]), int(dest['hex'][2:]))
        x2 = dest['coords'][0]
        y2 = dest['coords'][1]
        if abs(x1 - x2) > jumprange + 1:
            continue
        if abs(y1 - y2) > jumprange + 1:
            continue
        d = calculateDistanceInt(x1, y1, x2, y2)
        if d <= jumprange and d > 0:
            neighbours.append(dest)
    return neighbours


def getNeighboursWithMap(source, systems, map, jumprange):
    neighbours = []
    for dest in systems:
        d = map[source['index']][dest['index']]
        if d and d <= jumprange:
            neighbours.append(dest)
    return neighbours


def constructDistanceMap(systems):
    map = []
    index = 0
    for system in systems:
        system['coords'] = (int(system['hex'][:2]), int(system['hex'][2:]))
        system['index'] = index
        index += 1
    for source in systems:
        x1 = source['coords'][0]
        y1 = source['coords'][1]
        entry = []
        for dest in systems:
            x2 = dest['coords'][0]
            y2 = dest['coords'][1]
            entry.append(calculateDistanceInt(x1, y1, x2, y2))
        map.append(entry)
    return map
