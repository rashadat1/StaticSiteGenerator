import re
from blocktype import markdown_to_html_node
import os

def extract_title(markdown: str):
    matchgroup = re.findall(r"^[#]([^#].+)", markdown, re.MULTILINE)
    if matchgroup:
        return matchgroup[0].strip()
    else:
        raise Exception("Incorrect Format: Missing header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    print()
    print(f"Reading markdown file at {from_path}")
    with open(from_path, 'r') as f:
        markdown = f.read()
    print()
    print(f"Reading template file from {template_path}")
    with open(template_path, 'r') as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()

    page_title = extract_title(markdown)

    new_template = template.replace("{{ Title }}", page_title)
    new_template = template.replace("{{ Content }}", html_string)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    print("Saving updated template!")
    with open(dest_path, "w") as f:
        f.write(new_template)

    print("Static page created")

