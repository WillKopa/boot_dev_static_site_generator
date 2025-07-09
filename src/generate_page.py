import os
import shutil

from src.markdown_to_html import markdown_to_html_node
from src.extract_title import extract_title

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        from_path_content = file.read()

    with open(template_path, "r") as file:
        template_content = file.read()

    title = extract_title(from_path_content)
    html = markdown_to_html_node(from_path_content).to_html()
    filled_template = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html)
    filled_template.replace('href="/', f'href="{base_path}')
    filled_template.replace('src="/', f'src="{base_path}')

    with open(dest_path, "w") as file:
        file.write(filled_template)

def generate_pages(source_directory, template_path, destination_directory, base_path):
    sub_directories = os.listdir(source_directory)
    if not os.path.isdir(source_directory):
        os.mkdir(source_directory)
    if not os.path.isdir(destination_directory):
        os.mkdir(destination_directory)

    for sub in sub_directories:
        sub_source_path = os.path.join(source_directory, sub)
        sub_destination_path = os.path.join(destination_directory, sub)
        if os.path.isfile(sub_source_path):
            if (sub_source_path.endswith(".md")):
                generate_page(sub_source_path, template_path, sub_destination_path.rstrip(".md") + ".html", base_path)
        else:
            os.mkdir(sub_destination_path)
            generate_pages(sub_source_path, template_path, sub_destination_path, base_path)
