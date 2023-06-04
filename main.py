
from data import get_packages
from Package import Package
from Truck import Truck
from HashTable import HashTable


def main():
    undelivered_packages: HashTable = get_packages()
    delivered_packages: HashTable = HashTable()
    truck1: Truck = Truck(1)
    truck2: Truck = Truck(2)

    truck1.load_packages(undelivered_packages)
    truck2.load_packages(undelivered_packages)

    truck1.deliver_packages(delivered_packages)
    truck2.deliver_packages(delivered_packages)

    truck2.load_packages(undelivered_packages)
    truck2.deliver_packages(delivered_packages)

    for key in range(1, delivered_packages.size+1):
        package = delivered_packages.search(key)
        print(f'{package}: {package.delivery_status}')

    print(delivered_packages.is_full())

    print(f'Truck 1 traveled a total of {truck1.total_distance:.2f} miles;')
    print(f'and Truck 2 traveled a total of {truck2.total_distance:.2f} miles,')
    print(f'for a combined total of {truck1.total_distance + truck2.total_distance:.2f} miles.')

