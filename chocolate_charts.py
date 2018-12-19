# import re

if __name__ == "__main__":
    recipe_count = 919901
    recipe_offset = 10
    first_elf_idx = 0
    second_elf_idx = 1

    scoreboard = [3, 7]

    # part 1 condition: len(scoreboard) < recipe_count + recipe_offset
    # match = None
    pattern = str(recipe_count)
    digits = [int(d) for d in pattern]
    # pattern not in "".join(map(str, scoreboard))
    while scoreboard[-len(digits) :] != digits:
        recipe_1, recipe_2 = divmod(
            scoreboard[first_elf_idx] + scoreboard[second_elf_idx], 10
        )
        if recipe_1 != 0:
            scoreboard.append(recipe_1)
        scoreboard.append(recipe_2)
        first_elf_idx = (first_elf_idx + 1 + scoreboard[first_elf_idx]) % len(
            scoreboard
        )
        second_elf_idx = (
            second_elf_idx + 1 + scoreboard[second_elf_idx]
        ) % len(scoreboard)

        # match = re.search(str(recipe_count), scoreboard2string(scoreboard))

    # print("".join(str(score) for score in scoreboard[-10:]))
    # print(match)
    print("".join(map(str, scoreboard)).index(pattern))
