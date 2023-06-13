from datetime import datetime, time, timedelta
from enum import Enum


# Defines an enumeration of all the possible delivery status states of the package.
class PackageStatus(Enum):
    WAITING = 1
    EN_ROUTE = 2
    DELIVERED = 3
    LOST = 4


# Class that holds all the package data.
class Package:

    # The constructor initializes package data from the CSV file as well as data that is either derived
    # from that data or used later as the program generates new data about a package.
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
        self.delivery_status: PackageStatus = PackageStatus.WAITING
        self.delivery_time = None
        self.deliverer = None

    # Since Python's built-in hash() function calls this method,
    # the Package object can redefine how it is hashed.
    def __hash__(self):
        return self.package_id

    # Redefines the string representation of the Package object.
    def __repr__(self):
        return f"""
        {'-'*75}
        Package {self.package_id}
        {'-'*15}
        Delivery Address: 
        \t{self.address}
        \t{self.city}, {self.state} {self.zip_code}
        Weight: {self.mass} pounds
        Deadline: {self.deadline}
        """

    # Automatically set the status of the Package object without requiring any positional arguments.
    def set_status(self):
        self.delivery_status = PackageStatus(self.delivery_status.value+1)

    # Sets the delivery_time of the Package object to the time specified in the parameter.
    def set_delivery_time(self, delivery_time: timedelta):
        self.delivery_time = delivery_time

    # Takes in the integer id of the Truck that delivered the package.
    def set_deliverer(self, truck_number: int):
        self.deliverer = truck_number
