from collections import namedtuple, Counter
import re
from itertools import chain

Claim = namedtuple("claim", "id left_offset top_offset width height")
claim_pattern = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")


def load_claims(filename="input_3.txt"):
    claims = []
    with open(filename) as input_file:
        for line in input_file:
            match = re.search(claim_pattern, line)
            claim = Claim(*[int(group) for group in match.groups()])
            claims.append(claim)
        return claims


def get_inches(claim):
    inches = []
    for x in range(claim.width):
        for y in range(claim.height):
            inches.append((claim.left_offset + x, claim.top_offset + y))
    return inches


if __name__ == "__main__":
    claims = load_claims()
    get_width = lambda claim: claim.left_offset + claim.width
    get_height = lambda claim: claim.top_offset + claim.height
    inches_hor = get_width(max(claims, key=get_width))
    inches_vert = get_height(max(claims, key=get_height))
    # print('Total inches:', inches_hor*inches_vert)

    inches_from_all_claims = chain.from_iterable(
        get_inches(claim) for claim in claims
    )
    inches_counter = Counter(inches_from_all_claims)
    overlapping_inches = {
        inch_coords: count
        for inch_coords, count in inches_counter.items()
        if count > 1
    }
    print(len(overlapping_inches))

    overlapping_inches_set = set(overlapping_inches)
    for claim in claims:
        inches_set = set(get_inches(claim))
        if not inches_set & overlapping_inches_set:
            print(claim.id)
            break
