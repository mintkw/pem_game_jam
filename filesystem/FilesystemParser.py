import json
from filesystem.Filesystem import *
from cryptography.fernet import Fernet


class FilesystemParser:
    def parse_json(self, filename) -> Filesystem:
        with open(filename) as f:
            filesys_json = json.load(f)
            return Filesystem(
                lambda root, key: {k: self.__file_from_json(Fernet(key), root, k, v) for k, v in filesys_json.items()})

    def __file_from_json(self, cipher_suite, parent, name, json_node) -> File:
        if isinstance(json_node, str):
            if name.endswith('.exe'):
                return Executable(name, parent, None if json_node == '' else json_node)
            if name.startswith('enc_'):
                json_node = cipher_suite.encrypt(json_node.encode()).decode()
            return TextFile(name, parent, json_node, 0)
        elif isinstance(json_node, dict):
            if json_node.keys() == {'permission', 'content'}:
                if name.startswith('enc_'):
                    json_node['content'] = cipher_suite.encrypt(json_node['content'].encode()).decode()
                return TextFile(name, parent, json_node['content'], json_node['permission'])
            node = Node(name, parent, {})
            for child_name, child in json_node.items():
                node.children[child_name] = self.__file_from_json(cipher_suite, node, child_name, child)
            return node
        else:
            raise ValueError("AAAAAAAAAAA")
