from typing import *
from filesystem.Command import Command


class Node:
    def __init__(self, parent, children):
        self.__parent = parent
        self.__children = children

class Filesystem:
    def __init__(self):
        self.__root = Node(None, )
        self.__current_working_directory =

    def call_command(self, command: str) -> str:
        (command_type, args) = self.__parse_command(command)
        match command_type:
            case Command.NOCOMMAND:
                pass
            case Command.READ:
                pass
            case Command.ASSIST:
                pass
            case Command.TRAVERSE:
                pass
            case Command.RELOCATE:
                pass
            case Command.SUDO:
                pass

    def __parse_command(self, command: str) -> Tuple[Command, List[str]]:
        cmds = command.split()
        try:
            return Command(cmds[0]), cmds[1:]
        except:
            return Command.NOCOMMAND, cmds[1:]

    def __no_command(self, command_in) -> str:
        return f"koopa: command not found: {command_in}"

    def __read(self, args) -> str:
        pass

    def __assist(self, args) -> str:
        pass

    def __traverse(self, args) -> str:
        pass

    def __relocate(self, args) -> str:
        pass

    def __sudo(self, args) -> str:
        pass