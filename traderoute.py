import hexutils
import trade
import uwp

BTN_CUTOFF = 8


def getPathsFrom(src, dest, systems, pathfrom, paths, jumprange):
    space = list(systems)
    neighbours = hexutils.getNeighbours(src, space, jumprange)
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
                getPathsFrom(pot, dest, space, pathto, paths, jumprange)


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
        s = uwp.strToUwp(node['uwpString'])
        spm += trade.getPathStarportModifier(s['Starport'])
    return (dm + spm) * -1


def getPathDistance(path):
    distance = 0;
    last = path[0]
    for node in path[1:]:
        d = hexutils.calculateDistance(last['hex'], node['hex'])
        distance = distance + d
        last = node
    return distance


def getBestPath(src, dest, systems, jumprange=2):
    paths = []
    pathto = []

    space = list(systems)
    space.remove(src)
    getPathsFrom(src, dest, space, pathto, paths, jumprange)

    if paths:
        bestpath = paths[0]
        bestvalue = evaluatePath(paths[0])
        for path in paths[1:]:
            value = evaluatePath(path)
            if value > bestvalue:
                bestpath = path
                bestvalue = value
        return bestpath
    else:
        return None


def getTradeRoute(source, dest, systems):
    ubtn = trade.getUnmodifiedBilateralTradeNumber(source, dest)
    swtn = trade.getWorldTradeNumber(uwp.strToUwp(source['uwpString']))
    dwtn = trade.getWorldTradeNumber(uwp.strToUwp(dest['uwpString']))

    if ubtn < BTN_CUTOFF:
        return None

    path = getBestPath(source, dest, systems, 2)
    if path:
        btn = ubtn + evaluatePath(path)
    else:
        return None

    jr = min(swtn, dwtn)
    if btn > (jr + 5):
        btn = jr + 5

    return {'btn': btn, 'path': path}

