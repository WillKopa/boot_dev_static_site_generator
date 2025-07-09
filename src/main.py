import os
import sys

from src.copy_static_to_public import copy_static_to_docs
from src.generate_page import generate_pages

HOME_SOURCE = "content"
DESTINATION_PATH = "docs"
TEMPLATE_SOURCE = "template.html"

def main():
    base_path = sys.argv[0] if sys.argv[0] else "/"
    copy_static_to_docs()
    generate_pages(HOME_SOURCE, TEMPLATE_SOURCE, DESTINATION_PATH, base_path)

if __name__ == "__main__":
    main()