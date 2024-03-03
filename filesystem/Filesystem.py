from typing import *
from filesystem.Command import Command


class Node:
    def __init__(self, parent, children):
        self.parent = parent
        self.children = children


class TextFile:
    contents: str


File = Node | TextFile


class Filesystem:
    __root: Node
    __current_working_directory: Node

    def __init__(self):
        self.__root = Node(None, {})
        self.__current_working_directory = self.__root

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

    @staticmethod
    def need_args(args, n):
        if len(args) != n:
            return 'Wrong number of arguments'

    def __read(self, args) -> str:
        pass

    def __assist(self, args) -> str:
        return "skill issue (deleting all your files, please wait...)"

    def traverse(self, args) -> str:
        self.need_args(args, 1)
        new_cwd = self.locate_file(args[0])
        if new_cwd is None:
            return 'File not found'
        if isinstance(new_cwd, Node):
            self.__current_working_directory = new_cwd
        else:
            return "Can only traverse to a directory"

    def __relocate(self, args) -> str:
        self.need_args(args, 2)
        pass

    def __sudo(self, args) -> str:
        pass

    @staticmethod
    def validate_file_name(name: str) -> bool:
        return name not in ['', '.', '..'] and '/' not in name

    def locate_file(self, filename: str, cwd: Node = None) -> Optional[File]:
        if cwd is None:
            cwd = self.__current_working_directory
        if filename == '':
            raise ValueError('Empty filename')
        slash = filename.find('/')
        if slash == -1:
            slash = len(filename)
        match filename[:slash]:
            case '..':
                first = cwd
            case '.':
                first = cwd.parent
            case '':
                first = self.__root
            case name:
                first = name
        if slash == len(filename):
            return first
        else:
            return self.locate_file(filename[1 + slash:], first)
