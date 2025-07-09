import os
import shutil

DOCS_PATH = os.path.join(os.path.dirname(__file__), "../docs")
STATIC_PATH = os.path.join(os.path.dirname(__file__), "../static")

def copy_static_to_docs():
    recreate_public_directory()
    create_sub_directories(STATIC_PATH, DOCS_PATH)
    

def recreate_public_directory():
    if os.path.exists(DOCS_PATH):
        shutil.rmtree(DOCS_PATH)
    os.mkdir(DOCS_PATH)

def create_sub_directories(parent_static_directory, parent_public_directory):
    sub_directories = os.listdir(parent_static_directory)
    for sub in sub_directories:
        sub_static_path = os.path.join(parent_static_directory, sub)
        sub_public_path = os.path.join(parent_public_directory, sub)
        if os.path.isfile(sub_static_path):
            shutil.copy(sub_static_path, sub_public_path)
        else:
            os.mkdir(sub_public_path)
            create_sub_directories(sub_static_path, sub_public_path)

    