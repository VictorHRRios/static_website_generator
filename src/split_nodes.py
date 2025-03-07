from textnode import TextNode, TextType
from extract import extract_markdown_links, extract_markdown_images
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            split_nodes = []
            new_node = old_node.text.split(delimiter)
            if len(new_node) % 2 == 0:
                raise Exception("invalid markdown syntax")
            for i in range(len(new_node)):
                if new_node[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(new_node[i], TextType.TEXT))
                else:
                    split_nodes.append(TextNode(new_node[i], text_type))
            new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if images == []:
            new_nodes.append(old_node)
            original_text = ''
            continue
        for image in images:
            image_alt, image_link = image
            new_node = original_text.split(f"![{image_alt}]({image_link})", 1)
            if len(new_node) != 2:
                raise ValueError("invalid markdown")
            if new_node[0] != '':
                new_nodes.append(TextNode(new_node[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGES, image_link))
            original_text = new_node[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(old_node.text)
        if links == []:
            new_nodes.append(old_node)
            continue
        for link in links:
            link_text, link_url = link
            new_node = original_text.split(f"[{link_text}]({link_url})", 1)
            if len(new_node) != 2:
                raise ValueError("invalid markdown")
            if new_node[0] != '':
                new_nodes.append(TextNode(new_node[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINKS, link_url))
            original_text = new_node[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    return nodes
