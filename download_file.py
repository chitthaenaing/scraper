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
from global_var_config import *
from display_output import display

web_url = global_variables_config['URL']
download_directory = global_variables_config['download_dir']

if os.path.isdir(download_directory):
    # If download folder exits
    # Clearing old contents
    shutil.rmtree(download_directory)
os.mkdir(download_directory)


def download_files(file_lists):
    """
        Download Files
    """

    for file_link, file_name in file_lists:
        if not file_link.startswith("http"):
            file_link = web_url + file_link

        if file_name in [os.path.basename(file) for file in os.scandir(download_directory)]:
            file_name_ext = os.path.splitext(file_name)
            file_name = file_name_ext[0] + '_' + str(id(file_name)) + file_name_ext[1]

        download(file_link, file_name)


def download(url, file_name):
    """
        Download
    """

    try:
        full_download_path = os.path.abspath(download_directory) + os.sep + file_name
        urllib.request.urlretrieve(url, full_download_path)
        display(f'\t[*] Finished downloading {file_name}', file=global_variables_config["output_file"])
    except urllib.error.HTTPError as httperr:
        display(f'\t[-] {file_name} - HTTP Error {httperr.code}: {httperr.msg}', file=global_variables_config["output_file"])
    except Exception:
        display(f'\t[-] Download Error - {file_name}', file=global_variables_config["output_file"])
