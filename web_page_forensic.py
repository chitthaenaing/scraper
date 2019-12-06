# Script: web_page_forensic.py
# Desc: Perform Forensic analysis on web content
# Author: Chit Thae Naing
# Modified: Nov 29 2019 (PEP08)

# Use this module for searching hyperlinks
import re
# Use this module for parsing image's path
import os
# Use this module for md5 hashing
import hashlib
# Use this module for converting hex value
import binascii
from display_output import display
from global_var_config import *


def get_hyperlinks(content):
    """ Search hyperlinks in the context and return them """

    # finding absolute links
    # Starts with https or http://
    # Starts with / (eg. /theme/folder/a.png ) or // (eg. //ajax.googleapis.com/)
    # Covers the special case like "/media/images/logos/ednapuni_red.png?h=60&amp;la=en&amp;w=215&amp;hash=39DC25ADF6177FF9A1AEB6F9D09B30F47FE593E2"
    # absolute_pattern = r'https?://[\w\-\./]+|(?<=[\'\"])/[.\S]*(?=[\'\"])'
    absolute_pattern = r'(?<=[\'\"])https?://[.\S]*(?=[\'\"])|(?<=[\'\"])/[.\S]*(?=[\'\"])'
    absolute_links = re.findall(absolute_pattern, content.decode())
    absolute_links.sort()

    # finding relative links
    # Starts with characters - a.jpg or folder_one/a.jpg
    # Starts with dots - ./folder/a.jpg or ../folder/a.jpg
    # Covers the special case like "ednapuni_red.png?h=60&amp;la=en&amp;w=215&amp;hash=39DC25ADF6177FF9A1AEB6F9D09B30F47FE593E2"

    relative_pattern = r'(?<=[\'\"])([\w\-\(\)\%]+\.[\w\-\%\&\=\;\?]+|[\w\-\.]+/+.*?)(?=[\'\"])'
    relative_links = re.findall(relative_pattern, content.decode())
    relative_links.sort()

    return (
        absolute_links,
        relative_links,
        len(absolute_links) + len(relative_links)
    )


def get_image_lists(content):
    """
        Search Image files on web content and return them
    """
    absolute_links, relative_links, _ = get_hyperlinks(content)
    image_extension_lists = [
        '.jpg',
        '.JPG',
        '.jpeg',
        '.JPEG',
        '.png',
        '.PNG',
        '.gif',
        '.GIF',
        '.bmp',
        '.BMP'
    ]
    return [
            (link, os.path.basename(link)) for link in absolute_links
            for img_ext in image_extension_lists
            if link.find(img_ext) > -1
        ] + [
            (link, os.path.basename(link)) for link in relative_links
            for img_ext in image_extension_lists
            if link.find(img_ext) > -1
        ]


def get_document_lists(content):
    """
        Search document files on web content and return them
    """
    absolute_links, relative_links, _ = get_hyperlinks(content)
    doc_ext_list = [
        'docx',
        'pdf'
    ]
    return [
            (link, os.path.basename(link)) for link in absolute_links
            for doc_ext in doc_ext_list
            if link.find(doc_ext) > -1
        ] + [
            (link, os.path.basename(link)) for link in relative_links
            for doc_ext in doc_ext_list
            if link.find(doc_ext) > -1
        ]


def get_email_lists(content):
    """ Searching Email Address and return them """
    freetext_email_pattern = r'(?<!mailto:)[\w\.\-]+@[\w\.\-]+\.\w+'
    freetext_email_lists = re.findall(freetext_email_pattern, content.decode())

    mailto_email_pattern = r'(?<=mailto:)[\w\.\-]+@[\w\.\-]+\.\w+'
    mailto_email_lists = re.findall(mailto_email_pattern, content.decode())

    return (
        freetext_email_lists,
        mailto_email_lists,
        len(freetext_email_lists) + len(mailto_email_lists)
    )


def get_phoneno_lists(content):
    """ Searching Phone Number and return them """
    phoneno_pattern = r'\+?\d{1,3}[\s\-]?\(?\d\)?[\d\-\s]{6,12}(?:\d)'
    phoneno_lists = re.findall(phoneno_pattern, content.decode())
    return phoneno_lists


def get_md5hash_lists(content):
    """ Searching md5 hash and return them """
    md5_pattern = r'[\da-f]{32}'
    md5hash_lists = re.findall(md5_pattern, content.decode())
    return md5hash_lists


def dict_attack(hash_lists, word_lists_txt):
    """Checks password hash, against a dictionary of password lists"""

    found_pwd_lists = []
    for md5_hash in hash_lists:
        found_pwd = ''
        try:
            with open(word_lists_txt, 'rb') as word_list_file:
                for pwd in word_list_file.readlines():
                    if hashlib.md5(pwd.strip()).hexdigest() == md5_hash:
                        found_pwd = pwd.strip().decode()
                        break
                if found_pwd == '':
                    found_pwd = 'no matching password found'

                found_pwd_lists.append(
                    (md5_hash, found_pwd)
                )

        except IOError as err:
            display(f'[-] File Error {err} - {word_lists_txt} cannot be opened', file=global_variables_config["output_file"])

    return found_pwd_lists


def main():
    """ Get lists of hyperlinks found in the content """
    content = b'<!Doctype html><html><head><title>Chit Thae Naing</title></head><body><h1>Welcome to my site</h1></body></html>'
    print(get_hyperlinks(content))


if __name__ == '__main__':
    main()
