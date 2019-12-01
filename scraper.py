# Script: Scraper.py
# Desc: Scraping, information gathering and forensic analysis on web page
# Author: Chit Thae Naing
# Modified: Nov 29 2019 (PEP08)

# Use this module for time duration of retrieving Web Contents
import time
# Use this module for getting webpage content
from get_webpage_content import get_webpage
import os
import hashlib
# Use this module for web content forensic
from web_page_forensic import get_hyperlinks, get_image_lists, get_document_lists, get_email_lists, get_phoneno_lists, get_md5hash_lists, dict_attack, check_file_extension, check_badfile
from download_file import download_file, preparing_download_folder


def main():
    """
        Display Informations and forensic analysis of the given url
    """

    web_url = "http://www.soc.napier.ac.uk/~40009856/CW/"
    # web_url = "http://www.napier.ac.uk"
    print(f'[*] Retrieving URL - {web_url}')
    retrieving_start = time.time()
    web_page_content = get_webpage(web_url)
    retrieving_end = time.time()
    print(f'[*] Finished retrieving web contents within {retrieving_end - retrieving_start} seconds')
    # Searching Hyperlinks
    print(f'[*] Searching Hyperlinks')
    searching_start = time.time()
    absolute_links, relative_links, total_links = get_hyperlinks(web_page_content)
    searching_end = time.time()
    print(f'[*] Finished Searching hyperlinks within {searching_end - searching_start} seconds')
    print(f'[*] {total_links} hyperlinks found!')
    print(f'[*] Absolute links: ')
    for index, hyperlink in enumerate(set(absolute_links)):
        print(f'\t[{index+1:2d}] {hyperlink} => {absolute_links.count(hyperlink)}')

    print(f'[x] Relative links: ')
    for index, hyperlink in enumerate(set(relative_links)):
        print(f'\t[{index+1:2d}] {hyperlink} => {relative_links.count(hyperlink)}')
    
    # Searching Image Files
    print(f'[x] Searching Image Files: ')
    searching_image_start = time.time()
    image_lists = get_image_lists(web_page_content)
    searching_image_end = time.time()
    print(f'[*] Finished Searching image files within {searching_image_end - searching_image_start} seconds')
    print(f'[*] {len(set(image_lists))} image files found!')
    print(f'[x] Image lists: ')
    for image_link, image_name in set(image_lists):
        print(f'\t{image_name} => {image_lists.count((image_link, image_name))}')

    # Searching Document Files
    print(f'[x] Searching Document Files: ')
    searching_document_start = time.time()
    doc_lists = get_document_lists(web_page_content)
    searching_document_end = time.time()
    print(f'[*] Finished Searching document files within {searching_document_end - searching_document_start} seconds')
    print(f'[*] {len(set(doc_lists))} document files found!')
    print(f'[x] Document lists: ')
    for doc_link, doc_name in set(doc_lists):
        print(f'\t{doc_name} => {doc_lists.count((doc_link, doc_name))}')
    
    # Searching Email Address
    print(f'[x] Searching Email Address: ')
    searching_email_start = time.time()
    freetext_email_lists, mailto_email_lists, total_email_address = get_email_lists(web_page_content)
    searching_email_end = time.time()
    print(f'[*] Finished Searching email address within {searching_email_end - searching_email_start} seconds')
    print(f'[*] {total_email_address} email addresses found!')
    print(f'[x] FreeText Email lists: ')
    for email_address in set(freetext_email_lists):
        print(f'\t{email_address} => {freetext_email_lists.count(email_address)}')
    print(f'[x] Mailto Email lists: ')
    for email_address in set(mailto_email_lists):
        print(f'\t{email_address} => {mailto_email_lists.count(email_address)}')

    # Searching Phone Number
    print(f'[x] Searching Phone Number: ')
    searching_phoneno_start = time.time()
    phoneno_lists = get_phoneno_lists(web_page_content)
    searching_phoneno_end = time.time()
    print(f'[*] Finished Searching phone number within {searching_phoneno_end - searching_phoneno_start} seconds')
    print(f'[*] {len(phoneno_lists)} phone numbers found!')
    print(f'[x] Phone Number lists: ')
    for phoneno in set(phoneno_lists):
        print(f'\t{phoneno} => {phoneno_lists.count(phoneno)}')
    
    # Searching md5 Hash
    print(f'[x] Searching md5 hash: ')
    searching_md5hash_start = time.time()
    md5hash_lists = get_md5hash_lists(web_page_content)
    searching_md5hash_end = time.time()
    print(f'[*] Finished Searching md5 hash within {searching_md5hash_end - searching_md5hash_start} seconds')
    print(f'[*] {len(md5hash_lists)} md5 hash found!')
    print(f'[x] md5 hash lists: ')
    for md5hash in set(md5hash_lists):
        print(f'\t{md5hash} => {md5hash_lists.count(md5hash)}')
    

    # Cracking md5 hash with common passwords word lists
    print(f'[x] Cracking md5 hash: ')
    cracking_md5hash_start = time.time()
    found_password_lists = dict_attack(set(md5hash_lists))
    cracking_md5hash_end = time.time()
    print(f'[*] Finished Cracking md5 hash within {cracking_md5hash_end - cracking_md5hash_start} seconds')
    print(f'[x] Found Password: ')
    for md5hash, found_pwd in found_password_lists:
        print(f'\t{md5hash} => {found_pwd}')

    # Download Files
    print(f'[x] Preparing Folder for downloading')
    download_directory = 'download'
    preparing_download_folder(download_directory)
    print(f'[x] Finished setting up download folder')
    print(f'[x] Downloading Files: ')
    for file_link, file_name in image_lists + doc_lists:
    
        if not file_link.startswith("http"):
            file_link = web_url + file_link
        
        if file_name in [os.path.basename(file) for file in os.scandir(download_directory)]:
            file_name = os.path.splitext(file_name)[0] + '_' + str(id(file_name)) + os.path.splitext(file_name)[1]

        download_file(file_link, file_name, download_directory)

    # Checking File type
    for file in os.listdir(download_directory):
        check_file_extension(os.path.abspath(download_directory + os.sep + file))

    # Checking Badfile
    print(f'[x] Checking Bad files')
    for file in os.listdir(download_directory):
        check_badfile(hashlib.md5(file.encode()).hexdigest(), os.getcwd() + os.sep + 'badfiles.txt')
    print(f'[x] Finished Checking Bad files')

if __name__ == '__main__':
    main()
