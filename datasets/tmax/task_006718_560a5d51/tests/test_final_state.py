# test_final_state.py
import os

def test_extractor_files_exist():
    assert os.path.exists("/home/user/extractor.c"), "Source file /home/user/extractor.c does not exist."
    assert os.path.exists("/home/user/extractor"), "Compiled binary /home/user/extractor does not exist."
    assert os.access("/home/user/extractor", os.X_OK), "/home/user/extractor is not executable."

def test_extracted_files():
    readme_path = "/home/user/safe_output/README.md"
    main_c_path = "/home/user/safe_output/src/main.c"

    assert os.path.exists(readme_path), f"{readme_path} was not extracted."
    with open(readme_path, "r") as f:
        assert f.read() == "Project info here.", f"Incorrect contents in {readme_path}."

    assert os.path.exists(main_c_path), f"{main_c_path} was not extracted."
    with open(main_c_path, "r") as f:
        assert f.read() == "int main() { return 0; }", f"Incorrect contents in {main_c_path}."

def test_zip_slip_prevented():
    hacked_path = "/home/user/hacked.txt"
    assert not os.path.exists(hacked_path), f"Zip slip vulnerability exploited! {hacked_path} was created."

def test_extraction_log():
    log_path = "/home/user/safe_output/extraction.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    expected_log = (
        "EXTRACTED: README.md\n"
        "EXTRACTED: src/main.c\n"
        "REJECTED: ../../../home/user/hacked.txt\n"
        "REJECTED: /etc/shadow\n"
        "REJECTED: docs/../secret.txt\n"
    )

    with open(log_path, "r") as f:
        actual_log = f.read()

    assert actual_log.strip() == expected_log.strip(), f"Log file contents do not match expected output.\nExpected:\n{expected_log}\nGot:\n{actual_log}"