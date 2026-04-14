from textnode import *
import os
import shutil
from extract_markdown import *
import sys

def initiate(source = "./static", destination = "docs"):

    if destination == "docs":
        if os.path.exists(destination):
            shutil.rmtree("docs")
        os.makedirs("docs")


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
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    generate_pages_recursive("content", "template.html", "docs", basepath)

































main()