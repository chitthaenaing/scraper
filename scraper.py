# Script: Scraper.py
# Desc: Scraping, information gathering and forensic analysis on web page
# Author: Chit Thae Naing
# Modified: Nov 29 2019 (PEP08)

import sys
import time
from global_var_config import global_variables_config
from display_format import print_process_format


def loop_sub_process_lists(sub_process_lists):
    """
        Iterate through sub process lists
    """
    if sub_process_lists is not None and len(sub_process_lists) > 0:
        for sub_process in sub_process_lists:
            params_key = list(sub_process['params'].keys())[0]
            if global_variables_config.get(params_key) is not None:
                sub_process['params'][params_key] = global_variables_config.get(params_key)
                print_process_format(sub_process['heading'], sub_process['process_name'], sub_process['params'])

                if sub_process.get('sub_process_lists') is not None:
                    loop_sub_process_lists(sub_process.get('sub_process_lists'))


def main():
    """
        Display Informations and forensic analysis of the given url
    """
    process_lists = [
        {
            'heading': 'Getting Webpage Content via URL',
            'process_name': 'Retrieving URL',
            'params': {
                'URL': global_variables_config["URL"]
            },
            'sub_process_lists': [
                {
                    'heading': 'Getting Hyperlinks',
                    'process_name': 'Searching Hyperlinks',
                    'params': {
                        'web_page_content': global_variables_config["web_page_content"]
                    }
                },
                {
                    'heading': 'Getting Image Lists',
                    'process_name': 'Searching Image Lists',
                    'params': {
                        'web_page_content': global_variables_config["web_page_content"]
                    },
                    'sub_process_lists': [
                        {
                            'heading': 'Downloading Images',
                            'process_name': 'Downloading Images',
                            'params': {
                                'image_lists': global_variables_config["image_lists"]
                            }
                        }
                    ]
                },
                {
                    'heading': 'Getting Document Lists',
                    'process_name': 'Searching Document Lists',
                    'params': {
                        'web_page_content': global_variables_config["web_page_content"]
                    },
                    'sub_process_lists': [
                        {
                            'heading': 'Downloading Documents',
                            'process_name': 'Downloading Documents',
                            'params': {
                                'doc_lists': global_variables_config["doc_lists"]
                            }
                        }
                    ]
                },
                {
                    'heading': 'Getting Email Address',
                    'process_name': 'Searching Email Address',
                    'params': {
                        'web_page_content': global_variables_config["web_page_content"]
                    }
                },
                {
                    'heading': 'Getting Phone Number',
                    'process_name': 'Searching Phone Number',
                    'params': {
                        'web_page_content': global_variables_config["web_page_content"]
                    }
                },
                {
                    'heading': 'Getting md5 Hash Lists',
                    'process_name': 'Searching md5 Hash Lists',
                    'params': {
                        'web_page_content': global_variables_config["web_page_content"]
                    }
                },
                {
                    'heading': 'Cracking md5 Hash',
                    'process_name': 'Cracking md5 Hash',
                    'params': {
                        'md5hash_lists': global_variables_config["md5hash_lists"],
                        'password_file': global_variables_config["password_file"]
                    }
                }
            ]
        },
        {
            'heading': 'Checking Extension of Each File in Download Folder with its file signature',
            'process_name': 'Checking File Extension In a Directory',
            'params': {
                'directory': global_variables_config['download_dir']
            }
        },
        {
            'heading': 'Checking hex value of Each File in Download Folder with badfiles.txt',
            'process_name': 'Checking Badfiles In a Directory',
            'params': {
                'directory': global_variables_config['download_dir'],
                'bad_file': global_variables_config["bad_file"]
            }
        },
        {
            'heading': 'Checking the content similarity of the same filenames',
            'process_name': 'Checking File Content Similarity',
            'params': {
                'directory': global_variables_config['download_dir']
            }
        }
    ]

    for process in process_lists:
        print_process_format(process['heading'], process['process_name'], process['params'])
        if process.get('sub_process_lists') is not None:
            loop_sub_process_lists(process.get('sub_process_lists'))


if __name__ == '__main__':
    with open('output.txt', 'w') as output_file:
        global_variables_config['output_file'] = output_file
        main()
