from typing import *
from filesystem.Command import Command


class Node:
    name: str

    def __init__(self, name: str, parent, children):
        self.name = name
        self.parent = parent
        self.children = children


class TextFile:
    name: str
    parent: Node
    contents: str

    def __init__(self, name: str, parent: Node, contents: str):
        self.name = name
        self.parent = parent
        self.contents = contents


File = Node | TextFile


class Filesystem:
    __root: Node
    __current_working_directory: (str, Node)

    def __init__(self, root_children: Callable[[Node], Dict[str, File]]):
        self.__root = Node('', None, {})
        self.__root.children = root_children(self.__root)
        self.__current_working_directory = ("", self.__root)

    def call_command(self, command: str) -> str:
        """
        :param command:
        :return: (new working directory, output)
        """
        (command_type, args) = self.__parse_command(command)
        match command_type:
            case Command.NOCOMMAND:
                return self.__no_command(command_in=command.split()[0])
            case Command.READ:
                return self.__read(args)
            case Command.ASSIST:
                return self.__assist(args)
            case Command.TRAVERSE:
                return self.__traverse(args)
            case Command.RELOCATE:
                return self.__relocate(args)
            case Command.SUDO:
                return self.__sudo(args)

    @staticmethod
    def __parse_command(command: str) -> Tuple[Command, List[str]]:
        cmds = command.split()
        try:
            return Command(cmds[0]), cmds[1:]
        except:
            return Command.NOCOMMAND, cmds[1:]

    @staticmethod
    def __no_command(command_in) -> str:
        return f"koopa: command not found: {command_in}"

    @staticmethod
    def need_args(args, n):
        if len(args) != n:
            return 'Wrong number of arguments'

    def __read(self, args) -> str:
        """ :param args: args[0] filename.txt """
        filename = args[0]
        _, current_node = self.__current_working_directory
        return current_node.children[filename].contents

    @staticmethod
    def __assist(args) -> str:
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

    @classmethod
    def compute_cwd_str(cls, cwd: Node) -> str:
        if cwd.parent is None:
            return ''
        return cls.compute_cwd_str(cwd.parent) + '/' + cwd.name

    def __traverse(self, args) -> str:
        """ :param args: args[0] new working directory """
        self.need_args(args, 1)
        new_cwd = self.locate_file(args[0])
        if new_cwd is None:
            return 'File not found'
        if isinstance(new_cwd, Node):
            self.__current_working_directory = (Filesystem.compute_cwd_str(new_cwd), new_cwd)
        else:
            return "Can only traverse to a directory"

    def __relocate(self, args) -> str:
        """ :param args: args[0] dst args[1] src """
        self.need_args(args, 2)
        dst = self.locate_file(args[0])
        if dst is None:
            return 'Destination directory not found'
        if not isinstance(dst, Node):
            return 'Destination must be a directory'
        src = self.locate_file(args[1])
        if src is None:
            return 'Source file not found'
        del src.parent[src.name]
        dst.children[src.name] = src
        return 'Success'

    @staticmethod
    def __sudo(_args) -> str:
        return 'Denied (error code: MERE_MORTAL)'

    @staticmethod
    def validate_file_name(name: str) -> bool:
        return name not in ['', '.', '..'] and '/' not in name

    def cwd(self) -> str:
        return self.__current_working_directory[0]

    def locate_file(self, filename: str, cwd: Node = None) -> Optional[File]:
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
