from copy_to_public import copy_to_public
from generate_page import generate_page
import os
import pathlib

def main():
    copy_to_public()
    project_directory = str(pathlib.Path(__file__).parent.parent)
    generate_page(from_path = os.path.join(project_directory, "content", "index.md"), template_path = os.path.join(project_directory, "template.html"), dest_path = os.path.join(project_directory, "public/index.html"))
    

main()
