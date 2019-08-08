import sector
import traderoute
import sys
import draw
import hexutils
import hexgrid

def main(input, trade):
    if trade == "trade":
        draw.drawTradeRoutes(input, "trade.png", 256)
        draw.drawTraffic(input, "traffic.png", 256)
    else:
        #hexgrid.createSectorGrid("blank.png", hexSize=256, blank=True)
        #hexgrid.createSectorGrid("grid.png", hexSize=256)
        draw.drawWorldTradeNumber(input, "wtn.png", 256)
        #draw.drawSector(input, "sector.png", 256)

if __name__ == "__main__":
    input = sys.argv[1]
    trade = sys.argv[2]
    main(input, trade)
