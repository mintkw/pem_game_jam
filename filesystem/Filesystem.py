import typing


class Node:
    def __init__(self, parent, children):
        self.parent = parent
        self.children = children


class TextFile:
    contents: str


class Filesystem:
    def __init__(self):
        self.__root = Node(None, {})
        self.__current_working_directory = self.__root

    @staticmethod
    def validate_file_name(name: str) -> bool:
        return name not in ['', '.', '..'] and '/' not in name

    def locate_file(self, filename: str, cwd: Node = None) -> typing.Optional[Node]:
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
