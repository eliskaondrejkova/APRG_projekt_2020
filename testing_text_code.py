def new_file(text):
    with open("testing_test.txt", "w") as text_file:
        text_file.write(text)


def main():
    text = "Hello everyone! What are you doing during quarantine? Are you making face mask?"
    new_file(text)


if __name__ == "__main__":
    main()
