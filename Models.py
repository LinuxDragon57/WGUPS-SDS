from datetime import datetime, time
from enum import Enum

from run import determine_distance
from HashTable import HashTable


class Package:

    class Status(Enum):
        WAITING = 1
        MOVING = 2
        DELIVERED = 3
        LOST = 4

    delivery_status: Status = Status.WAITING

    def __init__(self, package_id: int = None, address: str = None, city: str = None, state: str = None,
                 zip_code: int = None, deadline: str = None, mass: str = None, notes: str = None):
        self.package_id: int = int(package_id)
        self.address: str = address
        self.city: str = city
        self.state: str = state
        self.zip_code: int = int(zip_code)
        if deadline == 'EOD':
            due = time(23, 59)
        else:
            due = datetime.strptime(deadline, "%I:%M %p").time()
        self.deadline = datetime.combine(datetime.today().date(), due)
        self.mass: int = int(mass)
        self.notes: str = notes

    def __hash__(self):
        return self.package_id

    def __repr__(self):
        return f"Package: {self.package_id}"

    def match_id(self, package_id) -> bool:
        return self.package_id == package_id

    def set_status(self):
        self.delivery_status = self.Status(self.delivery_status.value+1)


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

    def load_package(self, package: Package) -> bool:
        if len(self.loaded_packages) <= 16:
            self.loaded_packages.append(package)
            return True
        else:
            return False

    def load_packages(self, package_table: HashTable):
        pass
