# test_final_state.py

import os
import stat
import pytest

def test_c_program_exists():
    """Test that the C program source and compiled executable exist."""
    assert os.path.exists("/home/user/transform.c"), "The source file /home/user/transform.c does not exist."
    assert os.path.exists("/home/user/transform"), "The compiled executable /home/user/transform does not exist."

    st = os.stat("/home/user/transform")
    assert bool(st.st_mode & stat.S_IXUSR), "The file /home/user/transform is not executable."

def test_bash_script_exists():
    """Test that the bash script exists and is executable."""
    assert os.path.exists("/home/user/pipeline.sh"), "The bash script /home/user/pipeline.sh does not exist."
    st = os.stat("/home/user/pipeline.sh")
    assert bool(st.st_mode & stat.S_IXUSR), "The bash script /home/user/pipeline.sh is not executable."

def test_output_csv_content():
    """Test that the output.csv file has the correct final content."""
    assert os.path.exists("/home/user/output.csv"), "The output file /home/user/output.csv does not exist."

    expected_content = """id,name,email,ssn,country
1,John Doe,john@example.com,XXX-XX-6789,US
3,Bob Smith,bob@example.com,XXX-XX-8901,UK
7,Odd Guy,odd@example.com,XXX-XX-2345,US
9,Charlie,charlie@test.com,XXX-XX-3333,FR
"""
    with open("/home/user/output.csv", "r") as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), "The content of /home/user/output.csv does not match the expected final data. Check your C program logic and pipeline deduplication/sorting."