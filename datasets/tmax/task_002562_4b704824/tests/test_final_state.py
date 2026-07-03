# test_final_state.py
import os
import re

def test_result_log():
    log_path = "/home/user/math_build/result.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing. Did you redirect the output of ./math_app?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "148", f"Expected result.log to contain '148', but found '{content}'"

def test_math_app_compiled():
    app_path = "/home/user/math_build/math_app"
    assert os.path.isfile(app_path), f"Executable {app_path} is missing. Did you run make?"
    assert os.access(app_path, os.X_OK), f"File {app_path} is not executable."

def test_generator_c_fixed():
    gen_path = "/home/user/math_build/generator.c"
    assert os.path.isfile(gen_path), f"File {gen_path} is missing."

    with open(gen_path, "r") as f:
        content = f.read()

    # Check that calculate_magic is called with i*2 and i+1
    # We can use a regex to be flexible with spaces
    assert re.search(r"calculate_magic\s*\(\s*i\s*\*\s*2\s*,\s*i\s*\+\s*1\s*\)", content) or \
           re.search(r"calculate_magic\s*\(\s*2\s*\*\s*i\s*,\s*i\s*\+\s*1\s*\)", content), \
           "generator.c does not seem to call calculate_magic with the correct arguments (i * 2, i + 1)."

def test_main_c_unmodified():
    main_path = "/home/user/math_build/main.c"
    assert os.path.isfile(main_path), f"File {main_path} is missing."
    with open(main_path, "r") as f:
        content = f.read()
    assert "sum += magic_table[i];" in content, "main.c appears to have been modified."

def test_makefile_unmodified():
    makefile_path = "/home/user/math_build/Makefile"
    assert os.path.isfile(makefile_path), f"File {makefile_path} is missing."
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "math_app: main.c table.h" in content, "Makefile appears to have been modified."