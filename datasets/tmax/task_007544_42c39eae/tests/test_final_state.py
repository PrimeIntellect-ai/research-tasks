# test_final_state.py
import os
import pytest

def test_extractor_script_exists():
    assert os.path.isfile('/home/user/extractor.go'), "/home/user/extractor.go is missing"

def test_extracted_safe_files():
    expected_files = [
        '/home/user/clean_data/vision_data/images/img1.png',
        '/home/user/clean_data/vision_data/labels.csv',
        '/home/user/clean_data/nlp_corpus/train.txt',
        '/home/user/clean_data/nlp_corpus/test.txt',
        '/home/user/clean_data/audio_set/audio1.wav',
        '/home/user/clean_data/sensor_logs/log1.txt'
    ]
    for file_path in expected_files:
        assert os.path.isfile(file_path), f"Expected extracted file is missing: {file_path}"

def test_malicious_files_not_extracted():
    # Check that malicious files were not extracted to the system
    # We'll just check if they exist in the paths they tried to traverse to, or inside clean_data
    assert not os.path.exists('/home/user/clean_data/audio_set/../../../home/user/.bashrc'), "Malicious file was extracted!"
    assert not os.path.exists('/home/user/clean_data/sensor_logs/etc/shadow'), "Malicious file was extracted!"
    assert not os.path.exists('/home/user/clean_data/sensor_logs/dir/../../../etc/hosts'), "Malicious file was extracted!"

def test_malicious_log():
    log_path = '/home/user/malicious.log'
    assert os.path.isfile(log_path), f"{log_path} is missing"

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "[audio_set.zip] ../../../home/user/.bashrc",
        "[sensor_logs.zip] /etc/shadow",
        "[sensor_logs.zip] dir/../../../etc/hosts"
    ]

    # Sort expected lines just in case
    expected_lines.sort()

    assert lines == expected_lines, f"Contents of {log_path} do not match the expected sorted output"