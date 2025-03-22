import os
from typing import Optional, List
import pathlib
import shutil

print(os.path.join(str(pathlib.Path(__file__).parent), "public"))

class FileTreeNode:
    def __init__(self, path: str, children: Optional[List["FileTreeNode"]]=None):
        self.path = path
        self.children = children if children is not None else []

class Directory:
    def __init__(self, source_path: str):
        self.source_path = source_path
        children = [FileTreeNode(os.path.join(self.source_path, item)) for item in os.listdir(self.source_path)]

        self.root = FileTreeNode(self.source_path, children=children)
    

    def generate_file_structure(self) -> None:

        def add_children(node: FileTreeNode) -> None:
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
        stack = [(self.root, self.root.path)]

        while stack:
            curr, curr_path = stack.pop()
            if os.path.isfile(curr_path):
                # if a file we should copy to the new directory location
                print(f"Copying file at {curr_path} to {curr_path.replace(self.source_path, to_path)}")
                shutil.copy2(src=curr_path, dst=curr_path.replace(self.source_path, to_path))
            elif not os.path.isfile(curr_path) and os.path.exists(curr_path):
                # not a file and exists -> is a directory so create it
                print(f"Creating new directory {curr_path.replace(self.source_path, to_path)}")
                os.mkdir(curr_path.replace(self.source_path, to_path))

            for child in curr.children:
                stack.append((child,child.path))

def copy_to_public():
    project_directory = str(pathlib.Path(__file__).parent)
    from_path = os.path.join(project_directory, "static")
    to_path = os.path.join(project_directory, "public")

    print(f"Deleting {to_path} to prepare for copying")
    shutil.rmtree(to_path)
    os.mkdir(to_path)
    print(f"Finished deleting and creating fresh {to_path} directory")

    directory_tree = Directory(from_path)
    directory_tree.generate_file_structure() # create file tree structure in memory
    directory_tree.copy_to_dest(to_path) # recreate src directory file structure in dst

    print("Successfully completed src directory reconstruction")









