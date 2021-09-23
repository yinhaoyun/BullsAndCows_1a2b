from typing import List


def generate_ans() -> List[str]:
    ans = []
    formed = []
    used = [False] * 10

    def backtrack() -> None:
        if len(formed) == 4:
            ans.append(list(formed))
            return
        for i in range(len(used)):
            if used[i]:
                continue
            used[i] = True
            formed.append(i)
            backtrack()
            formed.pop()
            used[i] = False

    backtrack()
    return ans


def parse_ab(user_input) -> tuple[int, int]:
    user_input = user_input.strip()
    if len(user_input) != 4:
        return -1, -1
    if user_input[1] != "a" or user_input[3] != "b":
        return -1, -1
    a = int(user_input[0])
    b = int(user_input[2])
    return a, b


def verify_ab(ans1: List[int], ans2: List[int]) -> tuple[int, int]:
    a, b = 0, 0
    for i, n in enumerate(ans1):
        if ans1[i] == ans2[i]:
            a += 1
        elif n in ans2:
            b += 1
    return a, b


def delete_mismatch(ans, guess, a, b) -> List[List[int]]:
    def match(ans: List[int]) -> bool:
        va, vb = verify_ab(ans, guess)
        return va == a and vb == b

    return list(filter(match, ans))


if __name__ == '__main__':
    ans = generate_ans()
    while len(ans) > 1:
        print(ans)
        print(len(ans))
        print(f"And I guess {ans[0]}")
        user_input = input("?a?b: ")
        a, b = parse_ab(user_input)
        if a < 0 or b < 0:
            print("Invalid answer, input again...")

        if a + b > 4:
            print("a + b must less or equal to 4")

        ans = delete_mismatch(ans, ans[0], a, b)

    print(f"The answer is {ans[0]}")
