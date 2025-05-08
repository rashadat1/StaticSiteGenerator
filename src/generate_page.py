import re
from blocktype import markdown_to_html_node
import os
def extract_title(markdown: str) -> str:
    """
    Extracts the title from a Markdown string.

    The title is assumed to be the first level-1 Markdown heading (starting with '#').

    Args:
        markdown (str): The Markdown content.

    Returns:
        str: The extracted title text.

    Raises:
        Exception: If no valid title heading is found in the Markdown content.
    """
    matchgroup = re.findall(r"^[#]([^#].+)", markdown, re.MULTILINE)
    if matchgroup:
        return matchgroup[0].strip()
    else:
        raise Exception("Incorrect Format: Missing header")

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    """
    Generates a single HTML page from a Markdown file using a provided template.

    This function:
        - Reads the Markdown content.
        - Converts the Markdown to HTML.
        - Extracts the page title from the Markdown.
        - Injects the title and HTML content into the template.
        - Writes the final HTML page to the destination path.

    Args:
        from_path (str): Path to the Markdown file.
        template_path (str): Path to the HTML template file containing {{ Title }} and {{ Content }} placeholders.
        dest_path (str): Destination path where the generated HTML page will be saved.

    Returns:
        None
    """
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
    print("Page Title: " + page_title)
    new_template = template.replace("{{ Title }}", page_title).replace("{{ Content }}", html_string)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    print("Saving updated template!")
    with open(dest_path, "w") as f:
        f.write(new_template)

    print("Static page created")

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    """
    Recursively generates HTML pages from a directory of Markdown files.

    This function traverses the source directory, converts each Markdown file into an HTML page
    using the provided template, and replicates the folder structure in the destination directory.

    Args:
        dir_path_content (str): Path to the source directory containing Markdown files (and possibly subdirectories).
        template_path (str): Path to the HTML template file.
        dest_dir_path (str): Path to the destination directory where the generated HTML pages will be saved.

    Returns:
        None
    """
    if not os.path.isfile(dir_path_content) and os.path.exists(dir_path_content): 
        content = [file for file in os.listdir(dir_path_content)]
        for file in content:
            if os.path.isfile(os.path.join(dir_path_content, file)):
                if os.path.splitext(os.path.join(dir_path_content, file))[1] == '.md':
                    generate_page(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, os.path.splitext(file)[0] + ".html"))
            else:
                os.makedirs(os.path.join(dest_dir_path, file), exist_ok=True)
                generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))
        return
    else:
        return
