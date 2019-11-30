# Script: web_page_forensic.py
# Desc: Perform Forensic analysis on web content
# Author: Chit Thae Naing
# Modified: Nov 29 2019 (PEP08)

# Use this module for searching hyperlinks
import re


def get_hyperlinks(content):
    """ Search hyperlinks in the context and return them """

    # finding absolute links
    absolute_pattern = r'https?://[\w\-\./]+|(?<=[\'\"])/[.\S]*(?=[\'\"])'
    absolute_links = re.findall(absolute_pattern, content.decode())
    absolute_links.sort()

    # finding relative links
    relative_pattern = r'(?<=[\'\"])([\w\-\(\)]+\.[\w\-\%\&\=\;\?]+|[\./]*[\w\-]+/+.*?)(?=[\'\"])'
    relative_links = re.findall(relative_pattern, content.decode())
    relative_links.sort()

    return (
        {"absolute_links": absolute_links},
        {"relative_links": relative_links},
        {"total_links": len(absolute_links) + len(relative_links)}
    )


def main():
    """ Get lists of hyperlinks found in the content """
    content = b'<!Doctype html><html><head><title>Chit Thae Naing</title></head><body><h1>Welcome to my site</h1></body></html>'
    print(get_hyperlinks(content))


if __name__ == '__main__':
    main()

