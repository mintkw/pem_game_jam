from filesystem.Filesystem import Filesystem


class Executables:
    fs: Filesystem

    def __init__(self, fs):
        self.fs = fs

    def decrypt(self, node) -> str:
        node.decrypt_all(node, self.fs.get_key())
        return "Successfully decrypted the files."