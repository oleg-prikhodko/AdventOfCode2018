import re
from collections import defaultdict, namedtuple

Point = namedtuple("Point", "x y")
BBox = namedtuple("BBox", "xmin xmax ymin ymax")
POINT_PATTERN = re.compile(r"(?P<x>\d{1,3}), (?P<y>\d{1,3})")


def load_points(filename="day_6.txt"):
    points = []
    with open(filename) as input_file:
        for line in input_file:
            match = POINT_PATTERN.search(line)
            points.append(Point(int(match.group("x")), int(match.group("y"))))
        return points


def taxicab_distance(x1, x2, y1, y2):
    return abs(x1 - x2) + abs(y1 - y2)


if __name__ == "__main__":
    points = load_points()

    xmin = min(points, key=lambda point: point.x).x
    xmax = max(points, key=lambda point: point.x).x
    ymin = min(points, key=lambda point: point.y).y
    ymax = max(points, key=lambda point: point.y).y
    bbox = BBox(xmin, xmax, ymin, ymax)

    counts = defaultdict(int)
    infinite = set()
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):

            point_distances = sorted(
                (taxicab_distance(x, point.x, y, point.y), i)
                for i, point in enumerate(points)
            )

            if point_distances[0][0] != point_distances[1][0]:
                counts[point_distances[0][1]] += 1
                if x == xmin or x == xmax or y == ymin or y == ymax:
                    infinite.add(point_distances[0][1])

    print(
        max(
            counts.items(),
            key=lambda item: item[1] if item[0] not in infinite else 0,
        )
    )

    point_count = 0
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            total_dist = sum(
                taxicab_distance(x, point.x, y, point.y) for point in points
            )
            if total_dist < 10000:
                point_count += 1

    print(point_count)
