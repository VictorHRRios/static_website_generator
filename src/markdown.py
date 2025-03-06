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
            heading_number = type_of_heading(block)
            html_nodes = text_to_children(block[heading_number+1:].replace('\n', ' ')) # Remove new lines and handle inline
            block_node = ParentNode(f"h{heading_number}", html_nodes)
            return block_node
        case BlockType.CODE:
            block_node = ParentNode(block_type.value, [LeafNode('code', block[4:-3])])
            return block_node
        case BlockType.QUOTE:
            lines = block.split('\n')
            pars = []
            for line in lines:
                inline = text_to_children(line[1:].lstrip())
                pars.append(ParentNode('p', inline))
            block_node = ParentNode(block_type.value, pars)
            return block_node
        case BlockType.UNORDERED_LIST:
            lines = block.split('\n')
            unordered_list = []
            for line in lines:
                inline = text_to_children(line[2:])
                unordered_list.append(ParentNode('li', inline))
            block_node = ParentNode(block_type.value, unordered_list)
            return block_node
        case BlockType.ORDERED_LIST:
            lines = block.split('\n')
            ordered_list = []
            for line in lines:
                inline = text_to_children(line[3:])
                ordered_list.append(ParentNode('li', inline))
            block_node = ParentNode(block_type.value, ordered_list)
            return block_node
        case _:
            html_nodes = text_to_children(block.replace('\n', ' ')) # Remove new lines and handle inline
            block_node = ParentNode(BlockType.PARAGRAPH.value, html_nodes)
            return block_node

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
        block_node = block_to_html_node(block, block_type)
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