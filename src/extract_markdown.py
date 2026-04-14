from markdown_to_html_node import markdown_to_html_node
import os

def extract_title(markdown):
    with open(markdown, "r") as f:
        for line in f:
            if line.startswith("# "):
                return line[2:].strip()
    raise Exception

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        from_content = f.read()
    with open(template_path, "r") as t:
        temp_content = t.read() 
        
        
        
        
        
    
    html_string = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_path)
    temp_content = temp_content.replace("{{ Title }}", title)
    temp_content = temp_content.replace("{{ Content }}", html_string)

    folder = os.path.dirname(dest_path)
    if dest_path:
        os.makedirs(folder, exist_ok=True)


    with open(dest_path, "w") as f:
        f.write(temp_content)


def generate_pages_recursive(dir_path, template_path, dest_dir_path):
    
    
    dir_path_content = os.listdir(dir_path)
    for content in dir_path_content:
        destnation_path = os.path.join(dest_dir_path, content)
        current_path = os.path.join(dir_path, content)

        if os.path.isdir(current_path):
            os.mkdir(destnation_path)
            generate_pages_recursive(current_path, template_path, destnation_path)
        else:
            if content.endswith(".md"):
                generate_page(current_path, template_path, f"{dest_dir_path}/{content[:-3]}.html")