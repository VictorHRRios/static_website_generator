from enum import Enum
import re
from htmlnode import ParentNode, LeafNode, HTMLNode
from split_nodes import text_to_textnodes, TextNode, TextType, split_nodes_delimiter
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "pre"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    blocks = list(filter(lambda block: block != '', map(lambda block: "\n".join(map(lambda line: line.strip(), block.strip().strip('\n').split('\n'))), blocks)))
    return blocks

def isHeading(block):
    return re.match(r"^#{1,6} w*",block)

def isCode(block):
    return block[:3] == "```" and block[-3:] == "```"

def isQuote(block):
    lines = block.split('\n')
    for line in lines:
        if line[0] != '>':
            return False
    return True

def isUnOrderedList(block):
    lines = block.split('\n')
    for line in lines:
        if line[:2] != '- ':
            return False
    return True

def isOrderedList(block):
    lines = block.split('\n')
    for line in range(1, len(lines)+1):
        if lines[line-1][:3] != f"{line}. ":
            return False
    return True

def block_to_block_type(block):
    if isHeading(block):
        return BlockType.HEADING
    elif isCode(block):
        return BlockType.CODE
    elif isQuote(block):
        return BlockType.QUOTE
    elif isUnOrderedList(block):
        return BlockType.UNORDERED_LIST
    elif isOrderedList(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def block_to_html_node(block, block_type):
    #nodes = [TextNode(block, TextType.TEXT)]
    match block_type:
        case BlockType.HEADING:
            return []
        case BlockType.CODE:
            return [LeafNode('code', block[4:-3])]
        case BlockType.QUOTE:
            return []
        case BlockType.UNORDERED_LIST:
            lines = block.split('\n')
            unordered_list = []
            for line in lines:
                unordered_list.append(LeafNode('li', line[2:]))
            return unordered_list
        case BlockType.ORDERED_LIST:
            lines = block.split('\n')
            unordered_list = []
            for line in lines:
                unordered_list.append(LeafNode('li', line[3:]))
            return unordered_list
        case BlockType.PARAGRAPH:
            return []

def type_of_heading(heading_text):
    number = 1
    while (heading_text[number] == '#'):
        number +=1
    return number


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    blocks_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            heading_number = type_of_heading(block)
            block_node = ParentNode(f"h{heading_number}", None)
        else:
            block_node = ParentNode(block_type.value, None)
        block_parent_nodes = block_to_html_node(block, block_type)
        # if it is a paragraph or a quote
        if block_parent_nodes == []:
            if block_type == BlockType.QUOTE:
                html_nodes = text_to_children(block.replace('> ', '').replace('\n', ' ')) # Remove new lines and handle inline
            elif block_type == BlockType.HEADING:
                html_nodes = text_to_children(block[heading_number+1:].replace('\n', ' ')) # Remove new lines and handle inline
            else:
                html_nodes = text_to_children(block.replace('\n', ' ')) # Remove new lines and handle inline
            block_node.children = html_nodes
        else:
            if block_type == BlockType.CODE:
                block_parent_nodes = block_to_html_node(block, block_type) # Handle as final leaf node
            else:
                for block_parent_node in block_parent_nodes:
                    html_nodes = text_to_children(block_parent_node.value) # Attach inline to every other type
                    block_parent_node.children = html_nodes
            block_node.children = block_parent_nodes
        blocks_nodes.append(block_node)
    parent = ParentNode("div", blocks_nodes)
    return parent


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        text_node = text_node_to_html_node(text_node)
        html_nodes.append(text_node)
    return html_nodes