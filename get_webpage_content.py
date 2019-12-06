# Script: get_webpage_content.py
# Desc: Get Web Page Content
# Author: Chit Thae Naing
# Modified: Nov 29 2019 (PEP08)

# Use this module for reading the contents of url
import urllib.request
# Use this module for checking SSL certificate
import ssl
from global_var_config import *
from display_output import display


def get_webpage(url):
    """ Retrieve Web Page via url and return its content """

    # Not to do checking ssl certificate
    context = ssl._create_unverified_context()
    web_page_content = ''
    try:
        web_page_content = urllib.request.urlopen(url, context=context).read()
    except ValueError:
        display('[!] Web URL must be in full URL address (eg. https://www.chitthaenaing.me )', file=global_variables_config["output_file"])
    except Exception:
        display('[!] Web URL must be valid', file=global_variables_config["output_file"])

    return web_page_content


def main():
    """ Print the contents of the following web url """
    url = "http://www.soc.napier.ac.uk/~40009856/CW/"
    print(get_webpage(url))


if __name__ == '__main__':
    main()

