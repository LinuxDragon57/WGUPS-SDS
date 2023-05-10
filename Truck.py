import re
from datetime import datetime, timedelta

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
        min_distance: float = -1
        next_delivery: Package = Package()
        for package in self.loaded_packages:
            distance: float = determine_distance(current_location, package.address)
            if min_distance < 0 or distance < min_distance:
                min_distance = distance
                next_delivery = package
        return next_delivery

    def load_packages(self, package_table: HashTable, current_location: str = '4001 South 700 East',
                      keys: list[str] = None):
        package: Package = Package()

        def can_load() -> bool:
            # Return False unless the package passes all checks.
            if package.notes == '' or notes_list[3].match(package.notes):
                return True
            elif notes_list[0].match(package.notes):
                truck_number: int = int(re.search(r'\d+', package.notes).group())
                if truck_number == self.truck_number:
                    return True
            elif notes_list[1].match(package.notes) or notes_list[2].match(package.notes):
                if self.route_number > 1:
                    return True
            return False

        def load_package():
            if package is not None and can_load():
                self.loaded_packages.append(package)
                package.set_status()
                package_table.remove(key)

        if keys is None:
            min_distance: float = -1
            for key in range(1, package_table.size+1):
                package: Package = package_table.search(key)
                distance: float = determine_distance(current_location, package.address)
                if (min_distance < 0 or distance < min_distance) and package.package_id is not None:
                    min_distance = distance
                    load_package()
        else:
            for key in keys:
                for loaded_package in self.loaded_packages:
                    if not loaded_package.match_id(int(key)):
                        package = package_table.search(int(key))
                if package.package_id is not None:
                    load_package()

        if len(self.loaded_packages) <= 16 and package.package_id is not None:
            if notes_list[3].match(package.notes):
                package_keys = re.search(r'[\d+, ]+', package.notes).group().split(', ')
                self.load_packages(package_table=package_table, current_location=package.address, keys=package_keys)
            else:
                self.load_packages(package_table=package_table, current_location=package.address)

    def deliver_packages(self, time_elapsed: datetime, current_location: str = '4001 South 700 East',
                         total_distance: float = 0):
        if len(self.loaded_packages) > 0:
            package: Package = self.determine_next_delivery(current_location)
            distance: float = determine_distance(current_location, package.address)
            total_distance += distance
            delivery_time = distance / 18
            time_elapsed += timedelta(hours=delivery_time)
            package.set_status()
            self.deliver_packages(time_elapsed, package.address, total_distance)
        else:
            distance: float = determine_distance(current_location, '4001 South 700 East')
            total_distance += distance
            delivery_time = distance / 18
            time_elapsed += timedelta(hours=delivery_time)
            self.route_number += 1
            return total_distance, time_elapsed
