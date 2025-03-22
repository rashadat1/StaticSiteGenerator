import os
from typing import Optional, List
import pathlib
import shutil

print(os.path.join(str(pathlib.Path(__file__).parent), "public"))

class FileTreeNode:
    """
    Represents a node in the file system tree. Each node corresponds to either 
    a file or a directory.

    Attributes:
        path (str): The absolute path of the file or directory.
        children (Optional[List["FileTreeNode"]]): List of child nodes 
            (empty for files, populated for directories).
    """
    def __init__(self, path: str, children: Optional[List["FileTreeNode"]]=None):
        """
        Initializes a FileTreeNode instance.

        Args:
            path (str): The absolute path of the file or directory.
            children (Optional[List["FileTreeNode"]], optional): List of child nodes. 
                Defaults to an empty list.
        """
        self.path = path
        self.children = children if children is not None else []

class Directory:
    """
    Represents a directory and its contents as a tree structure. 
    Provides methods to construct the file tree and copy files recursively.

    Attributes:
        source_path (str): The absolute path to the root of the source directory.
        root (FileTreeNode): Root node representing the source directory.
    """
    def __init__(self, source_path: str):
        """
        Initializes a Directory instance, creating the root FileTreeNode 
        and capturing its immediate children.

        Args:
            source_path (str): The absolute path of the source directory.
        """
        self.source_path = source_path
        children = [FileTreeNode(os.path.join(self.source_path, item)) for item in os.listdir(self.source_path)]

        self.root = FileTreeNode(self.source_path, children=children)
    

    def generate_file_structure(self) -> None:
        """
        Recursively traverses the directory structure starting from `self.source_path`
        and builds the file tree representation in memory.

        The method iterates through all subdirectories and files, creating 
        `FileTreeNode` objects to represent them.
        """

        def add_children(node: FileTreeNode) -> None:
            """
            Helper function to recursively add child nodes to a given directory node.

            Args:
                node (FileTreeNode): The directory node whose children should be populated.
            """
            node.children = [FileTreeNode(os.path.join(node.path,item)) for item in os.listdir(node.path)]
            sub_directories = list(filter(lambda kiddie_node: not os.path.isfile(kiddie_node.path), node.children))
            if not sub_directories:
                # base case: if no children are directories we can terminate the recursion
                return
            for directory_node in sub_directories:
                add_children(directory_node)
            return
        
        add_children(self.root)
        return


    def copy_to_dest(self, to_path: str):
        """
        Recursively copies the directory structure and its files from `source_path` to `to_path`.

        The method ensures:
        - Directories are created at `to_path` before copying files.
        - Files retain their metadata using `shutil.copy2()`.

        Args:
            to_path (str): The destination directory path where files will be copied.
        """
        stack = [(self.root, self.root.path)]

        while stack:
            curr, curr_path = stack.pop()
            if os.path.isfile(curr_path):
                # if a file we should copy to the new directory location
                print(f"Copying file at {curr_path} to {curr_path.replace(self.source_path, to_path)}")
                print()
                shutil.copy2(src=curr_path, dst=curr_path.replace(self.source_path, to_path))
            elif not os.path.isfile(curr_path) and os.path.exists(curr_path):
                # not a file and exists -> is a directory so create it
                print(f"Creating new directory {curr_path.replace(self.source_path, to_path)}")
                print()
                os.mkdir(curr_path.replace(self.source_path, to_path))

            for child in curr.children:
                stack.append((child,child.path))

def copy_to_public():
    """
    Deletes the existing `public/` directory (if it exists), recreates it, and 
    copies the entire `static/` directory structure into it.

    This function:
    - Computes the project root path dynamically.
    - Removes the `public/` directory to ensure a fresh copy.
    - Uses the `Directory` class to recursively copy all files.
    """
    project_directory = str(pathlib.Path(__file__).parent.parent)
    from_path = os.path.join(project_directory, "static")
    to_path = os.path.join(project_directory, "public")

    print(f"Deleting {to_path} to prepare for copying")
    print()
    shutil.rmtree(to_path)

    directory_tree = Directory(from_path)
    directory_tree.generate_file_structure() # create file tree structure in memory
    directory_tree.copy_to_dest(to_path) # recreate src directory file structure in dst

    print("Successfully completed src directory reconstruction")
