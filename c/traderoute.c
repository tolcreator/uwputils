#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 80

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
} starSystem;

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

int main(int argc, char * argv[]){
    char * filename;
    char ** buffer;
    starSystem * systems;
    int ** map;
    int i;
    int j;
    int lines;
    int numSystems;

    filename = argv[1];
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

    for(i = 0; i < numSystems; i++){
        printSystem(systems[i]);
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
    for(i = 0; i < 5; i++){
        if(!strncmp(trades+(i*3), "  ", 2))
            break;
        starSystem->trades[starSystem->numTrades] = getTradeCode(trades+(i*3));
        starSystem->numTrades++;
    }
    starSystem->wtn = getWtn(*starSystem);
    return 0;
}

int hexToInt(char hex){
    if((hex >= '0') && (hex <= '9'))
        return hex - '0';
    if((hex >= 'a') && (hex <= 'z'))
        return hex - 'a';
    if((hex >= 'A') && (hex <= 'Z'))
        return hex - 'A';
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
    y1 *= 2;
    y2 *= 2;
    if(x1 % 2) y1++;
    if(x2 % 2) y2++;
    dy = abs(y2 - y1);
    dx = abs(x2 - x1);
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

