#!/bin/python
"""
    This program is intended to provide a way to test an existing second
  program.  This program will invoke the second program and pass the
  arguments to the second program, run it, then pass the second programs
  output through as if it were this program's output. So this is a wrapper!
  This makes it possible to emulate the second program and INJECT FAKE BUGS.
  A yaml file has a list of inputs, and associated fake bug outputs that
  allow us to pretend that the second program has specific (fake) bugs. 
  This can be helpful in assessing tester's skills, test suite quality,
  and test frameworks and bug tracking/reporting. (Test the tester!)
"""
import base64
import os
from pathlib import Path
import subprocess
import sys
from typing import Optional
import yaml as yam

def main() -> int:
    """
       A simple main() which reads args and faildata then looks
       for looks for a matching args/fail-case and fakes outputs
       for any match, or runs "for real" where no match found.
    """
    passargs = process_args(sys.argv)
    faildata_filename = Path(f'{sys.argv[0]}').stem
    faildata = read_cases(f'{faildata_filename}_{passargs[0]}.yaml')
    matched = match_case(faildata, ' '.join(passargs))
    return_code = 0
    if matched is None:   # no mathes in filedata, run normally
        return_code = run_real(passargs)
    else:
        return_code = run_fake(faildata, matched)
    # uncomment this line to force Thonny warnings
    return return_code

def clean_string(a_string: str) -> str:
    """
        Resolve special characters in the input string and return
        the resulting string.
    """
    if isinstance(a_string, str):
        a_string = base64.b64decode(a_string.encode('ascii')).decode('utf-8')
    return a_string

def match_case(fdata: dict, jargs: str) -> int | Optional[int]:
    """
        Given the input dictionary which has a 'cases' entry that
        contains a list of dictionaries, find a list entry where the
        'input' dict entry matches the string passed in and return
        the index of the list of cases as a match
    """
    match_index = next((i for i, c in enumerate(fdata['cases'])
                    if clean_string(c['in']) == jargs), None)
    return match_index

def print_result(out: str, err: str):
    """
        Send the output to stdout and errors to stderr
    """
    if out:
        print(f'{out.strip()}')
    if err:
        print(f'{err.strip()}', file=sys.stderr)

def process_args(pass_args: list[str]) -> list[str]:
    """
        Get command line args passed in by caller/user.
    """
    if len(pass_args) < 2:  # by default, argv[0] is this app's name
        print('ERROR: Missing required arg(s)', file=sys.stderr)
        print(f'\n   Usage: {pass_args[0]} <app2> <app2_arg> <app2_arg> ...')
        print(f'\n   Where "app2" is a second app to be invoked by {pass_args[0]}')
        sys.exit(2)
    if not os.path.isfile(pass_args[0]) and os.access(pass_args[0], os.X_OK):
        print(f'ERROR: {pass_args[0]} is not executable', file=sys.stderr)
        sys.exit(3)
    pcrocessed_args = pass_args[1:]
    # TODO - handle any Failer app specific args, then pass the rest
    # TODO - through to article under test
    return pcrocessed_args

def read_cases(cases_file_name: str) -> dict:
    """
        Read the yaml file with all the cases that we should fake a failure for,
        and the details to be faked e.g. stdout, stderr and return value or exit
        code
    """
    fdata: dict = {}
    try:
        with open(cases_file_name, 'r', encoding="utf-8") as y_file:
            fdata = yam.safe_load(y_file)
    except FileNotFoundError as exception:
        print(f'Exception: {exception}', file=sys.stderr)
    return fdata

def run(app_with_args: list) -> subprocess.CompletedProcess | None:
    """
        A wrapper for subprocess.run() to execute the 'app' or program
        being faked by Failer.  When none of the cases in failer yaml
        are mathced for faking, we run the app 'for real' and pass the
        results to stdout, stderr, return_code just as the app would normally do
    """
    try:
        completed_process = subprocess.run(app_with_args,
                            capture_output=True,
                            text=True,
                            check=True)
        return completed_process
    except FileNotFoundError:
        print('ERROR: Command not found or executable not in PATH:', end=' ')
        print(f'{app_with_args[0]}', file=sys.stderr)
        return None
    except subprocess.CalledProcessError as exception:
        print(f'ERROR: Command failed with exit code {exception.returncode}',
              file=sys.stderr)
        print(f'STDOUT: [{exception.stdout}]', file=sys.stderr)
        print(f'STDERR: [{exception.stderr}]', file=sys.stderr)
        return None

def run_fake(faildata: dict[str, list[dict]], matched: int) -> int:
    """
        We found a matching fake fail case so DON'T run "for real"
        but just pretend to run by printing the fake stdout and fake
        stderr to thier respective devices and return the faked return_code
    """
    fake_stdout = clean_string(faildata['cases'][matched]['out'])
    fake_stderr = clean_string(faildata['cases'][matched]['err'])
    fake_return_code = faildata['cases'][matched]['rc']
    print_result(fake_stdout, fake_stderr)
    return fake_return_code

def run_real(passargs: list) -> int:
    """
        We found no matching fake fail case so Failer should just run
        the "real" script/app/program and pass through the outputs
    """
    result = run(passargs)
    if result:
        print_result(result.stdout, result.stderr)
        return result.returncode
    return 0


if __name__ == '__main__':
    sys.exit(main())
