# test_final_state.py
import os

def test_culprit_file():
    culprit_path = '/home/user/culprit.txt'
    assert os.path.isfile(culprit_path), f"File {culprit_path} does not exist."

    with open(culprit_path, 'r') as f:
        content = f.read().strip()

    assert content == "researcher_89", f"Expected culprit to be 'researcher_89', but got '{content}'"

def test_clean_data_extracted():
    clean_data_dir = '/home/user/clean_data'
    assert os.path.isdir(clean_data_dir), f"Directory {clean_data_dir} does not exist."

    expected_files = {
        'dataset_info.txt',
        'images/img1.png',
        'images/img2.png'
    }

    actual_files = set()
    for root, dirs, files in os.walk(clean_data_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, clean_data_dir)
            actual_files.add(rel_path)

    assert actual_files == expected_files, f"Expected safe files {expected_files} in {clean_data_dir}, but found {actual_files}"

def test_zip_slip_detected():
    detected_path = '/home/user/zip_slip_detected.txt'
    assert os.path.isfile(detected_path), f"File {detected_path} does not exist."

    expected_malicious_paths = {
        '../../../home/user/.ssh/authorized_keys',
        'images/../../etc/shadow',
        '/absolute/path/malware.sh'
    }

    with open(detected_path, 'r') as f:
        lines = f.read().splitlines()

    actual_paths = {line.strip() for line in lines if line.strip()}

    assert actual_paths == expected_malicious_paths, f"Expected malicious paths {expected_malicious_paths}, but got {actual_paths}"