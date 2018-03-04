#!/usr/bin/env python3


from . import sources


def print_tips():
    for tip in sources.load_all_tips():
        print(tip)


def main():
    print_tips()


if __name__ == '__main__':
    main()
