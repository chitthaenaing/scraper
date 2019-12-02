# Script: Scraper.py
# Desc: Scraping, information gathering and forensic analysis on web page
# Author: Chit Thae Naing
# Modified: Nov 29 2019 (PEP08)

# Use this module for time duration of each process
import time
# Use this module for getting webpage content
from get_webpage_content import get_webpage
# Use this module for parsing paths
import os
# Use this module for hexing
import hashlib
# Use this module for web content forensic
from web_page_forensic import (
    get_hyperlinks,
    get_image_lists,
    get_document_lists,
    get_email_lists,
    get_phoneno_lists,
    get_md5hash_lists,
    dict_attack,
    check_file_extension,
    check_badfile
)

from download_file import download_file, preparing_download_folder

web_url = "http://www.soc.napier.ac.uk/~40009856/CW/"
# web_url = "http://www.napier.ac.uk"


def print_hyperlinks_info(result_info):
    """
        Print Hyperlinks Info
    """
    absolute_links, relative_links, total_links = result_info
    print(f'[*] {total_links} hyperlinks found!')
    print(f'[*] Absolute links: ')
    for index, hyperlink in enumerate(set(absolute_links)):
        print(f'\t[{index+1:2d}] {hyperlink} => {absolute_links.count(hyperlink)}')

    print(f'[x] Relative links: ')
    for index, hyperlink in enumerate(set(relative_links)):
        print(f'\t[{index+1:2d}] {hyperlink} => {relative_links.count(hyperlink)}')


def print_image_file_info(image_lists):
    """
        Print Image File Name
    """
    print(f'[*] {len(set(image_lists))} image files found!')
    print(f'[x] Image lists: ')
    for image_link, image_name in set(image_lists):
        print(f'\t{image_name} => {image_lists.count((image_link, image_name))}')


def print_document_info(doc_lists):
    """
        Print Document Info
    """
    print(f'[*] {len(set(doc_lists))} document files found!')
    print(f'[x] Document lists: ')
    for doc_link, doc_name in set(doc_lists):
        print(f'\t{doc_name} => {doc_lists.count((doc_link, doc_name))}')


def print_email_info(result_info):
    """
        Print Email Info
    """
    freetext_email_lists, mailto_email_lists, total_email_address = result_info
    print(f'[*] {total_email_address} email addresses found!')
    print(f'[x] FreeText Email lists: ')
    for email_address in set(freetext_email_lists):
        print(f'\t{email_address} => {freetext_email_lists.count(email_address)}')
    print(f'[x] Mailto Email lists: ')
    for email_address in set(mailto_email_lists):
        print(f'\t{email_address} => {mailto_email_lists.count(email_address)}')


def print_phoneno_info(phoneno_lists):
    """
        Print Phone Numbers
    """
    print(f'[*] {len(phoneno_lists)} phone numbers found!')
    print(f'[x] Phone Number lists: ')
    for phoneno in set(phoneno_lists):
        print(f'\t{phoneno} => {phoneno_lists.count(phoneno)}')


def print_md5hash_info(md5hash_lists):
    """
        Print md5 hash
    """
    print(f'[*] {len(md5hash_lists)} md5 hash found!')
    print(f'[x] md5 hash lists: ')
    for md5hash in set(md5hash_lists):
        print(f'\t{md5hash} => {md5hash_lists.count(md5hash)}')


def print_md5_crack_info(found_password_lists):
    """
        Print Found Password
    """
    print(f'[x] Found Password: ')
    for md5hash, found_pwd in found_password_lists:
        print(f'\t{md5hash} => {found_pwd}')


def print_format(heading, process_name, process_duration, result_info=()):
    """
        Results Format
    """
    heading_format = ''.join(['=' for _ in range(len(heading))])
    print(heading_format)
    print(heading)
    print(heading_format)
    print(f'[*] {process_name}:')
    print(f'[*] Finished {process_name} within {process_duration:.9f} seconds')

    if process_name == 'Searching hyperlinks':
        print_hyperlinks_info(result_info)
    elif process_name == 'Searching Image Files':
        print_image_file_info(result_info)
    elif process_name == 'Searching Document Files':
        print_document_info(result_info)
    elif process_name == 'Searching Email Address':
        print_email_info(result_info)
    elif process_name == 'Searching Phone Number':
        print_phoneno_info(result_info)
    elif process_name == 'Searching md5 hash':
        print_md5hash_info(result_info)
    elif process_name == 'Cracking md5 hash':
        print_md5_crack_info(result_info)


def main():
    """
        Display Informations and forensic analysis of the given url
    """

    # Getting Web Page Content
    retrieving_start = time.time()
    web_page_content = get_webpage(web_url)
    retrieving_end = time.time()
    print_format(
        'Getting Web Page Content',
        'Retrieving URL - ' + web_url,
        retrieving_end - retrieving_start
    )

    # Searching Hyperlinks
    searching_hyperlinks_start = time.time()
    hyperlinks_result = get_hyperlinks(web_page_content)
    searching_hyperlinks_end = time.time()
    print_format(
        'Getting Hyperlinks',
        'Searching hyperlinks',
        searching_hyperlinks_end - searching_hyperlinks_start,
        hyperlinks_result
    )

    # Searching Image Files
    searching_image_start = time.time()
    image_lists = get_image_lists(web_page_content)
    searching_image_end = time.time()
    print_format(
        'Getting Image File Lists',
        'Searching Image Files',
        searching_image_end - searching_image_start,
        image_lists
    )

    # Searching Document Files
    searching_document_start = time.time()
    doc_lists = get_document_lists(web_page_content)
    searching_document_end = time.time()
    print_format(
        'Getting Document Files',
        'Searching Document Files',
        searching_document_end - searching_document_start,
        doc_lists
    )

    # Searching Email Address
    searching_email_start = time.time()
    email_lists = get_email_lists(web_page_content)
    searching_email_end = time.time()
    print_format(
        'Getting Email Address',
        'Searching Email Address',
        searching_email_end - searching_email_start,
        email_lists
    )

    # Searching Phone Number
    searching_phoneno_start = time.time()
    phoneno_lists = get_phoneno_lists(web_page_content)
    searching_phoneno_end = time.time()
    print_format(
        'Getting Phone Number',
        'Searching Phone Number',
        searching_phoneno_end - searching_phoneno_start,
        phoneno_lists
    )

    # Searching md5 Hash
    searching_md5hash_start = time.time()
    md5hash_lists = get_md5hash_lists(web_page_content)
    searching_md5hash_end = time.time()
    print_format(
        'Getting md5 hash',
        'Searching md5 hash',
        searching_md5hash_end - searching_md5hash_start,
        md5hash_lists
    )

    # Cracking md5 hash with common passwords word lists
    cracking_md5hash_start = time.time()
    found_password_lists = dict_attack(set(md5hash_lists))
    cracking_md5hash_end = time.time()
    print_format(
        'Cracking md5 hash',
        'Cracking md5 hash',
        cracking_md5hash_end - cracking_md5hash_start,
        found_password_lists
    )

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
    for file_name in os.listdir(download_directory):
        with open(os.path.abspath(download_directory + os.sep + file_name), 'rb') as file:
            check_badfile(
                (
                    file_name, hashlib.md5(file.read()).hexdigest()
                ),
                os.getcwd() + os.sep + 'badfiles.txt'
            )
    print(f'[x] Finished Checking Bad files')


if __name__ == '__main__':
    main()
