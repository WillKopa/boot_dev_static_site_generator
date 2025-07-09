from src.copy_static_to_public import copy_static_to_public
from src.generate_page import generate_pages
import os

HOME_SOURCE = "content"
DESTINATION_PATH = "public"
TEMPLATE_SOURCE = "template.html"

def main():
    copy_static_to_public()
    generate_pages(HOME_SOURCE, TEMPLATE_SOURCE, DESTINATION_PATH)

if __name__ == "__main__":
    main()