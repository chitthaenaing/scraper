# Script: display_format.py
# Desc: How to display the information of each process
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
    dict_attack
)
from global_var_config import global_variables_config
from download_file import download_files
from check_files import (
    check_file_extension_indir,
    check_badfile_indir,
    check_file_content_similarity_indir
)
from display_output import display


def print_hyperlinks_info(result_info):
    """
        Print Hyperlinks Info
    """
    absolute_links, relative_links, total_links = result_info
    display(f'[*] {total_links} hyperlinks found!', global_variables_config['output_file'])
    display(f'[*] Absolute links: ', global_variables_config['output_file'])

    for index, hyperlink in enumerate(set(absolute_links)):
        display(f'\t[{index+1:2d}] {hyperlink} => {absolute_links.count(hyperlink)}', file=global_variables_config['output_file'])

    display(f'[x] Relative links: ', file=global_variables_config["output_file"])
    for index, hyperlink in enumerate(set(relative_links)):
        display(f'\t[{index+1:2d}] {hyperlink} => {relative_links.count(hyperlink)}', file=global_variables_config['output_file'])


def print_image_file_info(image_lists):
    """
        Print Image File Name
    """
    display(f'[*] {len(set(image_lists))} image files found!', file=global_variables_config['output_file'])
    display(f'[x] Image lists: ', file=global_variables_config['output_file'])
    for image_link, image_name in set(image_lists):
        display(f'\t{image_name} => {image_lists.count((image_link, image_name))}', file=global_variables_config['output_file'])


def print_document_info(doc_lists):
    """
        Print Document Info
    """
    display(f'[*] {len(set(doc_lists))} document files found!', file=global_variables_config['output_file'])
    display(f'[x] Document lists: ', file=global_variables_config['output_file'])
    for doc_link, doc_name in set(doc_lists):
        display(f'\t{doc_name} => {doc_lists.count((doc_link, doc_name))}', global_variables_config['output_file'])


def print_email_info(result_info):
    """
        Print Email Info
    """
    freetext_email_lists, mailto_email_lists, total_email_address = result_info
    display(f'[*] {total_email_address} email addresses found!', file=global_variables_config["output_file"])
    display(f'[x] FreeText Email lists: ', file=global_variables_config["output_file"])
    for email_address in set(freetext_email_lists):
        display(f'\t{email_address} => {freetext_email_lists.count(email_address)}', file=global_variables_config["output_file"])
    display(f'[x] Mailto Email lists: ', file=global_variables_config["output_file"])
    for email_address in set(mailto_email_lists):
        display(f'\t{email_address} => {mailto_email_lists.count(email_address)}', file=global_variables_config["output_file"])


def print_phoneno_info(phoneno_lists):
    """
        Print Phone Numbers
    """
    display(f'[*] {len(phoneno_lists)} phone numbers found!', file=global_variables_config["output_file"])
    display(f'[x] Phone Number lists: ', file=global_variables_config["output_file"])
    for phoneno in set(phoneno_lists):
        display(f'\t{phoneno} => {phoneno_lists.count(phoneno)}', file=global_variables_config["output_file"])


def print_md5hash_info(md5hash_lists):
    """
        Print md5 hash
    """
    display(f'[*] {len(md5hash_lists)} md5 hash found!', file=global_variables_config["output_file"])
    display(f'[x] md5 hash lists: ', file=global_variables_config["output_file"])
    for md5hash in set(md5hash_lists):
        display(f'\t{md5hash} => {md5hash_lists.count(md5hash)}', file=global_variables_config["output_file"])


def print_md5_crack_info(found_password_lists):
    """
        Print Found Password
    """
    display(f'[x] Found Password: ')
    for md5hash, found_pwd in found_password_lists:
        display(f'\t{md5hash} => {found_pwd}', file=global_variables_config["output_file"])


def print_downloaded_files_info(downloaded_files_results):
    """
        Print Downloaded Files Info
    """
    display('[x] Downloading Files: ', file=global_variables_config["output_file"])
    for download_file_result in downloaded_files_results:
        file_name = download_file_result["file_name"]
        error_message = download_file_result.get("error_message")
        display(f'\t[*] Finished downloading {file_name}', file=global_variables_config["output_file"])
        if error_message is not None:
            display(f'\t[-] {file_name} - {error_message}')


def getting_webpage_content(web_url):
    start = time.time()
    global_variables_config["web_page_content"] = get_webpage(web_url)
    end = time.time()
    return {
        'process_duration': end - start
    }


def getting_hyperlinks(web_page_content):
    start = time.time()
    hyperlinks_result = get_hyperlinks(web_page_content)
    end = time.time()
    return {
        'results': hyperlinks_result,
        'process_duration': end - start
    }


def getting_image_lists(web_page_content):
    start = time.time()
    global_variables_config["image_lists"] = get_image_lists(web_page_content)
    end = time.time()
    return {
        'results': global_variables_config["image_lists"],
        'process_duration': end - start
    }


def getting_document_lists(web_page_content):
    start = time.time()
    global_variables_config["doc_lists"] = get_document_lists(web_page_content)
    end = time.time()
    return {
        'results': global_variables_config["doc_lists"],
        'process_duration': end - start
    }


def getting_email_address(web_page_content):
    start = time.time()
    email_lists = get_email_lists(web_page_content)
    end = time.time()
    return {
        'results': email_lists,
        'process_duration': end - start
    }


def getting_phone_number(web_page_content):
    start = time.time()
    phoneno_lists = get_phoneno_lists(web_page_content)
    end = time.time()
    return {
        'results': phoneno_lists,
        'process_duration': end - start
    }


def getting_md5_hash_lists(web_page_content):
    start = time.time()
    global_variables_config["md5hash_lists"] = get_md5hash_lists(web_page_content)
    end = time.time()
    return {
        'results': global_variables_config["md5hash_lists"],
        'process_duration': end - start
    }


def getting_cracked_md5_hash_results(md5hash_lists, password_file):
    start = time.time()
    found_password_lists = dict_attack(set(md5hash_lists), password_file)
    end = time.time()
    return {
        'results': found_password_lists,
        'process_duration': end - start
    }


def downloading_files(file_lists):
    start = time.time()
    download_files(file_lists)
    end = time.time()
    return {
        'process_duration': end - start
    }


def checking_file_extension_indir(directory):
    start = time.time()
    check_file_extension_indir(directory)
    end = time.time()
    return {
        'process_duration': end - start
    }


def checking_badfile_indir(directory, bad_file):
    start = time.time()
    check_badfile_indir(directory, bad_file)
    end = time.time()
    return {
        'process_duration': end - start
    }


def checking_file_content_similarity(directory):
    start = time.time()
    check_file_content_similarity_indir(directory)
    end = time.time()
    return {
        'process_duration': end - start
    }


def print_process_format(heading, process_name, params):
    """
        Print Process Format
    """
    heading_format = ''.join(['=' for _ in range(len(heading))])
    display(heading_format, file=global_variables_config["output_file"])
    display(heading, file=global_variables_config["output_file"])
    display(heading_format, file=global_variables_config["output_file"])
    if "URL" in params.keys():
        display(f'[*] {process_name} - {params["URL"]}:')
    else:
        display(f'[*] {process_name}:')

    if process_name == 'Retrieving URL':
        process_info = getting_webpage_content(params["URL"])
        display(f'[*] Finished {process_name} - within {process_info["process_duration"]:.9f} s', file=global_variables_config["output_file"])

    elif process_name == 'Searching Hyperlinks':
        process_info = getting_hyperlinks(params["web_page_content"])
        display(f'[*] Finished {process_name} within {process_info["process_duration"]:.9f} s', file=global_variables_config["output_file"])
        print_hyperlinks_info(process_info["results"])

    elif process_name == 'Searching Image Lists':
        process_info = getting_image_lists(params["web_page_content"])
        display(f'[*] Finished {process_name} within {process_info["process_duration"]:.9f} s', file=global_variables_config["output_file"])
        print_image_file_info(process_info["results"])

    elif process_name == 'Searching Document Lists':
        process_info = getting_document_lists(params["web_page_content"])
        display(f'[*] Finished {process_name} within {process_info["process_duration"]:.9f} s', file=global_variables_config["output_file"])
        print_document_info(process_info["results"])

    elif process_name == 'Searching Email Address':
        process_info = getting_email_address(params["web_page_content"])
        display(f'[*] Finished {process_name} within {process_info["process_duration"]:.9f} s', file=global_variables_config["output_file"])
        print_email_info(process_info["results"])

    elif process_name == 'Searching Phone Number':
        process_info = getting_phone_number(params["web_page_content"])
        display(f'[*] Finished {process_name} within {process_info["process_duration"]:.9f} s', file=global_variables_config["output_file"])
        print_phoneno_info(process_info["results"])

    elif process_name == 'Searching md5 Hash Lists':
        process_info = getting_md5_hash_lists(params["web_page_content"])
        display(f'[*] Finished {process_name} within {process_info["process_duration"]:.9f} s', file=global_variables_config["output_file"])
        print_md5hash_info(process_info["results"])

    elif process_name == 'Cracking md5 Hash':
        process_info = getting_cracked_md5_hash_results(params["md5hash_lists"], params["password_file"])
        display(f'[*] Finished {process_name} within {process_info["process_duration"]:.9f} s', file=global_variables_config["output_file"])
        print_md5_crack_info(process_info["results"])

    elif process_name == 'Downloading Images':
        process_info = downloading_files(params["image_lists"])
        display(f'[*] Finished {process_name} within {process_info["process_duration"]:.9f} s', file=global_variables_config["output_file"])

    elif process_name == 'Downloading Documents':
        process_info = downloading_files(params["doc_lists"])
        display(f'[*] Finished {process_name} within {process_info["process_duration"]:.9f} s', file=global_variables_config["output_file"])

    elif process_name == 'Checking File Extension In a Directory':
        process_info = checking_file_extension_indir(params["directory"])
        display(f'[*] Finished {process_name} within {process_info["process_duration"]:.9f} s', file=global_variables_config["output_file"])

    elif process_name == 'Checking Badfiles In a Directory':
        process_info = checking_badfile_indir(params["directory"], params["bad_file"])
        display(f'[*] Finished {process_name} within {process_info["process_duration"]:.9f} s', file=global_variables_config["output_file"])

    elif process_name == 'Checking File Content Similarity':
        process_info = checking_file_content_similarity(params["directory"])
        display(f'[*] Finished {process_name} within {process_info["process_duration"]:.9f} s', file=global_variables_config["output_file"])


def main():
    """
        Handling about showing information of each process
    """


if __name__ == '__main__':
    main()