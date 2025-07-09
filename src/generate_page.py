from src.markdown_to_html import markdown_to_html_node
from src.extract_title import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        from_path_content = file.read()

    with open(template_path, "r") as file:
        template_content = file.read()

    title = extract_title(from_path_content)
    html = markdown_to_html_node(from_path_content).to_html()
    filled_template = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html)

    with open(dest_path, "w") as file:
        file.write(filled_template)
