import heapq

from ascii_graph import Pyasciigraph
import argparse
import sys

from collections import defaultdict
from typing import List

WORD_LENGTH = 5
COMPUTER, USER = range(2)
DICT_ANSWERS = "wordle-answers-alphabetical.txt"
DICT_ALLOWED_GUESS = "wordle-allowed-guesses.txt"
VOWEL = "aeiou"
COMMON_CONSONANT = "bcdfghjklmnpqrstvwxyz"
CONSONANT = "bcdfghjklmnpqrstvwxyz"
BEST_GUESS = ["BUMPH", "KEDGY", "CLINT"]

# -65011712 AEROS
# -1970176 LINTY
# -58880 BUMPH


def read_dict(filename: str) -> List[str]:
    file = open(filename, 'r')
    word_list = file.readlines()
    word_list = [w.strip().upper() for w in word_list]
    return word_list


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


def print_statistics(word_list):
    occurs = [0] * 26
    for word in word_list:
        for c in word.lower():
            occurs[ord(c) - ord('a')] += 1
    letter_statistics = [(chr(ord('a') + i), occurs[i]) for i in range(26)]
    letter_statistics.sort(reverse=True, key=lambda x:x[1])
    graph = Pyasciigraph()
    for line in graph.graph('test print', letter_statistics):
        print(line)


def match_score(word: str, letters: str) -> int:
    return sum([1 for l in letters if l in word])


def print_words_include(word_list: List[str], letters: str) -> None:
    letters = letters.upper()
    words = []
    for w in word_list:
        if match_score(w, letters) >= 5:
            words.append(w)
    print(words)


def calc_word_score(letter_scores: dict, word) -> int:
    return sum(letter_scores[c] for c in word)


def is_duplicated(word):
    return len(set(word)) != len(word)


def is_used(used, word):
    return any(c in used for c in word)


def get_most_common_word(word_list):
    occurs = [0] * 26
    for word in word_list:
        for c in word.lower():
            occurs[ord(c) - ord('a')] += 1
    letter_statistics = [(chr(ord('a') + i), occurs[i]) for i in range(26)]
    letter_statistics.sort(reverse=True, key=lambda x: x[1])
    graph = Pyasciigraph()
    for line in graph.graph('Letter Occurs', [l for l in letter_statistics if l[1] != 0]):
        print(line)

    new_letter_statistics = [(letter_statistics[i][0].upper(), 1 << (26 - i - 1)) for i in range(26)]
    letter_statistics = new_letter_statistics
    letter_scores = dict()
    for char, score in letter_statistics:
        letter_scores[char] = score
    # print(letter_scores)
    pq = []
    for w in word_list:
        score = -calc_word_score(letter_scores, w)
        heapq.heappush(pq, (score, w))
    while pq:
        score, word = heapq.heappop(pq)
        if is_duplicated(word) and pq:
            continue
        return word


def list_common_words(word_list):
    occurs = [0] * 26
    for word in word_list:
        for c in word.lower():
            occurs[ord(c) - ord('a')] += 1
    letter_statistics = [(chr(ord('a') + i), occurs[i]) for i in range(26)]
    letter_statistics.sort(reverse=True, key=lambda x: x[1])
    new_letter_statistics = [(letter_statistics[i][0].upper(), 1 << (26 - i - 1)) for i in range(26)]
    letter_statistics = new_letter_statistics
    graph = Pyasciigraph()
    for line in graph.graph('test print', letter_statistics):
        print(line)
    letter_scores = dict()
    for char, score in letter_statistics:
        letter_scores[char] = score
    print(letter_scores)
    pq = []
    for w in word_list:
        score = -calc_word_score(letter_scores, w)
        heapq.heappush(pq, (score, w))
    bests = []
    used = set()
    while pq:
        score, word = heapq.heappop(pq)
        if is_duplicated(word) or is_used(used, word):
            continue
        bests.append(word)
        used |= set(word)
        print(score, word)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--statistics", action="store_true", help="Show the statistics of letters")
    parser.add_argument("--list-words", help="List the words which include the letters")
    parser.add_argument("--list-common-words", action="store_true", help="List word by most common letters first")
    args = parser.parse_args()
    if args.statistics:
        word_list = read_dict(DICT_ALLOWED_GUESS)
        print_statistics(word_list)
        sys.exit(0)
    if args.list_words:
        word_list = read_dict(DICT_ALLOWED_GUESS)
        print_words_include(word_list, args.list_words)
        sys.exit(0)
    if args.list_common_words:
        word_list = read_dict(DICT_ANSWERS)
        print_statistics(word_list)
        list_common_words(word_list)
        sys.exit(0)

    print(f"Instruction")
    print(f" * Use the suggestion and feedback the response by 5 digits - 0:gray,1:yellow,2:green, E.g. '00120'")
    print(f" * Use your own answer and feedback the response, just type your answer")
    print(f"   Then type the response. E.g. '00120")
    print(f" * If the answer is not in the word list (Unable to guess), type '33333'")
    answer_list = read_dict(DICT_ANSWERS)
    guess_list = read_dict(DICT_ALLOWED_GUESS)
    while len(answer_list) > 1:
        print(answer_list)
        print(f"The current number of answer_list: {len(answer_list)}")
        print(f"The current number of guess_list: {len(guess_list)}")
        guess_word = get_most_common_word(answer_list)
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
                    guess_list.remove(answer_list)
                    break
                if user_input.count("0") + user_input.count("1") + user_input.count("2") == WORD_LENGTH:
                    answer_list = delete_mismatch(answer_list, guess_word, user_input)
                    guess_list = delete_mismatch(guess_list, guess_word, user_input)
                    break

            # Exception Handle
            print(f"Please type 5 digits or 5 letters...")
    if len(answer_list) == 1:
        print(f"The answer is {answer_list}")
    else:
        print(f"WTF...I cannot guess the answer!")
