# test_final_state.py
import os

def test_restored_directory_exists():
    assert os.path.isdir("/home/user/projects/restored/"), "/home/user/projects/restored/ directory does not exist."

def test_valid_files_extracted():
    config_path = "/home/user/projects/restored/config.json"
    main_path = "/home/user/projects/restored/main.py"

    assert os.path.isfile(config_path), f"Expected file {config_path} was not extracted."
    assert os.path.isfile(main_path), f"Expected file {main_path} was not extracted."

    with open(config_path, "r") as f:
        assert f.read() == '{"host": "localhost", "port": 8080}', "Content of config.json is incorrect."

    with open(main_path, "r") as f:
        assert f.read() == 'print("Hello World!")', "Content of main.py is incorrect."

def test_corrupted_files_not_extracted():
    app_data_path = "/home/user/projects/restored/app_data.csv"
    readme_path = "/home/user/projects/restored/readme.txt"

    assert not os.path.exists(app_data_path), f"Corrupted file {app_data_path} should not have been extracted."
    assert not os.path.exists(readme_path), f"Corrupted file {readme_path} should not have been extracted."

def test_corrupted_log():
    log_path = "/home/user/projects/restored/corrupted.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert "app_data.csv" in lines, "app_data.csv is missing from corrupted.log"
    assert "readme.txt" in lines, "readme.txt is missing from corrupted.log"
    assert len(lines) == 2, f"corrupted.log should contain exactly 2 entries, found {len(lines)}"