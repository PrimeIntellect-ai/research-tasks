# test_final_state.py
import os
import time
import pytest

def test_parser_go_exists_and_atomic():
    """Test that parser.go exists and uses os.Rename for atomic writes."""
    path = "/home/user/parser.go"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "os.Rename" in content, "parser.go does not appear to use os.Rename for atomic writes as requested."

def test_watch_sh_exists_and_inotify():
    """Test that watch.sh exists and uses inotifywait."""
    path = "/home/user/watch.sh"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "inotifywait" in content, "watch.sh does not appear to use inotifywait."

def test_manual_dataset_999():
    """Test that the manually created test file was processed correctly."""
    path = "/home/user/datasets/processed/dataset_999.txt"
    assert os.path.exists(path), f"File {path} does not exist. Did you manually create and process the test file?"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "Test €", f"Content of dataset_999.txt is incorrect. Expected 'Test €', got {repr(content)}."

def test_pipeline_processing():
    """Test the entire pipeline by dropping a valid .dat file and verifying the output."""
    raw_path = "/home/user/datasets/raw/eval_test.dat"
    processed_path = "/home/user/datasets/processed/dataset_42.txt"

    # Binary content: RAWD (52 41 57 44), ID=42 (2A 00 00 00), Length=11 (0B 00), Payload="Hello World"
    test_data = b'\x52\x41\x57\x44\x2A\x00\x00\x00\x0B\x00\x48\x65\x6C\x6C\x6F\x20\x57\x6F\x72\x6C\x64'

    with open(raw_path, "wb") as f:
        f.write(test_data)

    # Wait for the background watch script to process it
    time.sleep(2.5)

    assert os.path.exists(processed_path), f"File {processed_path} was not created. Is watch.sh running in the background and processing new files?"

    with open(processed_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert content == "Hello World", f"Content of dataset_42.txt is incorrect. Expected 'Hello World', got {repr(content)}."