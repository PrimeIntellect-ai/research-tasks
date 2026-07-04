# test_final_state.py

import os
import stat
import subprocess

def test_tool_fixed():
    path = "/app/txt2csv-tools-1.2/convert.sh"
    assert os.path.exists(path), f"Tool script {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert 'AWK_BIN="awk"' in content, f"The tool script {path} was not correctly fixed. Expected 'AWK_BIN=\"awk\"'."

def test_script_exists_and_executable():
    path = "/home/user/organize.sh"
    assert os.path.isfile(path), f"Script {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {path} is not executable."

def test_execution_time_and_output():
    script_path = "/home/user/organize.sh"

    # Clear previous output directories to ensure a clean run
    subprocess.run("rm -rf /home/user/processed/* /home/user/by_date/*", shell=True)

    # Run the script and measure time
    cmd = f'/usr/bin/time -f "%e" {script_path} > /tmp/time_out 2> /tmp/time_err'
    process = subprocess.run(cmd, shell=True, executable='/bin/bash')
    assert process.returncode == 0, "The organize.sh script failed to execute successfully."

    with open("/tmp/time_err", "r") as f:
        lines = f.read().strip().split('\n')
        time_str = lines[-1]

    try:
        exec_time = float(time_str)
    except ValueError:
        assert False, f"Could not parse execution time from time output: {time_str}"

    assert exec_time <= 10.0, f"Execution time {exec_time} exceeds the threshold of 10.0 seconds."

def test_processed_files():
    processed_dir = "/home/user/processed"
    assert os.path.isdir(processed_dir), f"Directory {processed_dir} does not exist."

    files = [f for f in os.listdir(processed_dir) if f.endswith('.csv')]
    assert len(files) == 5000, f"Expected 5000 .csv files in {processed_dir}, found {len(files)}."

def test_symlinks_by_date():
    processed_dir = "/home/user/processed"
    by_date_dir = "/home/user/by_date"

    processed_files = [f for f in os.listdir(processed_dir) if f.endswith('.csv')]
    assert len(processed_files) > 0, "No processed files found to check symlinks."

    for filename in processed_files:
        csv_path = os.path.join(processed_dir, filename)
        with open(csv_path, "r") as f:
            first_line = f.readline().strip()

        date_str = first_line

        symlink_path = os.path.join(by_date_dir, date_str, filename)
        assert os.path.islink(symlink_path), f"Expected symlink at {symlink_path} does not exist."

        target = os.readlink(symlink_path)
        resolved_target = os.path.normpath(os.path.join(os.path.dirname(symlink_path), target))
        assert resolved_target == csv_path, f"Symlink {symlink_path} points to {resolved_target}, expected {csv_path}."

def test_atomic_writes_heuristic():
    script_path = "/home/user/organize.sh"
    with open(script_path, "r") as f:
        content = f.read()
    assert "mv " in content or "install " in content, "Script does not appear to use atomic writes (e.g., missing 'mv' command to move temporary files)."