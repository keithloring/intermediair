""" pytest based unit tests for test_<module.py> """
import subprocess
import pytest
import failer

def main():
    """
        This main() is only here to overcome the "limitation" that Thonny IDE
        "cannot debug pytest".  With this and the "if __name__ == '__main__':"
        at the bottom of this file, you can set a breakpoint and run or debug
        with tests Thonny, stepping into the code being tested as desired.
    """
    print(f'Pytest Version: {pytest.__version__}')
    # call each test function below
    test_clean_string()
    test_match_case()
    test_print_result()
    test_process_args()
    test_run()
    test_run_fake()
    test_run_real()

def test_clean_string():
    """ Make sure we clean odd characters from strings """
    a_string = "VGhpcyBpcyBhIHRlc3Q="
    a_clean_string = failer.clean_string(a_string)
    assert a_clean_string == 'This is a test'

def test_match_case():
    """ exercise the matching of input to cases in the yaml file """
    faildict = {'cases': [{'in': 'aW4x', 'out': 'o1', 'err': 'e1', 'rc': 100},
                          {'in': 'aW4y', 'out': 'o2', 'err': 'e2', 'rc': 220},
                          {'in': 'aW4z', 'out': '03', 'err': 'e3', 'rc': 253}]}
    assert failer.match_case(faildict, 'in1') == 0
    assert failer.match_case(faildict, 'in2') == 1
    assert failer.match_case(faildict, 'in3') == 2
    assert failer.match_case(faildict, 'in4') is None

def test_print_result():
    """
       the first arg gets printed to stdout, the second to stderr
       
       prompt for pytest mock of stdour & stderr:
           https://share.google/aimode/wtmX7fIa3aaxGTRB4
       
       nothing = failer.print_result('content of stdout', 'content of stderr')
       assert nothing is None
    """

def test_process_args():
    """ exercise argment processing """
    arg_list = failer.process_args(['failer.py'])
    assert isinstance(arg_list, list)
    arg_list = failer.process_args(['one', 'two', 'three'])
    assert isinstance(arg_list, list)
    assert len(arg_list) == 3
    assert arg_list

def test_run():
    """ here we could run real or fake depending on inputs """
    try:
        completed_process = failer.run(['date', '-d', '20260323'])
    except subprocess.CalledProcessError as exception:
        assert exception is False
    assert isinstance(completed_process, subprocess.CompletedProcess)
    assert completed_process.args == ['date', '-d', '20260323']
    assert completed_process.stdout == 'Mon Mar 23 12:00:00 AM EDT 2026\n'
    assert completed_process.stderr == ''
    assert completed_process.returncode == 0

def test_run_fake():
    """ check that we fake output as expected when input DOES match a case """
    fakedata: dict = {'cases': [{'err': 'aW4y',
                                 'in': 'ZGF0ZSAtZCAyMDAwMDEwMQ==',
                                 'out': 'VGh1IEphbiAxIDEyOjAwOjAwIEFNIEVTVCAyMDAw',
                                 'rc': 123}]}
    return_code = failer.run_fake(fakedata, 0)
    assert return_code == 123

def test_run_real():
    """ check that we run as expeted when yaml has no cases matching the inputs """


if __name__ == '__main__':
    main()
