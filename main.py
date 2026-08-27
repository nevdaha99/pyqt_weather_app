from modules import app, window


def main():
    try:
        window.show()
        app.exec()
    except Exception as err:
        print(err)


if __name__ == "__main__":
    main()
