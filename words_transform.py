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

    order = "0123456789abcdefghijklmnopqrstuvwxyz"
    order_index = 0
    string = ""
    break_word = False

    file.write("{'%s':(" % order[order_index])
    for char in words:
        if (string == "") or (string[0] == order[order_index]):
            if char == "_":
                string = string + " "

            elif (char == "\r") or (break_word == True):
                file.write("'%s'," % string)
                string = ""
                break_word = False

            elif (char != "\n") and (char != "\r"):
                string = string + char
                string = string.lower()

        elif string[0] != order[order_index] and (order_index + 1 < len(order)):
            order_index += 1
            file.write("),\n'%s':(" % order[order_index])
            break_word = True

    file.write(")}")
    file.close()

    return


def main():
    """The driver function"""
    words = get_words()
    save_words(words)
    save_words_with_keys(words)


if __name__ == "__main__":
    main()
