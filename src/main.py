from copy_to_public import copy_to_public
from generate_page import generate_pages_recursive
import os
import pathlib

def main():
    copy_to_public()
    project_directory = str(pathlib.Path(__file__).parent.parent)
    generate_pages_recursive(dir_path_content = os.path.join(project_directory, "content"), template_path = os.path.join(project_directory, "template.html"), dest_dir_path = os.path.join(project_directory, "public"))
    

main()
