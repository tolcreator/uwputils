import uwp

def main():
    for i in range(0, 10000):
        u = uwp.generate()
        s = uwp.uwpToStr(u)
        print s
        uwp.sanityCheck(s)

if __name__ == "__main__":
    main()
