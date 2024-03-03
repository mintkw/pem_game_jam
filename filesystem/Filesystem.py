import typing

class Filesystem:
    class Node:
        def __init__(self, parent, children):
            self.__parent = parent
            self.__children = children

    def __init__(self):
        self.__root =
        self.__current_working_directory =