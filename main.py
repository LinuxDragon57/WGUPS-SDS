
from data import get_packages
from Truck import Truck


def main():
    package_table = get_packages()
    truck1: Truck = Truck(1)
    truck2: Truck = Truck(2)
    truck1.load_packages(package_table)
    truck2.load_packages(package_table)
