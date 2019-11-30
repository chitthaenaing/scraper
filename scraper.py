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
    retrieving_start = time.time()
    web_page_content = get_webpage(web_url)
    retrieving_end = time.time()
    print(f'[*] Finish retrieving web contents within {retrieving_end - retrieving_start} seconds')

    print(f'[*] Searching Hyperlinks')
    
    searching_start = time.time()
    absolute_links, relative_links, total_links = get_hyperlinks(web_page_content)
    searching_end = time.time()
    
    print(f'[*] Finish Searching hyperlinks within {searching_end - searching_start} seconds')
    print(f'[*] {total_links["total_links"]} hyperlinks found!')
    print(f'[*] Absolute links: ')
    for index, hyperlink in enumerate(set(absolute_links["absolute_links"])):
        print(f'\t[{index+1:2d}] {hyperlink} => {absolute_links["absolute_links"].count(hyperlink)}')
    
    print(f'[x] Relative links: ')
    for index, hyperlink in enumerate(set(relative_links["relative_links"])):
        print(f'\t[{index+1:2d}] {hyperlink} => {relative_links["relative_links"].count(hyperlink)}')
    

if __name__ == '__main__':
    main()
