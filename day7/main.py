"""
Advent of Code 2022, Day 7
No Space Left On Device
https://adventofcode.com/2022/day/7
"""

from os import path
from typing import NamedTuple, Optional, Protocol

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"

MAX_DIRECTORY_SIZE = 100000
ROOT_DIRECTORY = "/"


class File(NamedTuple):
    """Represents a file in the filesystem."""

    name: str
    size: int


class Directory(NamedTuple):
    """Represents a directory in the filesystem."""

    name: str
    size: int


class ChangeDirectory(NamedTuple):
    """Represents a change of directory in the filesystem."""

    directory: str


class ListDirectory(NamedTuple):
    """Represents a listing of the contents of a directory in the filesystem."""

    files: list[File]
    subdirectories: list[str]


Command = ChangeDirectory | ListDirectory


class FilesystemNode(Protocol):
    """Represents a node in the filesystem."""

    name: str
    size: int
    parent: Optional["FilesystemNode"]

    @property
    def depth(self) -> int:
        """Get the depth of the node in the filesystem."""

        return self.parent.depth + 1 if self.parent else 0


class DirectoryNode(FilesystemNode):
    """Represents a directory node in the filesystem."""

    def __init__(self, name: str, parent: Optional["DirectoryNode"] = None) -> None:
        """Create a new directory node."""

        self.name = name
        self.parent = parent

        self.files: dict[str, FileNode] = {}
        self.subdirectories: dict[str, DirectoryNode] = {}

    @property
    def size(self) -> int:
        """Get the total size of the directory and its contents."""

        total_file_size = sum(file.size for file in self.files.values())
        total_subdirectory_size = sum(
            subdirectory.size for subdirectory in self.subdirectories.values()
        )

        return total_file_size + total_subdirectory_size

    def add_file(self, file: File) -> None:
        """Add a file to the directory."""

        self.files[file.name] = FileNode(file, parent=self)

    def add_subdirectory(self, directory: str) -> None:
        """Add a subdirectory to the directory."""

        self.subdirectories[directory] = DirectoryNode(directory, parent=self)

    def __str__(self) -> str:
        """Create a string representation of the directory node for printing."""

        padding = " " * self.depth
        self_repr = f"{padding}- {self.name}: ({self.size})"
        if not self.files and not self.subdirectories:
            return self_repr

        children_reprs = [
            f"\n{str(child)}"
            for child in (*self.files.values(), *self.subdirectories.values())
        ]
        children_repr = "".join(children_reprs)

        return f"{self_repr}{children_repr}"

    def __repr__(self) -> str:
        """Create a string representation of the directory node for debugging."""

        return f"DirectoryNode({self.name})"


class FileNode(FilesystemNode):
    """Represents a file node in the filesystem."""

    def __init__(self, file: File, parent: Optional[DirectoryNode] = None) -> None:
        """Create a new file node."""

        self.file = file
        self.parent = parent

    @property
    def name(self) -> str:
        """Get the name of the file."""

        return self.file.name

    @property
    def size(self) -> int:
        """Get the size of the file."""

        return self.file.size

    def __str__(self) -> str:
        """Create a string representation of the file node for printing."""

        padding = " " * self.depth
        return f"{padding}- {self.name}: ({self.size})"

    def __repr__(self) -> str:
        """Create a string representation of the file node for debugging."""

        return f"FileNode({self.name}, {self.size})"


class Filesystem:
    """Represents the filesystem as a whole."""

    def __init__(self, root: FilesystemNode) -> None:
        """Create a new filesystem."""

        self.root = root

    def __str__(self) -> str:
        """Create a string representation of the filesystem for printing."""

        return str(self.root)


def read_terminal_output(file_path: str) -> list[Command]:
    """Read the terminal output from a file as a list of commands."""

    with open(file_path, encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]

    commands = []
    index = 0
    while index < len(lines):
        line = lines[index]
        segments = line.split()
        command_type = segments[1]

        index += 1
        if command_type == "cd":
            directory = segments[2]
            commands.append(ChangeDirectory(directory))
            continue

        files = []
        subdirectories = []

        while index < len(lines) and not lines[index].startswith("$"):
            segments = lines[index].split()
            if segments[0] == "dir":
                subdirectories.append(segments[1])
            else:
                size = int(segments[0])
                name = segments[1]
                files.append(File(name, size))
            index += 1

        commands.append(ListDirectory(files, subdirectories))

    return commands


def recreate_filesystem(commands: list[str]) -> Filesystem:
    """Recreate the filesystem from the commands in the terminal output."""

    # NOTE: We assume the first command is always a change of directory to the root.
    # Since the root directory will never normally be a subdrectory, we create a
    # temporary sentinel node to act as the parent of the root directory so that
    # we can handle all commands in a uniform manner.

    head_node = DirectoryNode("TEMP")
    head_node.add_subdirectory(ROOT_DIRECTORY)

    current_node: DirectoryNode = head_node

    for command in commands:
        match command:
            case ChangeDirectory(directory):
                if directory == "..":
                    current_node = current_node.parent
                else:
                    current_node = current_node.subdirectories[directory]
            case ListDirectory(files, subdirectories):
                for file in files:
                    current_node.add_file(file)
                for subdirectory in subdirectories:
                    current_node.add_subdirectory(subdirectory)

    filesystem = Filesystem(head_node.subdirectories[ROOT_DIRECTORY])
    return filesystem


def find_directories_with_max_total_size(
    filesystem: Filesystem,
    maximum_total_size: int,
) -> list[Directory]:
    """Find all directories of a size of at most the given maximum total size."""

    def find_directories(node: DirectoryNode) -> list[Directory]:
        directories = []
        if node.size <= maximum_total_size:
            directories.append(Directory(node.name, node.size))

        for subdirectory in node.subdirectories.values():
            directories.extend(find_directories(subdirectory))

        return directories

    return find_directories(filesystem.root)


def sum_directory_sizes(directories: list[Directory]) -> int:
    """Sum the sizes of all directories."""

    return sum(directory.size for directory in directories)


def main() -> None:
    """Read terminal output from a file and process the filesystem it describes."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    commands = read_terminal_output(file_path)

    filesystem = recreate_filesystem(commands)
    print(filesystem)

    small_directories = find_directories_with_max_total_size(
        filesystem,
        MAX_DIRECTORY_SIZE,
    )
    small_directories_total_size = sum_directory_sizes(small_directories)
    print(
        f"The total size of all directories with at most {MAX_DIRECTORY_SIZE} bytes:",
        small_directories_total_size,
    )


if __name__ == "__main__":
    main()
