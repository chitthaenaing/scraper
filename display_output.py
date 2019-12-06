# Script: display_output.py
# Desc: To output on both console and output file
# Author: Chit Thae Naing
# Modified: Nov 29 2019 (PEP08)


def display(text, file=""):
    """
        Print output to console and
        Write output to a file
    """
    if file:
        print(text, file=file)
    print(text)