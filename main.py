import json


def get_words(index):
    """Saves content of the file dictionary.txt or 'dictionary_user.txt' into the variable words"""
    if index == "1":
        try:
            with open("dictionary_user.txt", "r") as file:
                words = ""
                for line in file:
                    words = words + line

        except IOError:
            print("The file 'dictionary_user.txt' is not available. Loading 'dictionary.txt'!")
            with open("dictionary.txt", "r") as file:
                words = ""
                for line in file:
                    words = words + line

    else:
        with open("dictionary.txt", "r") as file:
            words = ""
            for line in file:
                words = words + line

    return words


def save_words_with_keys(words):
    """Saves variable 'words' into the new file dictionary_with_keys.json"""
    file = open("dictionary_with_keys.json", "w+")

    order = "0123456789abcdefghijklmnopqrstuvwxyz"
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


def load_files():
    """Loads the dictionary and the text file and saves them as variables"""
    testing_text_list = list()
    word = ""

    file_name = input("Please write here the name of the file, which is to be corrected (without the suffix): ")

    try:
        with open(file_name + ".txt") as file:
            text = file.read()

            for char in text:
                if char.isalnum() or char == "'":
                    word = word + char

                else:
                    if word != "":
                        testing_text_list.append(word)
                        word = ""

                    if char != " ":
                        testing_text_list.append(char)
    except IOError:
        print("File which is to be checked is not accessible.")
        return False

    with open("dictionary_with_keys.json") as file:
        dictionary = file.read()

    return True, testing_text_list, dictionary


def create_checked_file():
    """Creates a new file in which it will saves the corrected version of original file"""
    with open("checked_text.txt", "w+") as file:
        print("Created a new file!")

    return


def text_correction(text_list, dictionary, correcting):
    """Sends individual words from text_list for a check whether they are in the dictionary, if not sends them for
     correction and later for a save of their correct form."""
    if correcting == "1":
        print("Currently checking your file, please hold on.\n")

    first_position = True
    change = False

    for position, i in enumerate(text_list):
        check = False
        check2 = True
        result = False

        if i.find("'") != -1 and i[0] != "'":
            check = True

        if i.isalnum() or (check and len(i) > 1):
            if correcting == "1":
                item = i.lower()
                same_letter_words = get_words_from_dict(item, dictionary)

                top_index = len(same_letter_words) - 1
                bottom_index = 0
                index = 1
                original_word = get_list_indexes(item)

                result = narrowing_search(same_letter_words, top_index, bottom_index, original_word, index,
                                          control=False)

            if correcting == "2":
                result = True
                item = i
                print("\nChecked word is: " + i)
                answer = input("Do you wish to change it(y/n): ")
                while (answer != "y") and (answer != "Y") and (answer != "n") and (answer != "N"):
                    answer = input("Please, use only y (yes) or n (no): ")

                if (answer == "y") or (answer == "Y"):
                    item = input("Please, write here te correct form: ")

            first_position, dictionary, change = checked_file(result, item, position, text_list, i, dictionary, check2,
                                                              first_position, change)

        else:
            check2 = False
            first_position, dictionary, change = checked_file(result, item, position, text_list, i, dictionary, check2,
                                                              first_position, change)

    if change:
        answer = input("\nThere were detected changes in the database.\nDo you want to make the changes permanent by"
                       " saving them into the file 'dictionary_user'?\n(Please note, that this may affect the script "
                       "next time!)(y/n): ")

        while (answer != "n") and (answer != "N") and (answer != "y") and (answer != "Y"):
            print("Please use only letters n (no) or y (yes)!")
            answer = input("Should the changes be saved?(y/n): ")

        if (answer == "y") or (answer == "Y"):
            print("Saving the changes. Please, hold on.")
            save_changes(dictionary)

    return


def get_words_from_dict(word, dictionary):
    """Gets words from the dictionary according to the first letter of the searched word"""
    same_letter_words = list()

    if word[0].isalnum():
        val_keys = dictionary.get(word[0])
        values = val_keys.keys()

        same_letter_words = []
        for item in values:
            same_letter_words.append(item)

    return same_letter_words


def get_list_indexes(word):
    """Translates the word into a list of indexes according to the ALPHABET"""
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
    word_indexes_list = list()

    for letter in word:
        for item in range(0, len(ALPHABET)):
            if ALPHABET[item] == letter:
                word_indexes_list.append(item)

    return word_indexes_list


def narrowing_search(same_letter_words, top_index, bottom_index, original_word, index, control):
    """Gets the words with the same starting letter, uses search algorithm and tries to find the searched word in
    them """
    if bottom_index > top_index:
        if control:
            return False, bottom_index
        else:
            return False

    half = round((top_index + bottom_index) / 2)
    dict_word = same_letter_words[half]

    checked_word = get_list_indexes(dict_word)

    if original_word == checked_word:
        return True

    else:
        if original_word[index - 1] != checked_word[index - 1]:
            index -= 1
            if original_word[index] < checked_word[index]:
                top_index = half - 1

            elif original_word[index] > checked_word[index]:
                bottom_index = half + 1

            result = narrowing_search(same_letter_words, top_index, bottom_index, original_word, index, control)
            return result

        if (index > len(original_word) - 1) or (index > len(checked_word) - 1):
            same_letter_words.remove(dict_word)
            top_index = top_index - 1
            result = narrowing_search(same_letter_words, top_index, bottom_index, original_word, index, control)
            return result

        else:
            if original_word[index] < checked_word[index]:
                top_index = half - 1
                result = narrowing_search(same_letter_words, top_index, bottom_index, original_word, index, control)
                return result

            elif original_word[index] > checked_word[index]:
                bottom_index = half + 1
                result = narrowing_search(same_letter_words, top_index, bottom_index, original_word, index, control)
                return result

            elif original_word[index] == checked_word[index]:
                index += 1

                result = narrowing_search(same_letter_words, top_index, bottom_index, original_word, index, control)
                return result


def l_distance(word_1, word_2):
    """Gets the distance needed to change one string into another one"""
    length_word1 = len(word_1) + 1
    length_word2 = len(word_2) + 1

    matrix = [[0 for i in range(0, length_word1)] for j in range(0, length_word2)]

    for i in range(0, length_word1):
        matrix[0][i] = i
    for j in range(0, length_word2):
        matrix[j][0] = j

    for i in range(1, length_word2):
        for j in range(1, length_word1):
            if word_1[j - 1] == word_2[i - 1]:
                matrix[i][j] = matrix[i - 1][j - 1]
            else:
                matrix[i][j] = min([matrix[i - 1][j], matrix[i][j - 1], matrix[i - 1][j - 1]]) + 1
    distance = matrix[i][j]

    return distance


def similar_length_words(original_word, dictionary):
    """Creates a list of words which have same or +- 2 letter length as original_word"""
    similar_words_list = list()
    searched_length = len(original_word)

    dict_keys = dictionary.values()
    for letter in dict_keys:
        for word in letter:
            if (letter.get(word) == searched_length) or (letter.get(word) == searched_length + 1) \
                    or (letter.get(word) == searched_length - 1) or (letter.get(word) == searched_length + 2) \
                    or (letter.get(word) == searched_length - 2):
                similar_words_list.append(word)

    return similar_words_list


def possible_variations(word, similar_words_list):
    """Creates a list selection (min. length of 3 words if possible) which contains the most similar possibilities"""
    for i in range(1, len(word)):
        name = "possibilities_with_distance_%d" % i
        locals()[name] = list()

    for possible_replacement in similar_words_list:
        distance = l_distance(word, possible_replacement)

        name = "possibilities_with_distance_%d" % distance
        if name in locals():
            locals()[name].append(possible_replacement)

    count_of_possibilities = 0
    selection = list()

    for i in range(1, len(word)):
        name = "possibilities_with_distance_%d" % i
        for item in locals()[name]:
            selection.append(item)

        if len(locals()[name]) > 2 or count_of_possibilities > 2:
            break

        elif len(locals()[name]) > 0:
            count_of_possibilities = count_of_possibilities + len(locals()[name])

    return selection


def checked_file(result, item, position, text_list, i, dictionary, check, first_position, change):
    """Rewrites the corrected version of the original file into the file 'checked_text.txt'"""
    with open("checked_text.txt", "a") as file:
        if check:
            if result:
                if (position > 0) and (not text_list[position - 1].isalnum()):
                    file.write(" ")

                if not first_position:
                    file.write(" ")
                    if i.istitle():
                        item = item.capitalize()

                elif first_position:
                    item = item.capitalize()
                    first_position = False

                file.write(item)

            else:
                print("Word '" + item + "' is not in the dictionary.")
                char = item[0]
                if char.isalnum:
                    answer = input("Do you wish to add word '" + item + "' to the dictionary?(y/n): ")

                    while (answer != "n") and (answer != "N") and (answer != "y") and (answer != "Y"):
                        print("Please use only letters n (no) or y (yes)!")
                        answer = input("Do you wish to add word '" + item + "' to the dictionary?(y/n): ")

                    if (answer == "y") or (answer == "Y"):
                        dictionary, change = add_to_dictionary(item, dictionary)
                        new_word = item

                    elif (answer == "n") or (answer == "N"):
                        similar_words_list = similar_length_words(item, dictionary)
                        selection = possible_variations(item, similar_words_list)
                        new_word = printout(item, selection)

                        while new_word not in selection:
                            print("\nThe written word is not in the list!")
                            new_word = printout(item, selection)

                        print("\nReplacing the original word '" + item + "' with a new word '" + new_word + "'!\n")

                    if (position > 0) and (not text_list[position - 1].isalnum()):
                        file.write(" ")

                    if not first_position:
                        file.write(" ")
                        if i.istitle():
                            new_word = new_word.capitalize()

                    elif first_position:
                        new_word = new_word.capitalize()
                        first_position = False

                    file.write(new_word)

        else:
            if i != ",":
                first_position = True
            file.write(i)
    return first_position, dictionary, change


def printout(item, selection):
    """Prints the possible correct variations of the original misspelled word"""
    print("\nThese are the possible right variations of the misspelled word '" + item + "':")

    line = "["
    count = 0
    for num, option in enumerate(selection):
        if count == 0:
            line = line + option
            count += 1
        else:
            line = line + ", " + option
            count += 1

        if count % 10 == 0 and count != 0:
            line = line + ", "
            print(line)
            line = ""
            count = count - 10
    if count != 0:
        print(line + "]")

    new_word = input("Please, select the most desirable option from this list: ")

    return new_word


def add_to_dictionary(item, dictionary):
    """Adds new word to variable 'dictionary_with_keys'. And if wanted updates the files 'dictionary_with_keys.json'
    and 'dictionary.txt'"""
    new_dictionary = {}
    dict_keys = dictionary.keys()

    for letter in dict_keys:
        if letter == item[0]:
            word_dictionary = {}
            letter_values = dictionary.get(letter)
            all_words = letter_values.keys()
            all_words_list = list(letter_values.keys())

            top_index = len(all_words_list)
            bottom_index = 0
            index = 1
            original_word = get_list_indexes(item)
            result = narrowing_search(all_words_list, top_index, bottom_index, original_word, index, control=True)
            new_position = result[1]

            for index, word in enumerate(all_words):
                if index == new_position:
                    length = len(item)
                    pair = {item: length}
                    word_dictionary.update(pair)

                    value = letter_values.get(word)
                    copy = {word: value}
                    word_dictionary.update(copy)

                else:
                    value = letter_values.get(word)
                    copy = {word: value}
                    word_dictionary.update(copy)

            copy = {letter: word_dictionary}
            new_dictionary.update(copy)

        else:
            words_of_the_letter = dictionary.get(letter)
            copy = {letter: words_of_the_letter}
            new_dictionary.update(copy)

    change = True

    return new_dictionary, change


def save_changes(dictionary):
    """Saves changes that were made to the database into the new files 'dictionary_user'"""
    with open("dictionary_user.txt", "w+") as file:
        dict_keys = dictionary.keys()
        first_time = True

        for letter in dict_keys:
            words = dictionary.get(letter)
            for word in words:
                if first_time:
                    file.write(word)
                    first_time = False
                else:
                    file.write("\n" + word)

    return


def main():
    """Driver function"""
    print("This is the start of the script.")

    index = input("\nFor using the file 'dictionary_user.txt' press 1 and for the file 'dictionary.txt' press 2: ")
    while (index != "1") and (index != "2"):
        index = input("Please, use only 1 => 'dictionary_user.txt' or 2 => 'dictionary.txt': ")

    words = get_words(index)
    save_words_with_keys(words)
    file_exists = load_files()

    if file_exists:
        create_checked_file()
        text_list = file_exists[1]
        string = file_exists[2]

        dictionary = json.loads(string)

        answer = input("For automatic correction press 1 and for interactive press 2: ")
        while (answer != "1") and (answer != "2"):
            answer = input("Please, use only 1 => automatic or 2 => interactive: ")

        text_correction(text_list, dictionary, answer)

    print("This is the end of the script.")


if __name__ == "__main__":
    main()
