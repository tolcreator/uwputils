#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 80

typedef struct StarSystem {
    int x;
    int y;
    char starport;
    char population;
    char techlevel;
} starSystem;

int readFromFile(char* filename, char* buffer[]);
int getNumLinesInFile(char* filename);
void constructDistanceMap(int n, char* buffer[], int* map[]);
int getDistance(char* source, char* dest);
void getCoordsFromString(char* s, int coords[]);

int main(int argc, char * argv[]){
    char * filename;
    char ** buffer;
    int ** map;
    int i;
    int j;
    int lines;

    filename = argv[1];
    lines = getNumLinesInFile(filename);
    if(lines == 0) return -1;

    buffer = (char **)malloc(lines * sizeof(char *));
    for(i = 0; i < lines; i++){
        buffer[i] = (char *)malloc(MAX_LINE_LENGTH * sizeof(char));
    }
    readFromFile(filename, buffer);

    map = (int **)malloc(lines * sizeof(int *));
    for(i = 0; i < lines; i++){
        map[i] = (int *)malloc(lines * sizeof(int));
    }

    constructDistanceMap(lines, buffer, map);

    for(i = 0; i < lines; i++){
        for(j = 0; j < lines; j++){
            printf("%02d ", map[i][j]);
        }
        printf("\n");
    }

    // Cleanup
    for(i = 0; i < lines; i++){
        free(buffer[i]);
        free(map[i]);
    }
    free(buffer);
    free(map);
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

int readFromFile(char* filename, char* buffer[]){
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

void constructDistanceMap(int n, char* buffer[], int* map[]){
    int s;
    int d;

    for(s = 0; s < n; s++){
        for(d = 0; d < n; d++){
            map[s][d] = getDistance(buffer[s], buffer[d]);
        }
    }
}

int getDistance(char* source, char* dest){
    int scoords[2];
    int dcoords[2];
    int dx;
    int dy;

    getCoordsFromString(source, scoords);
    getCoordsFromString(dest, dcoords);

    scoords[1] *= 2;
    dcoords[1] *= 2;
    if(scoords[0] % 2) scoords[1]++;
    if(dcoords[0] % 2) dcoords[1]++;
    dy = abs(dcoords[1] - scoords[1]);
    dx = abs(dcoords[0] - scoords[0]);
    if((dx + dy) % 2) printf("Thought this had to be even? %d %d\n", dx, dy);
    return (dx + dy) / 2;
}

void getCoordsFromString(char* s, int coords[]){
    char sx[3];
    char sy[3];

    memcpy(sx, s+14, 2);
    memcpy(sy, s+16, 2);
    sx[2] = 0;
    sy[2] = 0;
    coords[0] = strtol(sx, 0, 10);
    coords[1] = strtol(sy, 0, 10);
}
