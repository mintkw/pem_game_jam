import json
from filesystem.Filesystem import Filesystem


class FilesystemParser:
    def parse_json(self, filename) -> Filesystem:
        with open(filename) as f:
            filesys_json = json.load(f)
            Filesystem()
            self.__construct_filesys()

    def __construct_filesys(self, curr_node, dictionary) -> Filesystem:
        for x in dictionary:
            if isinstance(dictionary[x], str):
                return