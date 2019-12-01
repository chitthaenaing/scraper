# Script: web_page_forensic.py
# Desc: Perform Forensic analysis on web content
# Author: Chit Thae Naing
# Modified: Nov 29 2019 (PEP08)

# Use this module for searching hyperlinks
import re
# Use this module for parsing image's path
import os
# Use this module for md5 hashing
import hashlib
# Use this module for converting hex value
import binascii

def get_hyperlinks(content):
    """ Search hyperlinks in the context and return them """

    # finding absolute links
    # Starts with https or http://
    # Starts with / (eg. /theme/folder/a.png ) or // (eg. //ajax.googleapis.com/)
    # Covers the special case like "/media/images/logos/ednapuni_red.png?h=60&amp;la=en&amp;w=215&amp;hash=39DC25ADF6177FF9A1AEB6F9D09B30F47FE593E2"
    # absolute_pattern = r'https?://[\w\-\./]+|(?<=[\'\"])/[.\S]*(?=[\'\"])'
    absolute_pattern = r'(?<=[\'\"])https?://[.\S]*(?=[\'\"])|(?<=[\'\"])/[.\S]*(?=[\'\"])'
    absolute_links = re.findall(absolute_pattern, content.decode())
    absolute_links.sort()

    # finding relative links
    # Starts with characters - a.jpg or folder_one/a.jpg
    # Starts with dots - ./folder/a.jpg or ../folder/a.jpg
    # Covers the special case like "ednapuni_red.png?h=60&amp;la=en&amp;w=215&amp;hash=39DC25ADF6177FF9A1AEB6F9D09B30F47FE593E2"

    relative_pattern = r'(?<=[\'\"])([\w\-\(\)]+\.[\w\-\%\&\=\;\?]+|[\w\-\.]+/+.*?)(?=[\'\"])'
    relative_links = re.findall(relative_pattern, content.decode())
    relative_links.sort()

    return (
        absolute_links,
        relative_links,
        len(absolute_links) + len(relative_links)
    )


def get_image_lists(content):
    """
        Search Image files on web content and return them
    """
    absolute_links, relative_links, _ = get_hyperlinks(content)
    image_extension_lists = [
        '.jpg',
        '.JPG',
        '.jpeg',
        '.JPEG', 
        '.png', 
        '.PNG', 
        '.gif', 
        '.GIF', 
        '.bmp', 
        '.BMP'
    ]
    return [
            (link, os.path.basename(link)) for link in absolute_links
            for img_ext in image_extension_lists
            if link.find(img_ext) > -1
        ] + [
            (link, os.path.basename(link)) for link in relative_links
            for img_ext in image_extension_lists
            if link.find(img_ext) > -1
        ]


def get_document_lists(content):
    """
        Search document files on web content and return them
    """
    absolute_links, relative_links, _ = get_hyperlinks(content)
    doc_ext_list = [
        'docx',
        'pdf'
    ]
    return [
            (link, os.path.basename(link)) for link in absolute_links
            for doc_ext in doc_ext_list
            if link.find(doc_ext) > -1
        ] + [
            (link, os.path.basename(link)) for link in relative_links
            for doc_ext in doc_ext_list
            if link.find(doc_ext) > -1
        ]


def get_email_lists(content):
    """ Searching Email Address and return them """
    freetext_email_pattern = r'(?<!mailto:)[\w\.\-]+@[\w\.\-]+\.\w+'
    freetext_email_lists = re.findall(freetext_email_pattern, content.decode())

    mailto_email_pattern = r'(?<=mailto:)[\w\.\-]+@[\w\.\-]+\.\w+'
    mailto_email_lists = re.findall(mailto_email_pattern, content.decode())

    return (
        freetext_email_lists,
        mailto_email_lists,
        len(freetext_email_lists) + len(mailto_email_lists)
    )


def get_phoneno_lists(content):
    """ Searching Phone Number and return them """
    phoneno_pattern = r'\+\d{1,3}[\s\-]?\(?\d\)?[\d\-\s]+(?=\d)'
    phoneno_lists = re.findall(phoneno_pattern, content.decode())
    return phoneno_lists


def get_md5hash_lists(content):
    """ Searching md5 hash and return them """
    md5_pattern = r'[\da-f]{32}'
    md5hash_lists = re.findall(md5_pattern, content.decode())
    return md5hash_lists


def dict_attack(hash_lists):
    """Checks password hash, against a dictionary of common passwords"""

    # set up list of common passwords
    common = ['123', '1234', '12345', '123456', '1234567', '12345678',
              'password', 'qwerty', 'abc', 'abcd', 'abc123', '111111',
              'monkey', 'arsenal', 'letmein', 'trustno1', 'dragon',
              'baseball', 'superman', 'iloveyou', 'starwars',
              'montypython', 'cheese', '123123', 'football', 'batman']
    
    found_pwd_lists = []
    for md5_hash in hash_lists:
        found_pwd = ''
        for pwd in common:
            if hashlib.md5(pwd.encode()).hexdigest() == md5_hash:
                found_pwd = pwd
                break
        if found_pwd == '':
            found_pwd = 'no matching password found'
        
        found_pwd_lists.append(
            (md5_hash, found_pwd)
        )
    return found_pwd_lists


def check_file_extension(file):
    """ Checking file extension with its file type """
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
            print(f'[x] Checking File Signature of {file} - {file_hex_value}')
            if file_type !=  'None':
                print(f'\t[x] File type identified as {file_type[0]}')
                print(f'\t[x] Extension: {os.path.splitext(file)[1][1:]}')
                if os.path.splitext(file)[1][1:] in file_type:
                    print(f'\t[+] OK - valid extension for this file type')
                else:
                    print(f'\t[-] Expected: .{file_type[0]}. Investiagtion recommended.')
            else:
                print(f'[-]\tFile type not identified - file signature not found in db!')    
    except IOError as err:
        print(f'[-] File Error {err}')


def check_badfile(md5_hash, bad_file):
    """ Checking file with badfiles.txt """
    try:
        with open(bad_file, 'r') as f:
            badfiles = {}
            for line in f.readlines():
                badfiles[line.split(':')[0][1:-1]] = line.split(':')[1].strip()[1:-1]
            # print(f'{md5_hash} - {badfiles.get(md5_hash)}')
            if badfiles.get(md5_hash) != 'None':
                print(f'[x] {md5_hash} known bad files as {badfiles.get(md5_hash)}')
       
    except IOError as err:
        print(f'[-] File Error {err}')
    

def main():
    """ Get lists of hyperlinks found in the content """
    content = b'<!Doctype html><html><head><title>Chit Thae Naing</title></head><body><h1>Welcome to my site</h1></body></html>'
    print(get_hyperlinks(content))


if __name__ == '__main__':
    main()
