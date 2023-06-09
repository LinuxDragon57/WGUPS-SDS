from datetime import datetime, time, timedelta
from enum import Enum


class PackageStatus(Enum):
    WAITING = 1
    EN_ROUTE = 2
    DELIVERED = 3
    LOST = 4


class Package:

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

    def __hash__(self):
        return self.package_id

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

    def match_id(self, package_id) -> bool:
        return self.package_id == package_id

    def set_status(self):
        self.delivery_status = PackageStatus(self.delivery_status.value+1)

    def set_delivery_time(self, delivery_time: timedelta):
        self.delivery_time = delivery_time

    def set_deliverer(self, truck_number: int):
        self.deliverer = truck_number
