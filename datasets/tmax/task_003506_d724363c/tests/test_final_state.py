# test_final_state.py

import os
import glob

def test_test_result_log_content():
    log_path = "/home/user/test_result.log"
    assert os.path.isfile(log_path), f"Expected result log file {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = "Z" * 100
    assert content == expected_content, f"Content of {log_path} is incorrect. Expected 100 'Z's, got {len(content)} characters."

def test_processor_c_fixed():
    c_path = "/home/user/app/processor.c"
    assert os.path.isfile(c_path), f"{c_path} is missing."

    with open(c_path, "r") as f:
        content = f.read()

    assert "char buffer[50];" not in content, "Vulnerable fixed-size buffer `char buffer[50];` is still present in processor.c."
    assert "strcpy(buffer, input_str);" not in content, "Unsafe `strcpy(buffer, input_str);` is still present in processor.c."

    has_dynamic_alloc = "malloc" in content or "strdup" in content or "calloc" in content or "PyMem_Malloc" in content
    assert has_dynamic_alloc, "processor.c does not seem to use dynamic memory allocation (e.g., malloc, strdup)."

    has_free = "free" in content or "PyMem_Free" in content
    assert has_free, "processor.c does not seem to free the dynamically allocated memory."

def test_extension_compiled():
    # Check if the extension was compiled in-place
    so_files = glob.glob("/home/user/app/processor.*.so")
    assert len(so_files) > 0, "The C extension was not compiled in-place in /home/user/app. Missing processor.*.so file."

def test_test_client_script_exists():
    client_path = "/home/user/app/test_client.py"
    assert os.path.isfile(client_path), f"The test client script {client_path} is missing."