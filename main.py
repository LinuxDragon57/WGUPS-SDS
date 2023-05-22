
from data import get_packages
from Truck import Truck
from HashTable import HashTable


def main():
    package_table: HashTable = get_packages()
    truck1: Truck = Truck(1)
    truck2: Truck = Truck(2)
    truck1.load_packages(package_table)
    truck2.load_packages(package_table)
