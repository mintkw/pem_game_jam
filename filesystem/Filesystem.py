from typing import *
from filesystem.Command import Command
from cryptography.fernet import Fernet


class Node:
    name: str

    def __init__(self, name: str, parent, children):
        self.name = name
        self.parent = parent
        self.children = children

    def decrypt_all(self, key: bytes):
        cipher_suite = Fernet(key)
        for child_name, child in list(self.children.items()):
            if isinstance(child, Node):
                child.decrypt_all(key)
            elif isinstance(child, TextFile) and child_name.startswith('enc_'):
                new_child = TextFile(child_name[4:], self, cipher_suite.decrypt(child.contents.encode()).decode(),
                                     child.permission_level)
                del self.children[child_name]
                self.children[new_child.name] = new_child


class TextFile:
    name: str
    parent: Node
    contents: str
    permission_level: int

    def __init__(self, name: str, parent: Node, contents: str, permission_level: int):
        self.name = name
        self.parent = parent
        self.contents = contents
        self.permission_level = permission_level


class Executable:
    name: str
    parent: Node
    password: Optional[str]

    def __init__(self, name: str, parent: Node, password: Optional[str]):
        self.name = name
        self.parent = parent
        self.password = password

    def run(self, password: Optional[str], fs) -> str:
        if self.password is not None and self.password != password:
            return f"Permission denied. Try running this file as ../{self.name} [password]"
        match self.name[:-4]:
            case 'DecryptPass':
                fs.locate_file('/Documents/passwords').decrypt_all(fs.get_key())
                return 'Success'
            case s if s.startswith('Findings'):
                n = int(s[8:])
                if f'findings{n}.txt' not in self.parent.children:
                    return 'Missing required dependency. Try moving the dependency to this folder.'
                del self.parent.children[f'findings{n}.txt']
                fs.locate_file(f'/Documents/findings{n}').decrypt_all(fs.get_key())
                del self.parent.children[self.name]
                return 'Success'
            case s:
                raise ValueError(f'Unrecognised executable: {s}')


class RequiresMoreArgs(Exception):
    pass


File = Node | TextFile | Executable


class Filesystem:
    __key: bytes
    __root: Node
    __current_working_directory: (str, Node)
    __perms: int

    def __init__(self, root_children: Callable[[Node, bytes], Dict[str, File]]):
        self.__key = Fernet.generate_key()
        self.__root = Node('', None, {})
        self.__root.children = root_children(self.__root, self.__key)
        self.__current_working_directory = ("", self.__root)
        self.__perms = 0

    def get_key(self):
        return self.__key

    def grant_perms(self, perms: int):
        self.__perms = max(perms, self.__perms)

    def call_command(self, command: str) -> str:
        """
        :param command:
        :return: (new working directory, output)
        """
        if command == '':
            return ''
        if command.startswith('./') or command.startswith('../'):
            args = command[1+command.index('/'):].split()
            executable = self.locate_file(args[0])
            if executable is None:
                return 'koopa: file not found.'
            if not isinstance(executable, Executable):
                return f'koopa: file is not executable: {executable.name}.'
            if len(args) not in [1, 2]:
                return f'{executable.name}: too many arguments.'
            password = args[1] if len(args) == 2 else None
            return executable.run(password, self)
        (command_type, args) = self.__parse_command(command)
        try:
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
                case Command.SHOWALL:
                    return self.__showall(args)
        except RequiresMoreArgs as e:
            return e.args[0]

    def decrypt_all(self):
        self.__root.decrypt_all(self.__key)

    @staticmethod
    def __parse_command(command: str) -> Tuple[Command, List[str]]:
        cmds = command.split()
        try:
            return Command(cmds[0]), cmds[1:]
        except:
            return Command.NOCOMMAND, cmds[1:]

    @staticmethod
    def __no_command(command_in) -> str:
        return f"koopa: command not found: {command_in}. Try running `assist`."

    @staticmethod
    def need_args(args, n):
        if len(args) != n:
            raise RequiresMoreArgs(f"Wrong number of arguments. Requires {n} arguments.")

    def __read(self, args) -> str:
        """ :param args: args[0] filename.txt """
        self.need_args(args, 1)
        filename = args[0]
        file = self.locate_file(filename)
        if not file:
            return f"koopa: no such filename {filename}."
        if not isinstance(file, TextFile):
            return f"koopa: not a text file."
        if self.__perms < file.permission_level:
            return f"koopa: permission denied."
        return file.contents

    def __showall(self, args):
        if len(args) == 0:
            currnode = self.__current_working_directory[1]
        else:
            self.need_args(args, 1)
            currnode = self.locate_file(args[0])
            if not currnode:
                return f'koopa: file not found {args[0]}.'
            if not isinstance(currnode, Node):
                return f'koopa: not a directory.'
        children_ls = []
        for child in currnode.children:
            children_ls.append(child)
        return "  ".join(children_ls)

    # def __run(self, args) -> str:
    #     """:param args: args[0] password if any"""
    #     if len(args) > 1:
    #         self.need_args(args, 1)
    #     filename = args[0]
    #     _, current_node = self.__current_working_directory
    #     executable = current_node.children.get(filename)
    #     if not executable:
    #         return f"koopa: no such executable {executable}"
    #     if not args[1:]:
    #         return executable.run(None, self)
    #     else:
    #         self.need_args(args, 2)
    #         return executable.run(args[1], self)

    @staticmethod
    def __assist(args) -> str:
        """ :param args: args[0] 'please'"""
        if len(args) == 0 or "please" not in args[0].lower():
            return "koopa: say pretty please!"
        return """
        rd [textfile] -- read textfile
        assist please -- help manual
        trv [directory] -- traverse the file system
            trv . -- traverse to previous directory
            trv .. -- traverse to current directory
        shwall -- show the contents of the current directory
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
            return ''
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
        del src.parent.children[src.name]
        dst.children[src.name] = src
        return 'Success'

    def __sudo(self, _args) -> str:
        self.grant_perms(1)
        return f"Permissions given. Permission level now {self.__perms}."

    @staticmethod
    def validate_file_name(name: str) -> bool:
        return name not in ['', '.', '..'] and '/' not in name and ' ' not in name

    def cwd(self) -> str:
        return self.__current_working_directory[0]

    def locate_file(self, filename: str, cwd: Node = None) -> Optional[File]:
        if cwd is None:
            _, cwd = self.__current_working_directory
        if filename == '':
            return cwd
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
                first = cwd.children.get(name)
                if first is None:
                    return None
        if slash == len(filename):
            return first
        else:
            return self.locate_file(filename[1 + slash:], first)
