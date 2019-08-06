import hexutils
import trade
import uwp

BTN_CUTOFF = 8
JUMP_CUTOFF = 20
gIterations = 0

def getPathsFrom(src, dest, systems, pathfrom, paths, map, jumprange):
    global gIterations
    gIterations = gIterations + 1
    if len(pathfrom) > JUMP_CUTOFF:
        return
    space = list(systems)
    neighbours = hexutils.getNeighboursWithMap(src, space, map, jumprange)
    if neighbours:
        pathfrom.append(src)
        currentvalue = evaluatePath(pathfrom, partial=True)
        if (currentvalue + trade.getUnmodifiedBilateralTradeNumber(src, dest)) < BTN_CUTOFF:
            """ Cut off point: I don't care anymore """
            return

        if paths:
            bestvalue = getBestPathOf(paths)
            if currentvalue <= bestvalue:
                """ We're already on a wild goose chase """
                return

        if dest in neighbours:
            """ We're there """
            pathfrom.append(dest)
            paths.append(pathfrom)
        else:
            neighbours.sort(key=lambda k: k['uwpString'][0])
            for pot in neighbours:
                space.remove(pot)
            for pot in neighbours:
                pathto = list(pathfrom)
                getPathsFrom(pot, dest, space, pathto, paths, map, jumprange)


def getBestPathOf(paths):
    bestvalue = -100
    if paths:
        for path in paths:
            value = evaluatePath(path)
            if value > bestvalue:
                bestvalue = value
    return bestvalue


def evaluatePath(path, partial=False):
    distance = getPathDistance(path)
    dm = trade.getTradeDistanceModifier(distance)
    spm = 0
    if partial:
        toevaluate = path[1:]
    else:
        toevaluate = path[1:-1]
    for node in toevaluate:
        spm += trade.getPathStarportModifier(node['uwpString'][0])
    return (dm + spm) * -1


def getPathDistance(path):
    distance = 0;
    last = path[0]
    for node in path[1:]:
        d = hexutils.calculateDistance(last['hex'], node['hex'])
        distance = distance + d
        last = node
    return distance


def getBestPath(src, dest, systems, map, jumprange):
    global gIterations
    paths = []
    pathto = []

    space = list(systems)
    space.remove(src)
    gIterations = 0
    getPathsFrom(src, dest, space, pathto, paths, map, jumprange)
    print gIterations
    if paths:
        bestpath = paths[0]
        bestvalue = evaluatePath(paths[0])
        for path in paths[1:]:
            value = evaluatePath(path)
            if value > bestvalue:
                bestpath = path
                bestvalue = value
            if value == bestvalue:
                if len(path) < len(bestpath):
                    bestpath = path
        return bestpath
    else:
        return None


def getTradeRoute(source, dest, systems, map, jumprange=2):
    source['wtn'] = trade.getWorldTradeNumber(uwp.strToUwp(source['uwpString']))
    dest['wtn'] = trade.getWorldTradeNumber(uwp.strToUwp(dest['uwpString']))
    ubtn = trade.getUnmodifiedBilateralTradeNumber(source, dest)

    if ubtn < BTN_CUTOFF:
        return None

    path = getBestPath(source, dest, systems, map, jumprange)
    if path:
        btn = ubtn + evaluatePath(path)
    else:
        return None

    jr = min(source['wtn'], dest['wtn'])
    if btn > (jr + 5):
        btn = jr + 5

    return {'btn': btn, 'path': path}


def readFromFile(filename):
    routes = []
    with open(filename, 'r') as file:
        for line in file:
            parsed = parseLine(line)
            if parsed:
                routes.append(parsed)
    return routes


def parseLine(line):
    route = {}
    items = line.split()
    route['btn'] = items[1]
    route['nodes'] = items[4:]
    return route


def getColourForBtn(btn):
    return {
        0: '#000000',
        1: '#080000',
        2: '#0c0000',
        3: '#100000',
        4: '#140000',
        5: '#180000',
        6: '#1c0000',
        7: '#200000',
        8: '#280000',
        9: '#300000',
        10: '#400000',
        11: '#600000',
        12: '#800000',
        13: '#c00000',
        14: '#ff0000',
        15: '#ff8000',
        16: '#d0d000',
        17: '#80a020',
        18: '#00a0a0',
        19: '#0000ff',
        20: '#a000a0',
    }.get(btn, '#ffffff')


def getSizeForBtn(btn):
    btns = {
        0: 1,
        1: 1,
        2: 1,
        3: 1,
        4: 1,
        5: 1,
        6: 2,
        7: 3,
        8: 3,
        9: 4,
        10: 4,
        11: 6,
        12: 8,
        13: 10,
        14: 12,
        15: 18,
        16: 24,
        17: 32,
        18: 40,
        19: 60,
        20: 80,
    }
    if btn not in btns:
        print btn
    return btns.get(btn, 1)

