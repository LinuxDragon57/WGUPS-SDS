# This file contains all static functions that manipulates data within the application.
# This file makes heavy use of the python CSV library:
# https://docs.python.org/3/library/csv.html
import pathlib
import csv

from HashTable import HashTable
from Package import Package

# Global file path variable allows setting the relative filepath
# directory to the directory in which this file is located when
# using the open() function.
__here__ = pathlib.Path(__file__).parent


# This function reads the packages CSV file, and it inserts them into the HashTable.
def get_packages() -> HashTable:
    package_list: HashTable = HashTable()  # Instantiate the HashTable
    with open(__here__/'static/packages.csv', newline='') as csvfile:  # Open the CSV file.
        package_reader = csv.DictReader(csvfile, dialect='unix')  # Read the package data.
        # Note that package_reader is a list of dictionaries where each row is
        # a package and the dictionary's keys correspond to the Package fields.
        for row in package_reader:  # Iterate through the extracted data
            # noinspection PyArgumentList
            package = Package(**row)  # Create a new package object by inserting the dictionary from each row.
            package_list.insert(package)  # Insert the package into the HashTable.
    return package_list  # Return the packages HashTable, and close the csv file.


# This function reads the distances CSV file, and it inserts them into a 2-dimensional list.
def get_distances() -> list[list]:
    distances_list: list[list] = []  # Create a new list of lists.
    with open(__here__/'static/distances.csv', newline='',) as csvfile:  # Open the CSV file.
        # Read the addresses and distance data - while ensuring that numbers aren't gathered as strings.
        distance_reader = csv.reader(csvfile, dialect='unix', quoting=csv.QUOTE_NONNUMERIC)
        # Note that distance_reader is a list of lists, but it is not in an ideal format inside the csv.reader object.
        for row in distance_reader:  # Iterate through the extracted data.
            distances_list.append(row)  # Append each row to the list of lists.
    return distances_list  # Return the distances matrix, and close the csv file.


# This function reads the distances CSV file, and it inserts only the addresses into a tuple.
def get_addresses() -> tuple:
    street_addresses: list = []  # Create a new list.
    with open(__here__/'static/distances.csv', newline='') as csvfile:  # Open the CSV file.
        address_list = csv.reader(csvfile, dialect='unix').__next__()  # Read the first line of the distance data.
        # Note that address_list is a simple one dimensional list.
        for address in address_list:  # Iterate through the extracted data.
            # The first part of the address is irrelevant. So since every address is on two lines, split the
            # string at the return character; and append the last portion to the street_addresses list.
            street_addresses.append(address.split('\n').pop())
    return tuple(street_addresses)  # Return the street_addresses list as a tuple, and close the csv file.
