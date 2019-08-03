import hexgrid
import draw

def main():
    size=128
    hexgrid.createSectorGrid("grid.png", hexSize=size)
    hexgrid.createSectorGrid("blank.png", hexSize=size, blank=True)
    draw.drawSector("uwp.txt", "sector.png", hexSize=size)

if __name__ == "__main__":
    main()
