import json
from filesystem.Filesystem import *


class FilesystemParser:
    def parse_json(self, filename) -> Filesystem:
        with open(filename) as f:
            filesys_json = json.load(f)
            return Filesystem(lambda root: {k: self.__file_from_json(root, k, v) for k, v in filesys_json.items()})

    def __file_from_json(self, parent, name, json_node) -> File:
        if isinstance(json_node, str):
            return TextFile(name, parent, json_node)
        elif isinstance(json_node, dict):
            node = Node(name, parent, {})
            for child_name, child in json_node.items():
                node.children[child_name] = self.__file_from_json(node, child_name, child)
            return node
        else:
            raise ValueError("AAAAAAAAAAA")
