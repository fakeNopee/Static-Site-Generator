from textnode import *
import os
import shutil
from extract_markdown import *


def initiate(source = "./static", destination = "public"):

    if destination == "public":
        if os.path.exists(destination):
            shutil.rmtree("public")
        os.makedirs("public")


    for copy in os.listdir(source):
        copy_source = os.path.join(source, copy)
        copy_destination = os.path.join(destination, copy)

        if os.path.isdir(copy_source):
            os.mkdir(copy_destination)
            initiate(copy_source, copy_destination)
        else:
            shutil.copy(copy_source, copy_destination)
            print(f"copying {copy_source} ---> {copy_destination}")



def main():
    initiate()
    generate_pages_recursive("content", "template.html", "public")


































main()