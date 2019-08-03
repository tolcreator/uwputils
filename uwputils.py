import argparse
import sector

def main(filename, write, update, show):
    sector.autocomplete(filename, write=write, update=update, show=show)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="File to act on")
    parser.add_argument("-w", "--write", help="Make changes to the file", action="store_true")
    parser.add_argument("-u", "--update", help="Recalculate seconday characteristics", action="store_true")
    parser.add_argument("-s", "--show", help="Show systems", action="store_true")
    args = parser.parse_args()
    main(args.filename, args.write, args.update, args.show)
