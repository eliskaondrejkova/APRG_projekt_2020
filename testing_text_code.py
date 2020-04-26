def new_file(text):
    """Creates a new testing file"""
    with open("testing_text.txt", "w") as text_file:
        text_file.write(text)


def main():
    """Driver function"""
    text = "Hello everyone! What are you doing during quarantine? Are you making face mask?"
    new_file(text)


if __name__ == "__main__":
    main()
