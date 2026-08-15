from modules import *


def main():
    try:
        window.show()
        app.exec()
    except Exception as err:
        print(err)


if __name__ == "__main__":
    main()
