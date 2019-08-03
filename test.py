import hexgrid

def main():
    hexgrid.createSectorGrid("grid.png")
    hexgrid.createSectorGrid("blank.png", blank=True)

if __name__ == "__main__":
    main()
