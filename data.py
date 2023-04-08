import csv

from HashTable import HashTable
from Models import Package


def get_packages() -> HashTable:
    package_list: HashTable = HashTable()
    with open('./static/packages.csv', newline='') as csvfile:
        package_reader = csv.DictReader(csvfile, dialect='excel')
        for row in package_reader:
            # noinspection PyArgumentList
            package = Package(**row)
            package_list.insert(package)
        return package_list


def get_distances() -> list:
    distances: list = [[None]*29]*27

    return distances
