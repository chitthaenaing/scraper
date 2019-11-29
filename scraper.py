# Script: Scraper.py
# Desc: Scraping, information gathering and forensic analysis on web page
# Author: Chit Thae Naing
# Modified: Nov 29 2019 (PEP08)

# Use this module for time duration of retrieving Web Contents
import time
# Use this module for getting webpage content
from get_webpage_content import get_webpage

# Use this module for finding Hyperlinks
from web_page_forensic import get_hyperlinks


def main():
    """Display Informations and forensic analysis of the given url"""
    web_url = "http://www.soc.napier.ac.uk/~40009856/CW/"
    # web_url = "http://www.napier.ac.uk"
    print(f'[*] Retrieving URL - {web_url}')
    start = time.time()
    web_page_content = get_webpage(web_url)
    end = time.time()
    print(f'[*] Finish retrieving web contents within {end - start} seconds')

    print(f'[*] Searching Hyperlinks')
    for index, hyperlinks in enumerate(get_hyperlinks(web_page_content)):
        print(f'\t[{index+1:2d}] {hyperlinks}')
    

if __name__ == '__main__':
    main()
