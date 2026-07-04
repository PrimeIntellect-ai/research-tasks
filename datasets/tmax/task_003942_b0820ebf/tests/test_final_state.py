# test_final_state.py
import os
import re

def test_process_script_exists():
    script_path = '/home/user/process.sh'
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_malicious_paths_log():
    log_path = '/home/user/malicious_paths.log'
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_paths = ['../bad1.txt', '/etc/malicious.txt']
    assert sorted(lines) == sorted(expected_paths), f"Expected {expected_paths} in {log_path}, got {lines}."

def test_restored_files():
    restored_dir = '/home/user/restored'
    assert os.path.isdir(restored_dir), f"The output directory {restored_dir} does not exist."

    expected_files = {
        'file1.txt': "Updated data for file 1\n",
        'dir1/file2.txt': "Initial data for file 2\n",
        'dir2/file3.txt': "New file 3\n"
    }

    for rel_path, expected_content in expected_files.items():
        full_path = os.path.join(restored_dir, rel_path)
        assert os.path.isfile(full_path), f"Expected restored file {full_path} does not exist."
        with open(full_path, 'r') as f:
            content = f.read()
        assert content == expected_content, f"Content of {full_path} is incorrect. Expected {repr(expected_content)}, got {repr(content)}."

    # Check that malicious files were NOT extracted
    assert not os.path.exists(os.path.join(restored_dir, '../bad1.txt')), "Malicious file ../bad1.txt was extracted!"
    assert not os.path.exists(os.path.join(restored_dir, 'bad1.txt')), "Malicious file bad1.txt was extracted!"
    assert not os.path.exists('/etc/malicious.txt'), "Malicious file /etc/malicious.txt was extracted!"

def test_growth_log():
    log_path = '/home/user/growth.log'
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {log_path}, got {len(lines)}."

    expected_archives = ['inc_01.tar.gz', 'inc_02.tar.gz', 'inc_03.tar.gz']
    for i, line in enumerate(lines):
        match = re.match(r'^([^:]+):\s*(\d+)$', line)
        assert match, f"Line {i+1} in {log_path} is not in the correct format '<archive_filename>: <size_in_bytes>'. Got: {line}"
        archive, size = match.groups()
        assert archive == expected_archives[i], f"Expected archive {expected_archives[i]} on line {i+1}, got {archive}."