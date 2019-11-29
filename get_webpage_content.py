# Script: get_webpage_content.py
# Desc: Get Web Page Content
# Author: Chit Thae Naing
# Modified: Nov 29 2019 (PEP08)

# Use this module for reading the contents of url
import urllib.request

def get_webpage(url):
    """Retrieve Web Page via url and return its content"""
    try:
        web_page = urllib.request.urlopen(url)
    
    except ValueError:
        print('[!] Web URL must be in full URL address (eg. https://www.chitthaenaing.me )')
    
    except Exception:
        print('[x] Web URL must be valid')

def main():
    """Print the contents of the following web url""" 
    web_url = "http://www.soc.napier.ac.uk/~40009856/CW/"
    print(get_webpage(url))


if __name__ == '__main__':
    main()

