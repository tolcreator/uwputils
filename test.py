import uwp

def main():
    for i in range(0, 100000):
        u = uwp.generate()
        s = uwp.uwpToStr(u)
        print s
        uwp.sanityCheck(s)

if __name__ == "__main__":
    main()
