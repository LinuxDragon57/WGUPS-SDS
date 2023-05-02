import re

notes_list = [
    re.compile(r"Can only be on truck \d+", re.IGNORECASE),
    re.compile(r"Delayed on flight---will not arrive to depot until 9:05 am", re.IGNORECASE),
    re.compile(r"Wrong address listed", re.IGNORECASE),
    re.compile(r"Must be delivered with [\d+, ]+", re.IGNORECASE),
]