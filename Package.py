from datetime import datetime, time
from enum import Enum


class Package:

    class Status(Enum):
        WAITING = 1
        EN_ROUTE = 2
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
        return f"<Package {self.package_id}>"

    def match_id(self, package_id) -> bool:
        return self.package_id == package_id

    def set_status(self):
        self.delivery_status = self.Status(self.delivery_status.value+1)
