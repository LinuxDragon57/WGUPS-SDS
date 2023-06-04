import re
from datetime import timedelta

from Package import Package
from run import determine_distance
from HashTable import HashTable
from static.environment import notes_list


class Truck:

    def __init__(self, truck_number: int):
        self.truck_number = truck_number
        self.payload: list[Package] = list()
        self.route_number: int = 1
        self.total_distance: float = 0
        self.time_elapsed: timedelta = timedelta()

    def determine_next_delivery(self, current_location: str) -> Package:
        min_distance: float = -1
        next_delivery = None
        for package in self.payload:
            distance: float = determine_distance(current_location, package.address)
            if min_distance < 0 or distance < min_distance:
                min_distance = distance
                next_delivery = package
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
            if package in self.payload:
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
                if len(self.payload) <= (16 - len(packages)):
                    return True
            return False

        def load_package(package: Package):
            self.payload.append(package)
            package.set_status()
            package_table.remove(package.package_id)

        def load_related_packages(package: Package) -> Package:
            related_packages: list[Package] = get_related_packages(package)
            for package in related_packages:
                load_package(package)
            return package

        def load_nearest_package(current_location: str, not_loadable: list[Package]) -> tuple[str, list[Package]]:
            min_distance: float = -1
            nearest_package = None
            for key in range(1, package_table.size + 1):
                package: Package = package_table.search(key)
                if package is not None:
                    distance: float = determine_distance(current_location, package.address)
                    if distance != 0 and (min_distance < 0 or distance < min_distance):
                        min_distance = distance
                        nearest_package = package
            if nearest_package is not None:
                loadable: bool = can_load(nearest_package)
                if loadable and not notes_list[3].match(nearest_package.notes):
                    load_package(nearest_package)
                elif loadable and notes_list[3].match(nearest_package.notes):
                    nearest_package = load_related_packages(nearest_package)
                elif not loadable:
                    not_loadable.append(nearest_package)
                    package_table.remove(nearest_package.package_id)

            return nearest_package.address, not_loadable

        def execute():
            current_location: str = "4001 South 700 East"
            not_loadable: list[Package] = list()
            while True:
                load_size: int = len(self.payload)
                if load_size == 16 or package_table.is_empty():
                    for package in not_loadable:
                        package_table.insert(package)
                    break
                else:
                    current_location, not_loadable = load_nearest_package(current_location, not_loadable)

        execute()

    def deliver_packages(self, delivered_packages: HashTable) -> HashTable:
        current_location: str = "4001 South 700 East"
        while True:
            package: Package = self.determine_next_delivery(current_location)
            if package is not None:
                distance: float = determine_distance(current_location, package.address)
                self.total_distance += distance
                delivery_time = distance / 18
                self.time_elapsed += timedelta(hours=delivery_time)
                package.set_delivery_time(self.time_elapsed)
                package.set_status()
                current_location = package.address
                delivered_packages.insert(package)
                self.payload.remove(package)
            if len(self.payload) == 0:
                break
        distance: float = determine_distance(current_location, '4001 South 700 East')
        self.total_distance += distance
        delivery_time = distance / 18
        self.time_elapsed += timedelta(hours=delivery_time)
        self.route_number += 1
        return delivered_packages
