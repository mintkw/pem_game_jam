class Node:
    def __init__(self, parent, children):
        self.__parent = parent
        self.__children = children

class Filesystem:
    def __init__(self):
        self.__root = Node(None, )
        self.__current_working_directory =