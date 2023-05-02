import sys

from HashTable import HashTable
from data import get_addresses
from data import get_distances
from Models import Package


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


def load_packages(package_table: HashTable):
    min_distance = None
    current_location: str = ""
    for key in range(package_table.size):
        package: Package = package_table.search(key)
        distance = determine_distance(current_location, package.address)
        if min_distance is None or distance < min_distance:
            min_distance = distance
            next_delivery: Package = package
    # noinspection PyUnboundLocalVariable
    return next_delivery
