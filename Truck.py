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
        for package in self.loaded_packages:
            distance: float = determine_distance(current_location, package.address)
            if min_distance < 0 or distance < min_distance:
                min_distance = distance
                next_delivery: Package = package
        # noinspection PyUnboundLocalVariable
        return next_delivery

    def load_packages(self, package_table: HashTable):

        def get_related_packages(package: Package, unchecked_keys=None, packages=None) -> list[Package]:
            if unchecked_keys is None:
                unchecked_keys = list()
            if packages is None:
                packages = list()

            packages.append(package)
            unchecked_keys += list(map(int, re.findall(r'\d+', package.notes)))
            unchecked_keys = [*set(unchecked_keys)]
            for checked_package in packages:
                if checked_package.package_id in unchecked_keys:
                    unchecked_keys.remove(checked_package.package_id)
            if len(unchecked_keys) == 0:
                return packages
            else:
                next_package: Package = package_table.search(unchecked_keys.pop(0))
                return get_related_packages(next_package, unchecked_keys, packages)

        def can_load(package: Package) -> bool:
            # Return False unless the package passes all checks.
            if package in self.loaded_packages:
                return False
            if package.notes == '':
                return True
            elif notes_list[0].match(package.notes):
                truck_number: int = int(re.search(r'\d+', package.notes).group())
                if truck_number == self.truck_number:
                    return True
            elif notes_list[1].match(package.notes) or notes_list[2].match(package.notes):
                if self.route_number > 1:
                    return True
            elif notes_list[3].match(package.notes):
                packages = get_related_packages(package)
                if len(self.loaded_packages) <= (16 - len(packages)):
                    return True
            return False

        def load_nearest_packages(current_location: str):
            min_distance: float = -1
            for key in range(1, package_table.size+1):
                package: Package = package_table.search(key)
                distance: float = determine_distance(current_location, package.address)
                if (min_distance < 0 or distance < min_distance) and package.package_id is not None:
                    min_distance = distance
                    nearest_package: Package = package
            # noinspection PyUnboundLocalVariable
            if can_load(nearest_package):
                self.loaded_packages.append(nearest_package)
                nearest_package.set_status()
                package_table.remove(nearest_package.package_id)
            return nearest_package

        def load_related_packages(package: Package):
            related_packages = get_related_packages(package)
            for package in related_packages:
                self.loaded_packages.append(package)
                package.set_status()
                package_table.remove(package.package_id)
            return package

        def main():
            current_location: str = '4001 South 700 East'
            package = None
            while len(self.loaded_packages) < 16:
                if package is not None and notes_list[3].match(package.notes):
                    package = load_related_packages(package)
                else:
                    package = load_nearest_packages(current_location)
                current_location = package.address

        main()

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
