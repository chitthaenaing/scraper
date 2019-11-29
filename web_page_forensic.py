# Script: web_page_forensic.py
# Desc: Perform Forensic analysis on web content
# Author: Chit Thae Naing
# Modified: Nov 29 2019 (PEP08)

# Use this module for searching hyperlinks
import re


def get_hyperlinks(content):
    """ Search hyperlinks in the context and return them """

    # finding absolute links
    absolute_links = re.findall(r'https?://[\w\-\./]+|(?<=[\'\"])/[\w\-\./]*(?=[\'\"])', content.decode())
    absolute_links.sort()
    return absolute_links


def main():
    """ Get lists of hyperlinks found in the content """
    content = b'<!Doctype html><html><head><title>Chit Thae Naing</title></head><body><h1>Welcome to my site</h1></body></html>'
    print(get_hyperlinks(content))


if __name__ == '__main__':
    main()

