import sector
import traderoute
import sys
import hexutils

def main(filename, sourceHex, destHex):
    systems = sector.readSystemsFromFile(filename)
    systems = sector.stripNonSystems(systems)

    source = None
    dest = None

    for system in systems:
        if system['hex'] == sourceHex:
            source = system
        if system['hex'] == destHex:
            dest = system

    if source and dest:
        map = hexutils.constructDistanceMap(systems)
        route = traderoute.getTradeRoute(source, dest, systems, map, 2)
        if route:
            print "btn: " + str(route['btn']) + " len: " + str(len(route['path']))
            for node in route['path']:
                print node['name'] + ' ' + node['hex'] + ' ' + node['uwpString']
        else:
            print "No viable route found."
    else:
        print "Could not find %s %s" % (sourceHex, destHex)

if __name__ == "__main__":
    filename = sys.argv[1]
    source = sys.argv[2]
    dest = sys.argv[3]
    main(filename, source, dest)
