#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 80
#define MAX_PATH_STRING_LENGTH 280
#define MAX_PATH_LENGTH 45
#define MAX_PATHS 4096
// Jump range of 4 with every system populated
#define MAX_NEIGHBOURS 60
// Change above if you change this.
#define MAX_JUMP_RANGE 4
#define BTN_CUTOFF 10

int gdebug = 0;

enum tradeCodes {
    Ag, As, Ba, De, Fl, Ga, Hi, Ht, Ic, In, Lo, Lt, Na, Ni, Po, Ri, Wa, Va
};

typedef struct StarSystem {
    int x;
    int y;
    char starport;
    char population;
    char techlevel;
    int numTrades;
    enum tradeCodes trades[5];
    int wtn;
    int ag;
    int likesag;
    int ni;
    int in;
} starSystem;

typedef struct Path {
    int numNodes;
    int length;
    int starportmods;
    int nodes[MAX_PATH_LENGTH];
} path;

typedef struct PathSet {
    int ubtn;
    int numpaths;
    int bestvalue;
    path paths[MAX_PATHS];
} pathSet;

int readFromFile(char* filename, char* buffer[]);
int getNumLinesInFile(char* filename);
void constructDistanceMap(int n, starSystem* systems, int* map[]);
int getDistance(int x1, int y1, int x2, int y2);
int parseFile(int n, char* buffer[], starSystem systems[]);
int parseSystem(char* buffer, starSystem* starSystem);
enum tradeCodes getTradeCode(char* candidate);
int hexToInt(char hex);
int getWtn(starSystem s);
int getWtnTechMod(int tech);
int getWtnStarportMod(char starport, int uwtn);
void printSystem(starSystem s);
int getWorldTradeCodeModifier(starSystem origin, starSystem destination);
void getTradeRoute(int origin, int destination, int numSystems, starSystem* systems, int* map[], int jumprange, int cutoff);
void getBestPath(int origin, int destination, int numSystems, starSystem* systems, int* map[], int jumprange);
int removeSystem(int space[], int numSystems, int origin);
int getNeighbours(int origin, int numSystems, int* space, int* map[], int* neighbours, int jumprange);
void getPathsFrom(int origin, int destination, int numSystems, int* space, starSystem* system, int* map[], pathSet* paths, path pathFrom, int jumprange, int cutoff);
int getBtnDistanceMod(int d);
int getBtnStarportMod(char starport);

int main(int argc, char * argv[]){
    char * filename;
    char ** buffer;
    starSystem * systems;
    int ** map;
    int i;
    int j;
    int lines;
    int numSystems;
    int origin;
    int destination;
    int jumprange = 2;
    int cutoff = MAX_PATH_LENGTH;

    filename = argv[1];
    if(argc == 3){
        cutoff = strtol(argv[2], 0, 10);
    }

    lines = getNumLinesInFile(filename);
    if(lines == 0) return -1;

    // Allocation
    buffer = (char **)malloc(lines * sizeof(char *));
    map = (int **)malloc(lines * sizeof(int *));
    systems = (starSystem *)malloc(lines * sizeof(starSystem));
    for(i = 0; i < lines; i++){
        buffer[i] = (char *)malloc(MAX_LINE_LENGTH * sizeof(char));
        map[i] = (int *)malloc(lines * sizeof(int));
    }
    readFromFile(filename, buffer);

    // Initial data construction
    numSystems = parseFile(lines, buffer, systems);
    constructDistanceMap(numSystems, systems, map);

	/*
    for(i = 0; i < numSystems; i++){
		printf("%03d ", i);
        printSystem(systems[i]);
    }
	*/

    for(origin = 0; origin < numSystems; origin++){
        for(destination = origin+1; destination  < numSystems; destination++){
			getTradeRoute(origin, destination, numSystems, systems, map, jumprange, cutoff);
        }
    }

    // Cleanup
    for(i = 0; i < lines; i++){
        free(buffer[i]);
        free(map[i]);
    }
    free(buffer);
    free(map);
    free(systems);
    return 0;
}

void printSystem(starSystem s){
    int i;
    printf("%02d%02d %c%d-%d ", s.x, s.y, s.starport, s.population, s.techlevel);
    printf("%d: ", s.wtn);
    for(i = 0; i < s.numTrades; i++){
        printf("%02d ", s.trades[i]);
    }
    printf("\n");
}

int getNumLinesInFile(char* filename){
    FILE* fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    int lines = 0;

    fp = fopen(filename, "r");
    if (fp == NULL) return 0;

    while ((read = getline(&line, &len, fp)) != -1) {
        lines++;
    }
    fclose(fp);
    return lines;
}

int readFromFile(char* filename, char** buffer){
    FILE* fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    int index = 0;

    fp = fopen(filename, "r");
    if (fp == NULL) return -1;

    while ((read = getline(&line, &len, fp)) != -1) {
        strncpy(buffer[index], line, MAX_LINE_LENGTH);
        index++;
    }

    fclose(fp);
    return 0;
}

int parseFile(int n, char* buffer[], starSystem systems[]){
    int i;
    int ret;
    int numSystems = 0;
    for(i = 0; i < n; i++){
        ret = parseSystem(buffer[i], &systems[numSystems]);
        if(!ret) numSystems++;
    }
    return numSystems;
}

int parseSystem(char* buffer, starSystem* starSystem){
    char sx[3];
    char sy[3];
    char* trades = buffer + 31;
    int done = 0;
    int i;
    int j;
    enum tradeCodes likesag[] = {Na, As, De, Fl, Ic, Va};

    if(buffer[0] == '#') return -1;
    if(buffer[0] == '\n') return -1;
    if(buffer[0] == '\r') return -1;

    memcpy(sx, buffer+14, 2);
    memcpy(sy, buffer+16, 2);
    sx[2] = 0;
    sy[2] = 0;
    starSystem->x = strtol(sx, 0, 10);
    starSystem->y = strtol(sy, 0, 10);

    starSystem->starport = buffer[19];
    starSystem->population = hexToInt(buffer[23]);
    starSystem->techlevel = hexToInt(buffer[27]);

    // Get number of trades
    starSystem->numTrades = 0;
    starSystem->ag = 0;
    starSystem->likesag = 0;
    starSystem->ni = 0;
    starSystem->in = 0;
    for(i = 0; i < 5; i++){
        if(!strncmp(trades+(i*3), "  ", 2))
            break;
        starSystem->trades[starSystem->numTrades] = getTradeCode(trades+(i*3));
        if(starSystem->trades[starSystem->numTrades] == Ag){
            starSystem->ag = 1;
        }
        if(starSystem->trades[starSystem->numTrades] == Ni){
            starSystem->ni = 1;
        }
        if(starSystem->trades[starSystem->numTrades] == In){
            starSystem->in = 1;
        }
        for(j = 0; j < 6; j++){
            if(starSystem->trades[starSystem->numTrades] == likesag[j]){
                starSystem->likesag = 1;
            }
        }
        starSystem->numTrades++;
    }
    starSystem->wtn = getWtn(*starSystem);
    return 0;
}

int hexToInt(char hex){
    if((hex >= '0') && (hex <= '9'))
        return hex - '0';
    if((hex >= 'a') && (hex <= 'z'))
        return 10 + hex - 'a';
    if((hex >= 'A') && (hex <= 'Z'))
        return 10 + hex - 'A';
    return 0;
}

enum tradeCodes getTradeCode(char* candidate){
    if(!strncmp(candidate, "Ag", 2)) return Ag;
    if(!strncmp(candidate, "As", 2)) return As;
    if(!strncmp(candidate, "Ba", 2)) return Ba;
    if(!strncmp(candidate, "De", 2)) return De;
    if(!strncmp(candidate, "Fl", 2)) return Fl;
    if(!strncmp(candidate, "Ga", 2)) return Ga;
    if(!strncmp(candidate, "Hi", 2)) return Hi;
    if(!strncmp(candidate, "Ht", 2)) return Ht;
    if(!strncmp(candidate, "Ic", 2)) return Ic;
    if(!strncmp(candidate, "In", 2)) return In;
    if(!strncmp(candidate, "Lo", 2)) return Lo;
    if(!strncmp(candidate, "Lt", 2)) return Lt;
    if(!strncmp(candidate, "Na", 2)) return Na;
    if(!strncmp(candidate, "Ni", 2)) return Ni;
    if(!strncmp(candidate, "Po", 2)) return Po;
    if(!strncmp(candidate, "Ri", 2)) return Ri;
    if(!strncmp(candidate, "Wa", 2)) return Wa;
    if(!strncmp(candidate, "Va", 2)) return Va;
    return -1;
}

void constructDistanceMap(int n, starSystem* systems, int* map[]){
    int s;
    int d;

    for(s = 0; s < n; s++){
        for(d = 0; d < n; d++){
            map[s][d] = getDistance(systems[s].x, systems[s].y, systems[d].x, systems[d].y);
        }
    }
}

int getDistance(int x1, int y1, int x2, int y2){
    int dx;
    int dy;
    // x1 -= 1; x2 -= 1; y1 -= 1; y2 -= 1;
    y1 *= 2;
    y2 *= 2;
    if(!(x1 % 2)) y1++;
    if(!(x2 % 2)) y2++;
    dy = abs(y2 - y1);
    dx = abs(x2 - x1);
    if(dx > dy) return dx;
    return (dx + dy) / 2;
}

int getWtn(starSystem s){
    int uwtn;
    uwtn = getWtnTechMod(s.techlevel) + s.population;
    uwtn += getWtnStarportMod(s.starport, uwtn);
    if(uwtn < 0) uwtn = 0;
    return uwtn;
}

int getWtnTechMod(int tech){
    if (tech < 2) return -1;
    if (tech < 5) return 0;
    if (tech < 9) return 1;
    if (tech < 15) return 2;
    return 3;
}

int getWtnStarportMod(char starport, int uwtn){
    //            0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16
    int amod[] = {3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0};
    int bmod[] = {2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0,-1,-1,-2,-2,-2};
    int cmod[] = {2, 1, 1, 1, 1, 1, 0, 0, 0, 0,-1,-1,-2,-2,-3,-3,-3};
    int dmod[] = {1, 1, 1, 0, 0, 0, 0, 0,-1,-1,-2,-2,-3,-3,-4,-4,-4};
    int emod[] = {1, 1, 0, 0, 0, 0,-1,-1,-2,-2,-3,-3,-4,-4,-5,-5,-5};
    int xmod[] = {0, 0, 0, 0,-5,-5,-6,-6,-7,-7,-8,-8,-9,-9,-10,-10,-10};
    if(starport == 'A') return amod[uwtn];
    if(starport == 'B') return bmod[uwtn];
    if(starport == 'C') return cmod[uwtn];
    if(starport == 'D') return dmod[uwtn];
    if(starport == 'E') return emod[uwtn];
    if(starport == 'X') return xmod[uwtn];
    return 0;
}

int getWorldTradeCodeModifier(starSystem origin, starSystem destination){
    int dm = 0;
    if((origin.ag) && (destination.likesag)) dm++;
    if((destination.ag) && (origin.likesag)) dm++;
    if((origin.ni) && (destination.in)) dm++;
    if((destination.ni) && (origin.in)) dm++;
    return dm;
}

void getTradeRoute(int origin, int destination, int numSystems, starSystem* systems, int* map[], int jumprange, int cutoff){
    int ubtn;
    int* space;
    int i;
    pathSet paths;
    path start;
    int bestvalue;
    int best;
    int value;
    int s;

    ubtn = systems[origin].wtn +
        systems[destination].wtn +
        getWorldTradeCodeModifier(
            systems[origin],
            systems[destination]);

    // Set up initial space
    space = (int*)malloc(numSystems * sizeof(int));
    for(i = 0; i < numSystems; i++){
        space[i] = i;
    }

    // Remove the origin
    numSystems = removeSystem(space, numSystems, origin);
    free(space);

    start.numNodes = 0;
    start.length = 0;
    start.starportmods = 0;
    paths.numpaths = 0;
    paths.bestvalue = -1000;
    paths.ubtn = ubtn;
    getPathsFrom(origin, destination, numSystems, space, systems, map, &paths, start, jumprange, cutoff);
    bestvalue = 0;
    best = 0;

	if(gdebug) printf("%d paths found\n", paths.numpaths);
    for(i = 0; i < paths.numpaths; i++){
        value = ubtn + paths.paths[i].starportmods + getBtnDistanceMod(paths.paths[i].length);
		if(gdebug) printf("path %d value %d, bestvalue %d\n", i, value, bestvalue);
        if(value > bestvalue){
            best = 1;
        }
    }
    if(best){
        printf("%02d%02d->%02d%02d %02d %02d: ",
            systems[origin].x,
            systems[origin].y,
            systems[destination].x,
            systems[destination].y,
            ubtn + paths.paths[best].starportmods + getBtnDistanceMod(paths.paths[best].length),
            paths.paths[best].numNodes
        );
        for(i = 0; i < paths.paths[best].numNodes; i++){
            s =paths.paths[best].nodes[i];
            printf("%02d%02d ", systems[s].x, systems[s].y);
        }
        printf("\n");
    } else if (gdebug){
		printf("No best path found for %d to %d\n", origin, destination);
	}
}

int removeSystem(int space[], int numSystems, int origin){
    int i;
    for(i = 0; i < numSystems; i++){
        if(space[i] == origin){
            for(; i < numSystems-1; i++){
                space[i] = space[i+1];
            }
            return numSystems - 1;
        }
    }
    printf("Didn't find system %d to remove!\n", origin);
    return 0;
}

void getPathsFrom(int origin, int destination, int numSystems, int* space, starSystem* systems, int* map[], pathSet* paths, path pathFrom, int jumprange, int cutoff){
    int numNeighbours;
    int neighbours[MAX_NEIGHBOURS];
    int i;
    int* subspace;
    int currentvalue;
    if(pathFrom.length >= cutoff){
		if(gdebug) printf("length cutoff\n");
		return;
	}
    numNeighbours = getNeighbours(origin, numSystems, space, map, neighbours, jumprange);

	if(gdebug){
		for(i = 0; i < pathFrom.numNodes; i++){
			printf(".");
		}
		printf("%d to %d n: %d s: %d ", origin, destination, numNeighbours, numSystems);
		for(i = 0; i < numNeighbours; i++){
			printf("%d ", neighbours[i]);
		}
		printf("\n");
	}

    if(numNeighbours){
        // Add this system to the path that lead us here.
        pathFrom.nodes[pathFrom.numNodes] = origin;
        // If this is not the first system on the path
        if(pathFrom.numNodes){
            pathFrom.length += map[origin][pathFrom.nodes[pathFrom.numNodes-1]];
            pathFrom.starportmods += getBtnStarportMod(systems[origin].starport);
        }
        pathFrom.numNodes++;
        currentvalue = pathFrom.starportmods + getBtnDistanceMod(pathFrom.length);
        if((paths->ubtn + currentvalue) <= BTN_CUTOFF){
			if(gdebug) printf("btn cutoff\n");
			return;
		}
        if(currentvalue <= paths->bestvalue){
			if(gdebug) printf("Goose chase %d %d\n", currentvalue, paths->bestvalue);
			return;
		}
        for(i = 0; i < numNeighbours; i++){
            if(neighbours[i] == destination){
                pathFrom.nodes[pathFrom.numNodes] = destination;
                pathFrom.length += map[origin][destination];
                pathFrom.numNodes++;
                memcpy(&paths->paths[paths->numpaths], &pathFrom, sizeof(path));
                paths->numpaths++;
                if(currentvalue > paths->bestvalue) paths->bestvalue = currentvalue;
				if(gdebug) printf("found it\n");
                return;
            }
        }
        // Need to sort neighbours by starport. Do we? Lets not yet.
        subspace = (int*)malloc(numSystems*sizeof(int));
        for(i = 0; i < numSystems; i++){
            subspace[i] = space[i];
        }
        for(i = 0; i < numNeighbours; i++) removeSystem(subspace, numSystems, neighbours[i]);
        for(i = 0; i < numNeighbours; i++){
            // This sort of depends on how pass-as-reference vrs pass-as-value works...
            // I.e. does this create a copy of pathFrom?
            getPathsFrom(neighbours[i], destination, numSystems-numNeighbours, subspace, systems, map, paths, pathFrom, jumprange, cutoff);
        }
        free(subspace);
    }
}

int getBtnStarportMod(char starport){
    if(starport == 'X') return -3;
    if(starport == 'E') return -2;
    if(starport == 'D') return -1;
    return 0;
}

int getBtnDistanceMod(int d){
    if(d < 2)  return 0;
    if(d < 3)  return -1;
    if(d < 6)  return -2;
    if(d < 10) return -3;
    if(d < 20) return -4;
    if(d < 30) return -5;
    if(d < 60) return -6;
    if(d < 100) return -7;
    if(d < 200) return -8;
    if(d < 300) return -9;
    if(d < 600) return -10;
    if(d < 1000) return -11;
    return -12;
}

int getNeighbours(int origin, int numSystems, int* space, int* map[], int* neighbours, int jumprange){
    int i;
    int numNeighbours = 0;
    for(i = 0; i < numSystems; i++){
        if(map[origin][space[i]] <= jumprange){
            neighbours[numNeighbours] = space[i];
            numNeighbours++;
            if(numNeighbours >= MAX_NEIGHBOURS){
                printf("Hit max neighbours");
                return numNeighbours;
            }
        }
    }
    return numNeighbours;
}

