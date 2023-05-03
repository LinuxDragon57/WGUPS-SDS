import re

from Package import Package
from run import determine_distance
from HashTable import HashTable
from static.environment import notes_list


class Truck:

    def __init__(self, truck_number: int):
        self.truck_number = truck_number
        self.loaded_packages: list[Package] = list()
        self.route_number: int = 1

    def determine_next_delivery(self, current_location: str) -> Package:
        min_distance = None
        for package in self.loaded_packages:
            distance = determine_distance(current_location, package.address)
            if min_distance is None or distance < min_distance:
                min_distance = distance
                next_delivery: Package = package
        # noinspection PyUnboundLocalVariable
        return next_delivery

    def __can_load(self, package: Package) -> bool:
        if not any(notes_list.match(package.notes)):
            return True
        elif notes_list[0].match(package.notes):
            truck_number: int = int(re.search(r'\d+', package.notes).group())
            if truck_number == self.truck_number:
                return True
        elif notes_list[1].match(package.notes) or notes_list[2].match(package.notes):
            # Placeholder conditional. Checking against time would be better.
            if self.route_number > 1:
                return True
        elif notes_list[3].match(package.notes):
            packages = re.search(r'[\d+, ]+', package.notes).group().split(', ')
            for package_id in packages:
                for loaded_package in self.loaded_packages:
                    if loaded_package.match_id(int(package_id)):
                        packages.remove(package_id)
            # May not work if one of the packages is already loaded.
            if len(self.loaded_packages) <= 16 - (len(packages)+1):
                return True
        else:
            return False

    def load_packages(self, package_table: HashTable, current_location: str = '4001 South 700 East',
                      keys: list[str] = None):
        def continue_loading():
            if self.__can_load(package):
                self.loaded_packages.append(package)
                package_table.remove(key)
                if len(self.loaded_packages) <= 16 and notes_list[3].match(package.notes):
                    packages = re.search(r'[\d+, ]+', package.notes).group().split(', ')
                    self.load_packages(package_table, package.address, packages)
                elif len(self.loaded_packages) <= 16:
                    self.load_packages(package_table, package.address)

        if not any(keys):
            min_distance = None
            for key in range(package_table.size):
                package: Package = package_table.search(key)
                distance = determine_distance(current_location, package.address)
                if min_distance is None or distance < min_distance:
                    min_distance = distance
                    continue_loading()
        else:
            for key in keys:
                package: Package = package_table.search(int(key))
                continue_loading()
