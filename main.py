def load_files():
    """Loads the dictionary and the text file"""
    testing_text_list = list()
    word = ""

    with open("testing_text.txt") as file:
        text = file.read()

        for char in text:
            if char.isalnum():
                word = word + char

            else:
                if word != "":
                    word.lower()
                    testing_text_list.append(word)
                    word = ""

                if char != " ":
                    testing_text_list.append(char)

    with open("dictionary_with_keys.txt") as file:
        dictionary = file.read()

    return testing_text_list, dictionary


def main():
    """Driver function"""
    text_list, dictionary = load_files()


if __name__ == "__main__":
    main()
