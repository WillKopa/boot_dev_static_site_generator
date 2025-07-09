from src.copy_static_to_public import copy_static_to_public
from src.generate_page import generate_page

CONTENT_SOURCE = "content/index.md"
DESTINATION_PATH = "public/index.html"
TEMPLATE_SOURCE = "template.html"

def main():
    copy_static_to_public()
    generate_page(CONTENT_SOURCE, TEMPLATE_SOURCE, DESTINATION_PATH)

if __name__ == "__main__":
    main()