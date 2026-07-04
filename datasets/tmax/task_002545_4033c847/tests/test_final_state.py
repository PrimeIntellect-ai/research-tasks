# test_final_state.py
import os

def test_recovered_main_py():
    path = '/home/user/recovered_project/src/main.py'
    assert os.path.isfile(path), f"Expected file {path} to exist."
    with open(path, 'r') as f:
        content = f.read().strip()
    expected = "def hello_world():\n    print('Hello')"
    assert content == expected, f"Content of {path} is incorrect.\nExpected:\n{expected}\nGot:\n{content}"

def test_recovered_readme_md():
    path = '/home/user/recovered_project/docs/readme.md'
    assert os.path.isfile(path), f"Expected file {path} to exist."
    with open(path, 'r') as f:
        content = f.read().strip()
    expected = "# Documentation\nThis is the readme."
    assert content == expected, f"Content of {path} is incorrect.\nExpected:\n{expected}\nGot:\n{content}"

def test_recovered_helper_py():
    path = '/home/user/recovered_project/src/utils/helper.py'
    assert os.path.isfile(path), f"Expected file {path} to exist."
    with open(path, 'r') as f:
        content = f.read().strip()
    expected = "def add(a, b):\n    return a + b"
    assert content == expected, f"Content of {path} is incorrect.\nExpected:\n{expected}\nGot:\n{content}"

def test_invalid_file_not_extracted():
    path = '/home/user/recovered_project/evil/hidden.py'
    assert not os.path.exists(path), f"File {path} should not have been extracted because its chunk lacked [VALID_BLOCK]."

def test_chunks_directory_exists():
    path = '/home/user/chunks'
    assert os.path.isdir(path), f"Expected directory {path} to exist."

    # Check if there are files starting with piece_
    files = [f for f in os.listdir(path) if f.startswith('piece_')]
    assert len(files) > 0, f"Expected chunk files starting with 'piece_' in {path}."

def test_extractor_script_exists():
    path = '/home/user/extractor.py'
    assert os.path.isfile(path), f"Expected Python script {path} to exist."