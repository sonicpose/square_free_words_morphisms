from math import floor
import csv
from sfwords import isSquareFree
# from square_free_word_generator import generate_square_free_words_up_to_length
from ast import literal_eval

PATH_TO_WORDS = "square_free_words/"
PATH_TO_MORPHISMS = "morphisms/"

def main():
    # example_morphism_base = [
    #     [0, 1, 2, 0, 1],
    #     [0, 2, 0, 1, 2, 1],
    #     [0, 2, 1, 2, 0, 2, 1]
    # ]

    if check_if_factor_of([0,1], [3,4,0,1,4,2,3]):
        print("TELHLFDJS")

    example_morphism_base = [
        [0,1,2,3,4,5,6, 0, 7],
        [1,2],
        [3,4],
        [5,6]
    ]

    example_input_word = [0, 1, 2]
    #
    # # First method of applying morphism
    # example_output_word_one = apply_morphism_to_word(example_input_word, example_morphism_base)
    #
    # # Second method of applying morphism
    example_morphism_function = create_morphism_from_base(example_morphism_base)
    example_output_word_two = example_morphism_function(example_input_word)
    #
    # print(example_output_word_one == example_output_word_two)
    # print(example_output_word_one)
    print(example_output_word_two)

    test_result = test_morphism_square_free(example_morphism_base)
    print(test_result)

    return


# First method of applying morphisms
def create_morphism_from_base(morphism_base):
    def morphism_function(input_word):
        output_word = []    # Initial decleration
        for letter in input_word:
            if letter >= len(morphism_base):
                raise Exception("Invalid input to morphism", input_word, morphism_base)
            else:
                output_word = output_word + morphism_base[letter]

        return output_word

    return morphism_function


def generate_morphisms_up_to_given_size(size_of_input_alphabet, max_size_of_each_morphism_chunk):
    global PATH_TO_MORPHISMS
    global PATH_TO_WORDS

    current_filename = PATH_TO_MORPHISMS + str(size_of_input_alphabet) + "_" + str(max_size_of_each_morphism_chunk) + \
                       "_morphisms.csv"

    if size_of_input_alphabet > 1:
        old_filename = PATH_TO_MORPHISMS + str(size_of_input_alphabet - 1) + "_" +\
                       str(max_size_of_each_morphism_chunk) + "_morphisms.csv"
        try:
            list_of_old_size_morphisms = read_morphisms_from_csv(old_filename)
            print(list_of_old_size_morphisms)
            list_of_current_size_morphisms = generate_morphisms_of_next_size(list_of_old_size_morphisms, max_size_of_each_morphism_chunk)
        except FileNotFoundError:
            generate_morphisms_up_to_given_size(size_of_input_alphabet - 1, max_size_of_each_morphism_chunk)
            list_of_old_size_morphisms = read_morphisms_from_csv(old_filename)
            list_of_current_size_morphisms = generate_morphisms_of_next_size(list_of_old_size_morphisms, max_size_of_each_morphism_chunk)
    else:
        list_of_possible_words = []
        for i in range(1, max_size_of_each_morphism_chunk+1):
            words_filename = PATH_TO_WORDS + str(i) + "_letter_square_free_words.csv"
            list_of_possible_words = list_of_possible_words + read_words_from_csv(words_filename)
            list_of_current_size_morphisms = list(map(lambda x: [x], list_of_possible_words))

    fill_csv_with_words(current_filename, list_of_current_size_morphisms)

    return


def generate_morphisms_of_next_size(list_of_old_size_morphisms, max_size_of_each_morphism_chunk):
    global PATH_TO_WORDS

    list_of_current_size_morphisms = [] # Initial decleration

    list_of_possible_words = []
    for i in range(1, max_size_of_each_morphism_chunk + 1):
        words_filename = PATH_TO_WORDS + str(i) + "_letter_square_free_words.csv"
        list_of_possible_words = list_of_possible_words + read_words_from_csv(words_filename)   # Is there more efficient way to do this?

    for old_morphism in list_of_old_size_morphisms:
        for word in list_of_possible_words:
            new_morphism = old_morphism + [word]
            if test_morphism_square_free(new_morphism):
                list_of_current_size_morphisms.append(new_morphism)

    return list_of_current_size_morphisms


# Second method of applying morphisms
def apply_morphism_to_word(input_word, morphism_base):
    output_word = []  # Initial decleration
    for letter in input_word:
        if letter >= len(morphism_base):
            raise Exception("Invalid input to morphism")
        else:
            output_word = output_word + morphism_base[letter]

    return output_word


def ruler_morphism(input_word):
    output_word = []    # Initial decleration
    for letter in word:
        output_word = output_word + [0, letter + 1]

    return output_word


# Returns True if it passes the square-free test
def test_morphism_square_free(morphism_base):
    if not does_pass_all_three_letter_checks(morphism_base):
        print("FAILED TO PASS THREE LETTER CHECKS")
        return False
    else:
        size_of_alphbet = len(morphism_base)

        contained_words = generate_all_contained_words(morphism_base)
        alphabet = generate_alphabet_of_given_size(size_of_alphbet)
        morphism_function = create_morphism_from_base(morphism_base)
        for first_letter in alphabet:
            for second_letter in alphabet:
                for third_letter in alphabet:
                    for first_word in contained_words:
                        for second_word in contained_words:
                            possible_word = [first_letter] + first_word + [second_letter] + second_word + [third_letter]
                            if isSquareFree(possible_word):
                                morphed_word = morphism_function(possible_word)
                                if not isSquareFree(morphed_word):
                                    print("FAILED TO PASS CONTAINED WORDS CHECK")
                                    return False

    return True


def generate_alphabet_of_given_size(alphabet_size):
    return list(range(alphabet_size))


def generate_all_contained_words(morphism_base):
    size_of_domain = len(morphism_base)
    array_of_contained_words = []
    for i in range(0, size_of_domain):
        letters_contained_in_current_chunk = []
        for j in range(0, size_of_domain):
            if j != i:
                if check_if_factor_of(morphism_base[j], morphism_base[i]):
                    letters_contained_in_current_chunk.append(j)

        # Generate all square-free words from these letters and check if they're contained
        current_contained_words = [[]]
        morphism_function = create_morphism_from_base(morphism_base)


        for letter in letters_contained_in_current_chunk:
            for word in current_contained_words:
                new_word = word + [letter]
                if (not new_word in current_contained_words) and check_if_factor_of(morphism_function(new_word), morphism_base[i]):
                    current_contained_words.append(new_word)

        array_of_contained_words = array_of_contained_words + current_contained_words

    return array_of_contained_words


# Function needs testing
def check_if_factor_of(factor, word):
    length_of_factor = len(factor)
    length_of_word = len(word)

    for i in range(0, length_of_word):
        if word[i] == factor[0]:
            for j in range(1,length_of_factor):
                if word[i+j] != factor[j]:
                    break
                elif j == length_of_factor - 1:
                    return True

    return False


def does_pass_all_three_letter_checks(morphism_base):
    alphabet_size = len(morphism_base)
    words_for_testing = generate_three_letter_words_on_alphabet(alphabet_size)

    return test_given_words(morphism_base, words_for_testing)


# Returns True if morphism passes all words in square-free test
def test_given_words(morphism_base, words_for_testing):
    morphism_function = create_morphism_from_base(morphism_base)
    for word in words_for_testing:
        generated_word = morphism_function(word)
        if not isSquareFree(generated_word):
            return False

    return True


def generate_three_letter_words_on_alphabet(alphabet_size):
    letters = generate_alphabet_of_given_size(alphabet_size)

    list_of_words = []  # Initial decleration
    for first_letter in letters:
        for second_letter in letters:
            if second_letter != first_letter:
                for third_letter in letters:
                    if third_letter != second_letter:
                        list_of_words.append([first_letter, second_letter, third_letter])

    return list_of_words


def does_new_letter_intoduce_square(word):
    final_letter = word[-1]
    position_half_way_through_word = floor(len(word) / 2) - 1
    for i in range(position_half_way_through_word, len(word) - 1):
        if word[i] == final_letter:
            length_of_half_of_square = len(word) - i - 1
            for j in range(0, length_of_half_of_square):
                if word[i - j] != word[-1 - j]:
                    break
                elif j == length_of_half_of_square - 1:
                    return True

    return False


def generate_square_free_words_up_to_length(length):
    global PATH_TO_WORDS

    name_of_last_file = PATH_TO_WORDS + str(length - 1) + "_letter_square_free_words.csv"
    name_of_new_file = PATH_TO_WORDS + str(length) + "_letter_square_free_words.csv"

    if length > 1:
        try:
            square_free_words_of_last_length = read_words_from_csv(name_of_last_file)
        except FileNotFoundError:
            generate_square_free_words_up_to_length(length - 1)
            square_free_words_of_last_length = read_words_from_csv(name_of_last_file)

        square_free_words_of_current_length = \
            generate_square_free_words_of_next_length(square_free_words_of_last_length, 3)
        # print(square_free_words_of_last_length)
        # print(square_free_words_of_current_length)
        fill_csv_with_words(name_of_new_file, square_free_words_of_current_length)
    else:
        square_free_words_of_current_length = [[0], [1], [2]]
        fill_csv_with_words(PATH_TO_WORDS + '1_letter_square_free_words.csv', square_free_words_of_current_length)

    return


def generate_square_free_words_of_next_length(square_free_words_of_last_length, size_of_alphabet):
    alphabet = generate_alphabet_of_given_size(size_of_alphabet)
    square_free_words_of_current_length = []  # Initial decleration
    for word in square_free_words_of_last_length:
        for letter in alphabet:
            new_word = word + [letter]
            if not does_new_letter_intoduce_square(new_word):
                # print(new_word)
                # print(does_new_letter_intoduce_square(new_word))
                square_free_words_of_current_length.append(new_word)

    return square_free_words_of_current_length


def fill_csv_with_words(filename, list_of_words):
    with open(filename, mode='w') as file:
        writer = csv.writer(file, delimiter=',')
        for word in list_of_words:
            writer.writerow(word)

    return


def read_words_from_csv(filename):
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        list_of_words_pre_reformat = list(reader)

    # This is to fix a problem where it would read in the letters as string characters instead of integers
    # For example the word 010 would be read in as ["0", "1", "0"] as opposed to [0, 1, 0]
    list_of_words_post_reformat = []
    for word in list_of_words_pre_reformat:
        new_word = list(map(int, word))
        list_of_words_post_reformat.append(new_word)

    return list_of_words_post_reformat


def read_morphisms_from_csv(filename):
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        list_of_morphisms_pre_reformat = list(reader)

    # This is to fix typing problem when returning from csv
    list_of_morphisms_post_reformat = []
    for morphism in list_of_morphisms_pre_reformat:
        new_morphism = list(map(literal_eval, morphism))
        list_of_morphisms_post_reformat.append(new_morphism)

    return list_of_morphisms_post_reformat


def generate_alphabet_of_given_size(alphabet_size):
    return list(range(alphabet_size))


generate_morphisms_up_to_given_size(3, 10)
# main()
# list_of_lists_of_lists = [
#     [[0,1,2], [0,2,3]],
#     [[4,5], [3,4]]
# ]
# fill_csv_with_words("test.csv", list_of_lists_of_lists)
# print(read_morphisms_from_csv("test.csv")[0][0][1])
