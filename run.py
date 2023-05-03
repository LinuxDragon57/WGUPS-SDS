import sys

from data import get_addresses
from data import get_distances


def determine_distance(address1: str, address2: str) -> float:
    addresses = get_addresses()
    distance_table = get_distances()
    if not (address1 in addresses and address2 in addresses):
        print(f'Could not determine the distance between "{address1}" and "{address2}".', file=sys.stderr)
        return -1
    else:
        coordinate1: int = addresses.index(address1)
        coordinate2: int = addresses.index(address2)
        if distance_table[coordinate1][coordinate2] != '':
            return distance_table[coordinate1][coordinate2]
        elif distance_table[coordinate2][coordinate1] != '':
            return distance_table[coordinate2][coordinate1]
