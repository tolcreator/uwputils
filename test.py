import sector
import traderoute
import sys
import draw
import hexutils

def main(input, output):
    draw.drawTradeRoutes(input, output, 128)

if __name__ == "__main__":
    input = sys.argv[1]
    output = sys.argv[2]
    main(input, output)
