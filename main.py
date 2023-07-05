# Tyler Gautney #001400532
# DO NOT ATTEMPT TO EXECUTE THIS FILE DIRECTLY.
# NOTHING WILL HAPPEN.

import argparse
import sys
from datetime import timedelta
from data import get_packages
from Truck import Truck
from HashTable import HashTable


# Main factory function.
def main():
    # Set up the CLI interface using Python's built-in argparse library.
    # https://docs.python.org/3/library/argparse.html
    # First, instantiate the argparse.ArgumentParser with meta-information about the program.
    parser = argparse.ArgumentParser(prog='WGUPS-SoftwareDeliverySystem',
                                     description='CLI for the WGUPS Delivery Route Planning System.')
    # Add an optional argument that allows a user to enter a time. This is not required.
    parser.add_argument('--time', type=str, help='Enter a time in 24-hour format (HH:MM)')
    # Add an optional argument that allows a user to enter one or more package id numbers. This is not required.
    parser.add_argument('--package-ids', type=int, nargs='+',
                        help='Enter at least one package ID number. This argument requires a time to be entered.\n'
                             'More arguments can be passed in as a space delimited list of integers.')

    parser.add_argument('--print-distance-traveled', action='store_true',
                        help='Print out the total distances traveled by all trucks.')
    args = parser.parse_args()  # Run the parser and place the extracted data into an argparse.Namespace object.

    # Set up two HashTable Objects to hold the packages.
    undelivered_packages: HashTable = get_packages()
    delivered_packages: HashTable = HashTable()

    # Fix the address on package 9
    package9 = undelivered_packages.pop(9)
    package9.address = '410 S State St'
    package9.zip_code = 84111
    undelivered_packages.insert(package9)

    # Create 3 Trucks with their respective truck number.
    # Truck 2 will depart late in order to wait on late packages.
    truck1: Truck = Truck(1)
    truck2: Truck = Truck(2, departure_hour=9, departure_minute=5)
    truck3: Truck = Truck(3)

    # Meanwhile, while Truck 2 is waiting, Trucks 1 & 3 load their packages...
    truck1.load_packages(undelivered_packages)
    truck3.load_packages(undelivered_packages)

    # and deliver them.
    truck1.deliver_packages(delivered_packages)
    truck3.deliver_packages(delivered_packages)

    # Finally Truck 2 loads and delivers its packages.
    truck2.load_packages(undelivered_packages)
    truck2.deliver_packages(delivered_packages)

    # Create a factory function for printing out whether any given package is en route
    # to its address or whether it has been delivered at the specified time.
    def print_delivery_status():
        time_ints = list(map(int, args.time.split(':')))  # Convert the CLI time argument into a list of ints.
        arg_time = timedelta(hours=time_ints[0], minutes=time_ints[1])  # Convert the list of ints into a timedelta.
        # If the time passed in by the user is before the package's delivery timestamp, then the package was still
        # en route at that time. Otherwise, the package had been delivered.
        if arg_time < package.delivery_time:
            print(f"\t\tPackage is en route on Truck {package.deliverer}")
        else:
            print(f"\t\tPackage was delivered by Truck {package.deliverer} at {package.delivery_time}.")

    # Use the arguments passed into the parser.ArgumentParser() object to
    # determine how to display data to stdout. Because the argparse.Namespace object
    # has values for all possible arguments, those that weren't given are None.
    # Therefore, an argument that is not in the Namespace is None, so the check looks as follows.
    # Comments are written out beside to translate the if-statement to a more human-readable logic.
    if args.time is None and args.package_ids is not None:  # !time && package_id
        for package_id in args.package_ids:
            package = delivered_packages.search(package_id)
            print(package)
            print(f"\t\tPackage was delivered at {package.delivery_time} by Truck {package.deliverer}.")
    elif args.time is not None and args.package_ids is None:  # time && !package_id
        for package in delivered_packages:
            print(package)
            print_delivery_status()
    elif args.time is not None and args.package_ids is not None:  # time && package_id
        for package_id in args.package_ids:
            package = delivered_packages.search(package_id)
            print(package)
            print_delivery_status()
    elif args.time is None and args.package_ids is None:  # !time && !package_id
        for package in delivered_packages:
            print(package)
            print(f"\t\tPackage was delivered at {package.delivery_time} by Truck {package.deliverer}.")

    if args.print_distance_traveled:
        total_distance: float = truck1.total_distance + truck2.total_distance + truck3.total_distance
        print("\n\n\n\t" + "-"*75)
        print(f'\tTruck 1 traveled a total of {truck1.total_distance:.2f} miles.')
        print(f'\tTruck 2 traveled a total of {truck2.total_distance:.2f} miles.')
        print(f'\tTruck 3 traveled a total of {truck3.total_distance:.2f} miles.')
        print(f'\tThe combined total distance of all trucks is {total_distance:.2f}')
        print('\t'+'-'*75)


# Ensure that this file is being run directly by the user.
if __name__ == '__main__':
    print("Please execute this script as a Python package rather than main.py as a standalone file.", file=sys.stderr)
    print("This means you must pass in the directory containing this file as an argument to the interpreter;\n"
          "rather than the file itself.", file=sys.stderr)
    print("This does not necessarily mean that you pass in the name of the directory containing this file.\n"
          "It depends upon your current working directory. Ideally, execute it one directory up.", file=sys.stderr)
