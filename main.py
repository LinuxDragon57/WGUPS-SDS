#!/usr/bin/python
# Tyler Gautney #001400532
import argparse
from datetime import timedelta
from data import get_packages
from Truck import Truck
from HashTable import HashTable


def main():
    parser = argparse.ArgumentParser(description='CLI for the WGUPS Delivery Route Planning System.')
    parser.add_argument('--time', type=str, help='Enter a time in 24-hour format (HH:MM)')
    parser.add_argument('--package-id', type=int, help='Enter a package ID number.')
    args = parser.parse_args()

    undelivered_packages: HashTable = get_packages()
    delivered_packages: HashTable = HashTable()
    truck1: Truck = Truck(1)
    truck2: Truck = Truck(2, departure_hour=9, departure_minute=5)
    truck3: Truck = Truck(3)

    truck1.load_packages(undelivered_packages)
    truck3.load_packages(undelivered_packages)

    truck1.deliver_packages(delivered_packages)
    truck3.deliver_packages(delivered_packages)

    truck2.load_packages(undelivered_packages)
    truck2.deliver_packages(delivered_packages)

    def print_delivery_status():
        time_ints = list(map(int, args.time.split(':')))
        arg_time = timedelta(hours=time_ints[0], minutes=time_ints[1])
        if package.delivery_time > arg_time:
            print(f"\t\tPackage is en route on Truck {package.deliverer}")
        else:
            print(f"\t\tPackage was delivered by Truck {package.deliverer} at {package.delivery_time}.")

    if args.time is None and args.package_id is not None:  # !time && package_id
        parser.error('The --package_id argument requires a time to be entered.')
    elif args.time is not None and args.package_id is None:  # time && !package_id
        for key in range(1, delivered_packages.size+1):
            package = delivered_packages.search(key)
            print(package)
            print_delivery_status()
    elif args.time is not None and args.package_id is not None:  # time && package_id
        package = delivered_packages.search(args.package_id)
        print(package)
        print_delivery_status()
    elif args.time is None and args.package_id is None:  # !time && !package_id
        for key in range(1, delivered_packages.size+1):
            package = delivered_packages.search(key)
            print(package)
            print(f"\t\tPackage was delivered at {package.delivery_time} by Truck {package.deliverer}.")


if __name__ == '__main__':
    main()
