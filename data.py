import csv

from HashTable import HashTable
from Package import Package


def get_packages() -> HashTable:
    package_list: HashTable = HashTable()
    with open('./static/packages.csv', newline='') as csvfile:
        package_reader = csv.DictReader(csvfile, dialect='unix')
        for row in package_reader:
            # noinspection PyArgumentList
            package = Package(**row)
            package_list.insert(package)
        return package_list


def get_distances() -> list[list]:
    distances_list: list[list] = list()
    with open('./static/distances.csv', newline='',) as csvfile:
        distance_reader = csv.reader(csvfile, dialect='unix', quoting=csv.QUOTE_NONNUMERIC)
        for row in distance_reader:
            distances_list.append(row)
    return distances_list


def get_addresses() -> tuple:
    street_addresses: list = []
    with open('./static/distances.csv', newline='') as csvfile:
        address_list = csv.reader(csvfile, dialect='unix').__next__()
        for address in address_list:
            street_addresses.append(address.split('\n').pop())
        return tuple(street_addresses)
