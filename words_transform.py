import requests


def get_words():
    """Gets words from the web and saves them to variable 'words'"""
    website = "https://www.wordgamedictionary.com/english-word-list/download/english.txt"
    response = requests.get(website)
    response.encoding = "utf-8"
    words = response.text

    if response.status_code == 200:
        return words

    else:
        print("Could not find the url!")
        return


def save_words(words):
    """Saves variable 'words' into the new file dictionary.txt"""
    file = open("dictionary.txt", "w+")

    for char in words:
        if char == "_":
            char = " "
        file.write(str(char))
    file.close()

    return


def save_words_with_keys(words):
    """Saves variable 'words' into the new file dictionary_with_keys.txt"""
    file = open("dictionary_with_keys.txt", "w+")

    count = 0
    first = 0

    file.write("{")
    for index, char in enumerate(words):
        if words[index] == "_":
            char = " "

        if words[index] == "\r":
            file.write("': '%d',\n" % count)
            count = 0
            first = 0

        if first == 0:
            file.write("'")
            first += 1

        if (words[index] != "\n") and (words[index] != "\r"):
            file.write(str(char))
            count += 1

        if words[index] == len(words):
            file.write("}")

    file.close()

    return


def main():
    """The driver function"""
    words = get_words()
    save_words(words)
    save_words_with_keys(words)


if __name__ == "__main__":
    main()