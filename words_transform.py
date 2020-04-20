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
    """Saves variable 'words' into the new file dictionary_with_keys.json"""
    file = open("dictionary_with_keys.json", "w+")

    order = "0123456789abcdefghijklmnopqrstuvwxyz"
    order_index = 0
    string = ""
    get_smaller_index = False
    first_time = True
    length = 0

    file.write('{"%s":{' % order[order_index])
    for index, char in enumerate(words):
        if get_smaller_index:
            index -= 1
            char = words[index]
            get_smaller_index = False

        if (string == "") or (string[0] == order[order_index]):
            if char == "_":
                string = string + " "

            elif char == "\r":
                if " " not in string:
                    if first_time:
                        file.write('"%s": %d' % (string, length))
                        first_time = False
                    else:
                        file.write(', "%s": %d' % (string, length))

                length = 0
                string = ""

            elif (char != "\n") and (char != "\r"):
                string = string + char
                string = string.lower()
                length += 1

        elif string[0] != order[order_index] and (order_index + 1 < len(order)):
            order_index += 1
            file.write('},\n"%s":{' % order[order_index])
            get_smaller_index = True
            first_time = True

    file.write('}}')
    file.close()

    return


def main():
    """The driver function"""
    words = get_words()
    save_words(words)
    save_words_with_keys(words)


if __name__ == "__main__":
    main()
