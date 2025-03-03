from textnode import *
import os
import shutil
from markdown import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        md_content = file.read()
    with open(template_path, 'r') as file:
        template_content = file.read()
    html_str = markdown_to_html_node(md_content).to_html()
    title_str = extract_title(md_content)
    template_content = template_content.replace("{{ Title }}", title_str)
    template_content = template_content.replace("{{ Content }}", html_str)
    with open(dest_path, "w") as text_file:
        text_file.write(template_content)


    


def copy_contents(source, destination):
    if not os.path.exists(source):
        raise Exception("directory to copy from don't exist")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    list_of_files = os.listdir(source)
    for file in list_of_files:
        source_file = os.path.join(source, file)
        destination_file = os.path.join(destination, file)
        if os.path.isfile(source_file):
            shutil.copy(source_file, destination_file)
        else:
            os.mkdir(destination_file)
            copy_contents(source_file, destination_file)

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line[:2] == "# ":
            return line
    raise Exception("No header")
    
def main():
    #sample = TextNode("this is a text node", TextType.BOLD, 'https://www.boot.dev')
    copy_contents("static", "public")
    generate_page("content/index.md", 'template.html', 'public/index.html')
    
    

if __name__ == "__main__":
    main()