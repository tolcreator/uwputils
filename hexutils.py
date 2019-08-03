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
