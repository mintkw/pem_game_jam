from typing import *
from filesystem.Command import Command


class Node:
    def __init__(self, parent, children):
        self.parent = parent
        self.children = children


class TextFile:
    contents: str


class Filesystem:
    def __init__(self):
        self.__root = Node(None, {})
        self.__current_working_directory = ("/", self.__root)

    def call_command(self, command: str) -> (str, str):
        """
        :param command:
        :return: (new working directory, output)
        """
        (command_type, args) = self.__parse_command(command)
        match command_type:
            case Command.NOCOMMAND:
                return self.__cwd(), self.__no_command(command_in=command.split()[0])
            case Command.READ:
                return self.__cwd(), self.__read(args)
            case Command.ASSIST:
                return self.__cwd(), self.__assist(args)
            case Command.TRAVERSE:
                return self.__cwd(), self.__traverse(args)
            case Command.RELOCATE:
                return self.__cwd(), self.__relocate(args)
            case Command.SUDO:
                return self.__cwd(), self.__sudo(args)

    def __parse_command(self, command: str) -> Tuple[Command, List[str]]:
        cmds = command.split()
        try:
            return Command(cmds[0]), cmds[1:]
        except:
            return Command.NOCOMMAND, cmds[1:]

    def __no_command(self, command_in) -> str:
        return f"koopa: command not found: {command_in}"

    def __read(self, args) -> str:
        """ :param args: args[0] filename.txt """
        filename = args[0]
        _, current_node = self.__current_working_directory
        return current_node.children[filename].contents

    def __assist(self, args) -> str:
        """ :param args: args[0] 'please'"""
        if not ("please" in args[0].lower()):
            return "koopa: say pretty please!"
        return """
        rd [textfile] -- read textfile
        assist please -- help manual
        trv [directory] -- traverse the file system
        rlc [filename] [new_directory] -- move file to new directory
        god [cmd] -- run a command in god mode
        """

    def __traverse(self, args) -> str:
        pass

    def __relocate(self, args) -> str:
        pass

    def __god(self, args) -> str:
        pass

    @staticmethod
    def validate_file_name(name: str) -> bool:
        return name not in ['', '.', '..'] and '/' not in name

    def __cwd(self) -> str:
        return self.__current_working_directory[0]

    def locate_file(self, filename: str, cwd: Node = None) -> Optional[Node]:
        if cwd is None:
            _, cwd = self.__current_working_directory
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
