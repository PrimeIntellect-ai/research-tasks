# test_final_state.py

import os
import stat
import pytest

RESTORE_SH_PATH = "/home/user/restore.sh"
GENERATE_PY_PATH = "/home/user/generate_restore.py"

def test_generate_script_exists():
    assert os.path.exists(GENERATE_PY_PATH), f"The script {GENERATE_PY_PATH} was not found."
    assert os.path.isfile(GENERATE_PY_PATH), f"{GENERATE_PY_PATH} is not a file."

def test_restore_sh_exists_and_executable():
    assert os.path.exists(RESTORE_SH_PATH), f"The generated script {RESTORE_SH_PATH} was not found. Did you run your python script?"
    assert os.path.isfile(RESTORE_SH_PATH), f"{RESTORE_SH_PATH} is not a file."

    st = os.stat(RESTORE_SH_PATH)
    is_executable = bool(st.st_mode & stat.S_IXUSR)
    assert is_executable, f"The file {RESTORE_SH_PATH} is not executable. Please use chmod +x."

def test_restore_sh_content():
    expected_content = (
        "#!/bin/bash\n"
        "restore_cmd --db db_prod --id b1 --type full\n"
        "restore_cmd --db db_prod --id b2 --type incremental\n"
        "restore_cmd --db db_prod --id b3 --type incremental\n"
    )

    with open(RESTORE_SH_PATH, "r") as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), (
        f"The content of {RESTORE_SH_PATH} does not match the expected output.\n"
        f"Expected:\n{expected_content.strip()}\n"
        f"Got:\n{content.strip()}"
    )