# Script: download_file.py
# Desc: Get Web Page Content
# Author: Chit Thae Naing
# Modified: Nov 29 2019 (PEP08)

# Use this module for reading the contents of url
import urllib.request
# Use this module for moving and renaming files
import shutil
# Use this module for parsing path
import os


def preparing_download_folder(download_directory):
    """ Setting up download folder """
    if os.path.isdir(download_directory):
    # If download folder exits
    # Clearing old contents
        shutil.rmtree(download_directory)    
    os.mkdir(download_directory)


def download_file(url, file_name, download_directory):
    """ Download file """
    try:
        urllib.request.urlretrieve(url, os.path.abspath(download_directory) + os.sep + file_name)
        print(f'\t[*] Finished downloading {file_name}')
    except urllib.error.HTTPError as httperr:
        print(f'\t[-] {file_name} - HTTP Error {httperr.code}: {httperr.msg}')
    except Exception:
        print(f'\t[-] Download Error - {file_name}')
    