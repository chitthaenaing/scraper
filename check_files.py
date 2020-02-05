# Script: check_files.py
# Desc: Checking files in the given directory
# Author: Chit Thae Naing
# Modified: Nov 29 2019 (PEP08)
import os
import binascii
import hashlib
from global_var_config import global_variables_config
from display_output import display


def check_file_extension_indir(directory):
    """
        Checking File Extension in a specific directory
    """
    for file_name in os.listdir(directory):
        check_file_extension(os.path.abspath(directory + os.sep + file_name))


def check_file_extension(file):
    """
        Checking file extension with its file type
    """
    file_hex_signatures = {
        b'474946': ('gif', 'GIF'),
        b'ffd8ff': ('jpg', 'JPG', 'jpeg', 'JPEG'),
        b'89504e': ('png', 'PNG'),
        b'424d': ('bmp', 'BMP'),
        b'504b03': ('docx', 'DOCX'),
        b'255044': ('pdf', 'PDF')
    }

    try:
        with open(file, 'rb') as f:
            file_content = f.read(3)
            file_hex_value = binascii.hexlify(file_content)
            file_type = file_hex_signatures.get(file_hex_value)
            display(f'[x] Checking File Signature of {file} - {file_hex_value}', file=global_variables_config["output_file"])
            if file_type != 'None':
                display(f'\t[x] File type identified as {file_type[0]}', file=global_variables_config["output_file"])
                display(f'\t[x] Extension: {os.path.splitext(file)[1][1:]}', file=global_variables_config["output_file"])
                if os.path.splitext(file)[1][1:] in file_type:
                    display(f'\t[+] OK - valid extension for this file type', file=global_variables_config["output_file"])
                else:
                    display(f'\t[-] Expected: .{file_type[0]}. Investigation recommended.', file=global_variables_config["output_file"])
            else:
                display(f'[-]\tFile type not identified - file signature not found in db!', file=global_variables_config["output_file"])
    except IOError as err:
        display(f'[-] File Error {err}', file=global_variables_config["output_file"])


def check_badfile_indir(directory, bad_file_txt):
    """
        Checking badfile in a specific directory
    """
    for file_name in os.listdir(directory):
        check_badfile(os.path.abspath(directory) + os.sep + file_name, bad_file_txt)


def check_badfile(file, bad_file):
    """
        Checking file with badfiles.txt
    """
    try:
        with open(file, 'rb') as f:
            file_name = os.path.basename(file)
            md5_hash = hashlib.md5(f.read()).hexdigest()
            try:
                with open(bad_file, 'r') as bf:
                    badfiles = {}
                    for line in bf.readlines():
                        badfiles[line.split(':')[0][1:-1]] = line.split(':')[1].strip()[1:-1]
                    if badfiles.get(md5_hash) is not None:
                        display(f'\t[x] {file_name}({md5_hash}) known bad files as {badfiles.get(md5_hash)}', file=global_variables_config["output_file"])
            except IOError as err:
                display(f'[-] File Error {err} - {bad_file} cannot be opened', file=global_variables_config["output_file"])
    except IOError as err:
        display(f'[-] File Error {err} - {file} cannot be opened', file=global_variables_config["output_file"])


def check_file_content_similarity_indir(directory):
    """
        Checking File Content Similarity in a specific directory
    """
    file_hash = {}
    for file_name in os.listdir(directory):
        file = os.path.abspath(directory) + os.sep + file_name
        try:
            with open(file, 'rb') as f:
                md5_hash = hashlib.md5(f.read()).hexdigest()
                file_hash[file_name] = md5_hash

        except IOError as err:
            display(f'[-] File Error {err} - {file} cannot be opened', file=global_variables_config["output_file"])

    same_content_files = {}
    for key, value in file_hash.items():
        same_content_files.setdefault(value, []).append(key)

    same_files = {key: same_content_files[key] for key in same_content_files if len(same_content_files[key]) > 1}

    for same_file_key in same_files:
        same_file_values = ", ".join(same_files[same_file_key]).replace(', ', ' and ', -1)
        display(f'\t[*] {same_file_values} have same {same_file_key}', file=global_variables_config["output_file"])


