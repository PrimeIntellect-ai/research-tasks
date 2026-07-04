# test_final_state.py
import os
import json
import stat

def test_generator_go_exists():
    assert os.path.isfile('/home/user/generator.go'), "/home/user/generator.go does not exist."

def test_makefile_exists_and_targets():
    makefile_path = '/home/user/Makefile'
    assert os.path.isfile(makefile_path), "/home/user/Makefile does not exist."
    with open(makefile_path, 'r') as f:
        content = f.read()

    for target in ['build', 'run', 'extract', 'all']:
        assert f"{target}:" in content or f"{target} :" in content, f"Makefile is missing the '{target}' target."

def test_generator_executable_exists():
    exe_path = '/home/user/generator'
    assert os.path.isfile(exe_path), "/home/user/generator does not exist."
    st = os.stat(exe_path)
    assert bool(st.st_mode & stat.S_IXUSR), "/home/user/generator is not executable."

def test_data_json_validity_and_content():
    json_path = '/home/user/data.json'
    assert os.path.isfile(json_path), "/home/user/data.json does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "/home/user/data.json is not valid JSON."

    assert isinstance(data, list), "/home/user/data.json should contain a JSON array."
    assert len(data) >= 40, "/home/user/data.json should contain at least 40 elements."

    item_20 = None
    for item in data:
        if item.get("n") == 20:
            item_20 = item
            break

    assert item_20 is not None, "Element with n=20 not found in /home/user/data.json."
    assert item_20.get("fib") == 6765, f"Expected fib=6765 for n=20, got {item_20.get('fib')}."
    assert item_20.get("lpf") == 41, f"Expected lpf=41 for n=20, got {item_20.get('lpf')}."

def test_answer_txt_content():
    answer_path = '/home/user/answer.txt'
    assert os.path.isfile(answer_path), "/home/user/answer.txt does not exist."

    with open(answer_path, 'r') as f:
        content = f.read().strip()

    assert content == "41", f"Expected /home/user/answer.txt to contain '41', got '{content}'."