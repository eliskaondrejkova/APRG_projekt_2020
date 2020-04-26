def get_words():
    """Saves content of the file dictionary.txt into the variable words"""
    with open("dictionary.txt") as file:
        words = ""
        for line in file:
            words = words + line

    return words


def save_words_with_keys(words):
    """Saves variable 'words' into the new file dictionary_with_keys.json"""
    file = open("dictionary_with_keys.json", "w+")

    order = "abcdefghijklmnopqrstuvwxyz"
    order_index = 0
    string = ""
    first_time = True
    length = 0

    file.write('{"%s":{' % order[order_index])
    for index, char in enumerate(words):
        if (string == "") or (string[0] == order[order_index]):
            if char == "\n":
                if first_time:
                    file.write('"%s": %d' % (string, length))
                    first_time = False
                else:
                    file.write(', "%s": %d' % (string, length))

                length = 0
                string = ""

            else:
                string = string + char
                length += 1

        elif string[0] != order[order_index] and (order_index + 1 < len(order)):
            order_index += 1
            file.write('},\n"%s":{' % order[order_index])
            first_time = True

    file.write('}}')
    file.close()

    return


def main():
    """The driver function"""
    words = get_words()
    save_words_with_keys(words)


if __name__ == "__main__":
    main()
