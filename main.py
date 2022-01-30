import random
from collections import defaultdict
from typing import List


WORD_LENGTH = 5
COMPUTER, USER = range(2)
DICT_FILE = "words.txt"


def generate_word_list() -> List[str]:
    file = open(DICT_FILE, 'r')
    word_list = file.readlines()
    word_list = [w.strip().upper() for w in word_list]
    return word_list


def parse_ab(user_input) -> tuple[int, int]:
    user_input = user_input.strip()
    if len(user_input) != 5:
        return -1, -1
    if user_input[1] != "a" or user_input[3] != "b":
        return -1, -1
    a = int(user_input[0])
    b = int(user_input[2])
    return a, b


def verify_ab(word1: str, word2: str) -> str:
    res = [0] * WORD_LENGTH
    for i in range(WORD_LENGTH):
        if word1[i] == word2[i]:
            res[i] = 2
        elif word2[i] in word1:
            res[i] = 1

    return "".join([str(r) for r in res])


def pre_process_response(guess: str, response: str) -> str:
    # Special Rule:
    # 1. "CHURR": 00210 should be 00211" because the second "R" occur once.
    # 2. "CHURR": 00020 should be 00021" because the second "R" occur once.
    # Simple by: if a character occurs twice, it is impossible to be 0, fix it to 1
    index_score_map = defaultdict(list)
    response = [int(score) for score in response]
    for i, c in enumerate(guess):
        index_score_map[c].append((i, response[i]))
    for c in index_score_map:
        if len(index_score_map[c]) > 1:
            if any([score for index, score in index_score_map[c]]):
                for index, score in index_score_map[c]:
                    if score == 0:
                        response[index] = 1
    return "".join(str(score) for score in response)


def delete_mismatch(answers: List[str], guess: str, response: str) -> List[str]:
    response = pre_process_response(guess, response)
    print(f"delete_mismatch: pre_process_response={response}")

    def match(word: str) -> bool:
        nonlocal response, guess
        return verify_ab(word, guess) == response

    return list(filter(match, answers))


if __name__ == '__main__':
    word_list = generate_word_list()
    print(f"Instruction")
    print(f" * Use the suggestion and feedback the response by 5 digits - 0:gray,1:yellow,2:green, E.g. '00120'")
    print(f" * Use your own answer and feedback the response, just type your answer")
    print(f"   Then type the response. E.g. '00120")
    print(f" * If the answer is not in the word list (Unable to guess), type '33333'")
    while len(word_list) > 1:
        print(word_list)
        print(f"The current number of word_list: {len(word_list)}")
        guess_i = random.randint(0, len(word_list) - 1)
        guess_word = word_list[guess_i]
        guesser = COMPUTER
        while True:
            print(f"{'COMPUTER' if guesser == COMPUTER else 'USER'} guess \"{guess_word}\"")

            user_input = input("Type the feedback or your answer: ")
            if len(user_input) == 5:
                if user_input.isalpha():
                    guesser = USER
                    guess_word = user_input.upper()
                    continue
                if user_input == "33333":
                    word_list.remove(guess_word)
                    break
                if user_input.count("0") + user_input.count("1") + user_input.count("2") == WORD_LENGTH:
                    word_list = delete_mismatch(word_list, guess_word, user_input)
                    break

            # Exception Handle
            print(f"Please type 5 digits or 5 letters...")
    if len(word_list) == 1:
        print(f"The answer is {word_list}")
    else:
        print(f"WTF...I cannot guess the answer!")
