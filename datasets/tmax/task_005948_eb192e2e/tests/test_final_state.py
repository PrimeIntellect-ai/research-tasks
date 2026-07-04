# test_final_state.py

import os

def test_incoming_directory_empty():
    incoming_dir = "/home/user/incoming_configs"
    assert os.path.isdir(incoming_dir), f"Directory {incoming_dir} is missing."
    files = os.listdir(incoming_dir)
    assert len(files) == 0, f"Directory {incoming_dir} is not empty. Found: {files}"

def test_processed_configs_files():
    processed_dir = "/home/user/processed_configs"
    assert os.path.isdir(processed_dir), f"Directory {processed_dir} is missing."

    expected_files = {
        "nginx_v1.21.0.json",
        "postgres_v14.2.xml",
        "redis_v6.2.6.csv"
    }

    actual_files = set(os.listdir(processed_dir))
    assert actual_files == expected_files, f"Expected files {expected_files} in {processed_dir}, but found {actual_files}."

def test_sync_log_content():
    log_file = "/home/user/sync_log.txt"
    assert os.path.isfile(log_file), f"Log file {log_file} is missing."

    expected_lines = [
        "[WATCHER] cache.csv moved to redis_v6.2.6.csv\n",
        "[WATCHER] db.xml moved to postgres_v14.2.xml\n",
        "[WATCHER] web.json moved to nginx_v1.21.0.json\n"
    ]

    with open(log_file, "r") as f:
        actual_lines = f.readlines()

    assert actual_lines == expected_lines, "The contents of sync_log.txt do not match the expected sorted format."