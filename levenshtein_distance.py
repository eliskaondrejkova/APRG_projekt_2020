def levenshtein_distance(word_1, word_2):
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


def main():
    """Drive code"""
    word_1 = "kroky"
    word_2 = "drak"
    print(levenshtein_distance(word_1, word_2))


if __name__ == "__main__":
    main()
