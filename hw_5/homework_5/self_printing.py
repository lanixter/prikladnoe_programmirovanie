import sys


def main():

    with open(__file__, 'r', encoding='utf-8') as file:
        content = file.read()
        print(content, end='')


if __name__ == '__main__':
    main()