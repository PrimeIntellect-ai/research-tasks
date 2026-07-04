# test_final_state.py

import os
import tarfile
import re
import stat

def test_backup_tarball_exists_and_valid():
    """Verify that the backup tarball exists and contains diag.cpp."""
    tarball_path = "/home/user/archive/network_diag.tar.gz"
    assert os.path.isfile(tarball_path), f"Backup tarball not found at {tarball_path}"

    try:
        with tarfile.open(tarball_path, "r:gz") as tar:
            names = tar.getnames()
            # Check if diag.cpp is in the tarball (it might be prefixed with path)
            has_diag = any(name.endswith("diag.cpp") for name in names)
            assert has_diag, f"diag.cpp not found in the backup tarball {tarball_path}"
    except tarfile.TarError as e:
        pytest.fail(f"Failed to open tarball {tarball_path}: {e}")

def test_pipeline_script_executable():
    """Verify that the run_pipeline.sh script exists and is executable."""
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Pipeline script not found at {script_path}"

    st = os.stat(script_path)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"Pipeline script at {script_path} is not executable"

def test_pipeline_log_exists_and_correct():
    """Verify that the pipeline log exists and contains the correct formatted output."""
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"Pipeline log not found at {log_path}"

    with open(log_path, "r") as f:
        content = f.read().strip()

    pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] STATUS: ALL_CLEAR$"
    assert re.match(pattern, content), f"Pipeline log content '{content}' does not match the expected format."

def test_build_directory_and_executable():
    """Verify that the build directory and compiled executable exist."""
    build_dir = "/home/user/build"
    executable_path = "/home/user/build/diag_tool"

    assert os.path.isdir(build_dir), f"Build directory not found at {build_dir}"
    assert os.path.isfile(executable_path), f"Compiled executable not found at {executable_path}"

    st = os.stat(executable_path)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"Compiled tool at {executable_path} is not executable"