#!/bin/python
"""
  This program replaces testcase details in a intermediair yaml input file with
  encoded strings just so they are less obvious so they can be found by
  testing and not by cheating when looking into the yaml file.  
"""
import base64
import sys
import yaml as yam

def encode_string(a_string: str) -> str:
    """
        Mix up the characters in a sring by encoding
    """
    if isinstance(a_string, str):
        a_string = base64.b64encode(a_string.encode('utf-8')).decode('utf-8')
    return a_string

def decode_string(a_string: str) -> str:
    """
       Undo the encoding to restore the string to normal
    """
    if isinstance(a_string, str):
        a_string = base64.b64decode(a_string.encode('ascii')).decode('utf-8')
    return a_string

def check_cases(cases: dict) -> dict:
    """
        Iterate the fields in each testcase in dictionary to encode
    """
    for index, a_case in enumerate(cases['cases']):
        for key, value in a_case.items():
            a_case[key] = encode_string(value)
        cases['cases'][index] = a_case
    return cases

def read_cases() -> dict:
    """
        Read the yaml file containing all the testcases with fake results
    """
    fdata = {}
    try:
        # TODO un-hardcode file name
        with open('intermediair_date_plain.yaml', 'r', encoding="utf-8") as y_file:
            fdata = yam.safe_load(y_file)
    except FileNotFoundError as exception:
        print(f'Exception: {exception}')
    return fdata

def write_cases(fdata: dict) -> int:
    """
        Write the yaml of testcases
    """
    inner_return_code: int = 0
    try:
        # TODO un-hardcode file name
        with open('intermediair_date.yaml', 'w', encoding="utf-8") as yfile:
            yam.safe_dump(fdata, yfile)
    except FileNotFoundError as exception:
        print(f'Exception: {exception}')
        inner_return_code = 1
    return inner_return_code

if __name__ == '__main__':
    return_code: int = write_cases(check_cases(read_cases()))
    sys.exit(return_code)
