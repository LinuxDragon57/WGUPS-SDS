import re
from datetime import timedelta

from Package import Package
from run import determine_next_package, determine_distance
from HashTable import HashTable
from static.environment import notes_list


# Class that models a truck that is able to carry packages.
class Truck:

    # The constructor initializes a truck with a parametrized truck number. Optionally, a departure hour and
    # a departure minute could be passed in. The truck will also have an empty payload and the departure
    # hour and minute will be initialized to both a departure time and a time elapsed timedelta object (if
    # these parameters weren't passed in, then the defaults will be used).
    def __init__(self, truck_number: int, departure_hour: int = 8, departure_minute: int = 0):
        self.truck_number = truck_number
        self.payload: list[Package] = list()
        self.total_distance: float = 0
        self.departure_time: timedelta = timedelta(hours=departure_hour, minutes=departure_minute)
        self.time_elapsed: timedelta = timedelta(hours=departure_hour, minutes=departure_minute)

    # This method takes in the Package HashTable as its only parameter. It intelligently loads the packages
    # using a series of functions.
    def load_packages(self, package_table: HashTable):

        # This local function recursively finds the packages that need to be loaded with other packages.
        def get_related_packages(package: Package, unchecked_keys=None, related_packages=None) -> list[Package]:
            if unchecked_keys is None:  # Initialize unchecked_keys to an empty list on first run.
                unchecked_keys = list()  # This is the running list of unchecked package ids.
            if related_packages is None:  # Initialize related_packages to an empty list on first run.
                related_packages = list()  # This is the list of packages that all need to be loaded with each other.

            # Append the parametrized package to the list of related packages.
            related_packages.append(package)
            # After appending the package to the list, extract all the other packages
            # that it needs to be loaded with from the end of its notes attribute string
            # as a list of integers and append it the running list of unchecked package ids.
            unchecked_keys += list(map(int, re.findall(r'\d+', package.notes)))
            # Then, remove duplicate integers from the running list of unchecked package ids.
            unchecked_keys = [*set(unchecked_keys)]
            # Iterate through the related_packages (which are already checked), and make sure that
            # none of their package ids also ended up in the list of unchecked ids.
            for checked_package in related_packages:
                if checked_package.package_id in unchecked_keys:
                    unchecked_keys.remove(checked_package.package_id)
            # The base case for the recursive function: If there aren't anymore
            # unchecked package ids, return the list of completed packages.
            if len(unchecked_keys) == 0:
                return related_packages
            # Otherwise, retrieve the next unchecked package id by popping it from the list of
            # unchecked package ids so that it can be used to retrieve the package from the HashTable.
            # Then continue the recursion with that package.
            else:
                next_package: Package = package_table.search(unchecked_keys.pop(0))
                return get_related_packages(next_package, unchecked_keys, related_packages)

        # This local function controls the loading of packages based upon their notes criteria.
        def can_load(package: Package) -> bool:
            # The package cannot be loaded if the package has already been loaded onto the truck.
            if package in self.payload:
                return False
            # The package can only be loaded if it has no notes, if the package must be delivered by a
            # certain truck and that truck number matches, if the package has been delayed for whatever
            # reason and the departure time is 09:05, or if the package must be loaded with other packages
            # and there's enough room on the truck for all of its "related" packages.
            if package.notes == '':
                return True
            elif notes_list[0].match(package.notes):
                truck_number: int = int(re.search(r'\d+', package.notes).group())
                if truck_number == self.truck_number:
                    return True
            elif notes_list[1].match(package.notes) or notes_list[2].match(package.notes):
                if self.time_elapsed >= timedelta(hours=9, minutes=5):
                    return True
            elif notes_list[3].match(package.notes):
                packages = get_related_packages(package)
                if len(self.payload) <= (16 - len(packages)):
                    return True
            return False  # By default, the function returns false.

        # This local function loads a single package passed to it on the truck, sets
        # the status of that package to Status.En_Route, marks it with the number of the
        # truck it is loaded onto, and removes it from the HashTable of unloaded packages.
        def load_package(package: Package):
            self.payload.append(package)
            package.set_status()
            package.set_deliverer(self.truck_number)
            package_table.remove(package.package_id)

        # This local function uses the recursive function above to retrieve a group of packages that
        # must be loaded with each other and loads them onto the truck.
        def load_related_packages(package: Package) -> Package:
            related_packages: list[Package] = get_related_packages(package)
            for package in related_packages:
                load_package(package)
            return package

        # This local function initially loads packages based upon the proximity of their delivery addresses,
        # but it will hand off functionality to other functions if it cannot load it based upon proximity.
        def load_nearest_package(current_location: str, not_loadable: list[Package]) -> tuple[str, list[Package]]:
            # Retrieve the package nearest to the current location.
            nearest_package: Package = determine_next_package(package_table, current_location)
            if nearest_package is not None:
                # Can the package be loaded onto this truck at this very moment?
                loadable: bool = can_load(nearest_package)
                # If so, and its notes do not state that it must be loaded with other packages, load it.
                if loadable and not notes_list[3].match(nearest_package.notes):
                    load_package(nearest_package)
                # However, if its notes state that it must be loaded with other packages, hand it off
                # to the function responsible for retrieving it and loading it with other packages.
                elif loadable and notes_list[3].match(nearest_package.notes):
                    nearest_package = load_related_packages(nearest_package)
                # Otherwise, take it out of the HashTable for now and temporarily place it aside
                # into a list of packages that cannot be loaded onto this truck right now.
                elif not loadable:
                    not_loadable.append(nearest_package)
                    package_table.remove(nearest_package.package_id)
            # Return the address of the package for the next use of this function
            # as well as the list  of set-aside packages that cannot be loaded.
            return nearest_package.address, not_loadable

        # This local function runs the main loop that keeps loading packages until the
        # truck is full or there are no more packages in the HashTable of packages.
        def execute_main_loop():
            # The truck starts its journey at the Hub.
            current_location: str = "4001 South 700 East"
            # This is the running list of packages that the algorithm sets aside because
            # they cannot currently be loaded onto this truck.
            not_loadable: list[Package] = list()
            while True:  # Exit controlled loop runs until either the truck is full or the HashTable is empty.
                if len(self.payload) == 16 or package_table.is_empty():
                    # Before exiting the loop, insert the packages that were set aside back into the HashTable.
                    for package in not_loadable:
                        package_table.insert(package)
                    break
                else:
                    # Load nearest package takes in a string and the running list of packages unable to
                    # be loaded, and then it returns both of those mutated variables.
                    current_location, not_loadable = load_nearest_package(current_location, not_loadable)

        execute_main_loop()  # Execute the main loop of the method.

    # This method takes in an empty HashTable object that it will populate with packages as it delivers
    # them so that their data can be retrieved by the user interface.
    def deliver_packages(self, delivered_packages: HashTable) -> HashTable:
        # As with the load_packages() method, the truck starts out at the Hub.
        # The only difference is that the truck is actually leaving the hub this time.
        current_location: str = "4001 South 700 East"
        while True:  # Exit controlled loop runs until the truck is empty.
            # First, determine the next package to deliver based upon its proximity to the current location.
            # It is kind of inefficient to have to run this again; but while the load_packages() method tried, the
            # packages inevitably got jumbled up as the load_packages() method made exceptions for the special cases.
            package: Package = determine_next_package(self.payload, current_location)
            if package is not None:
                # Now to retrieve the actual distance the truck travels between the current and next locations.
                distance: float = determine_distance(current_location, package.address)
                # Update the Truck's record of the total distance it has traveled.
                self.total_distance += distance
                # Determine a floating point value for the time elapsed between the two most recent delivery points.
                delivery_time = distance / 18
                # Use that floating point value to update the running time delta since it started the route.
                self.time_elapsed += timedelta(hours=delivery_time)
                # Set the package's delivery time based upon the current marker on the truck.
                package.set_delivery_time(self.time_elapsed)
                # Set the package's delivery status to Status.DELIVERED.
                package.set_status()
                # Update the Truck's current location to the delivery address of the package it just delivered.
                current_location = package.address
                # Insert that delivered package into the HashTable of delivered packages.
                delivered_packages.insert(package)
                # Remove the package from the truck.
                self.payload.remove(package)
            if len(self.payload) == 0:  # break out of the loop when the Truck is empty.
                break
        # Get the final distance for the truck's return journey to the hub.
        distance: float = determine_distance(current_location, '4001 South 700 East')
        return delivered_packages  # Return the HashTable of delivered packages.
