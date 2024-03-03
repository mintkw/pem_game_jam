from enum import Enum


class Command(Enum):
    READ = "rd"
    ASSIST = "assist"
    TRAVERSE = "trv"
    RELOCATE = "rlc"
    SUDO = "iamgod"
    NOCOMMAND = "none"
    SHOWALL = "shwall"

    def __str__(self):
        return f'{self.value}'
