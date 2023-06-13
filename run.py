# This file contains all static functions that process data within the application.
import sys

from data import get_addresses
from data import get_distances
from Package import Package


# This function parses the data to find the distance between any two given addresses.
def determine_distance(address1: str, address2: str) -> float:
    addresses = get_addresses()  # Get the tuple of street addresses
    distance_table = get_distances()  # Get the distances matrix, which is already a digraph.
    # If either one of the addresses aren't in the addresses tuple,
    # then the distance is unable to be determined.
    if not (address1 in addresses and address2 in addresses):
        print(f'Could not determine the distance between "{address1}" and "{address2}".', file=sys.stderr)
        sys.exit(1)
    else:
        # Get the index of the addresses passed into the function as parameters.
        coordinate1: int = addresses.index(address1)
        coordinate2: int = addresses.index(address2)
        # Use the two indices gathered to find the distance between the two addresses.
        # The order of the indices can be reversed if it finds an empty string.
        if distance_table[coordinate1][coordinate2] != '':
            return distance_table[coordinate1][coordinate2]
        elif distance_table[coordinate2][coordinate1] != '':
            return distance_table[coordinate2][coordinate1]


# Find the package closest to the location passed in as a parameter.
def determine_next_package(iterable, current_location: str) -> Package:
    return min(iterable, key=lambda nearest_package: determine_distance(current_location, nearest_package.address))
