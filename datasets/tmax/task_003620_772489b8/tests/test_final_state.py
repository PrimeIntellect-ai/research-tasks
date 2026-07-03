# test_final_state.py

import os
import stat
import subprocess
import re

def test_c_program_exists_and_executable():
    c_source = "/home/user/write_timestamp.c"
    c_bin = "/home/user/write_timestamp"

    assert os.path.isfile(c_source), f"C source file {c_source} is missing."
    assert os.path.isfile(c_bin), f"Compiled binary {c_bin} is missing."

    st = os.stat(c_bin)
    assert bool(st.st_mode & stat.S_IXUSR), f"Binary {c_bin} is not executable."

def test_c_program_output():
    c_bin = "/home/user/write_timestamp"
    env = os.environ.copy()
    env["TZ"] = "UTC"
    env["LC_ALL"] = "C"

    result = subprocess.run([c_bin], env=env, capture_output=True, text=True)
    assert result.returncode == 0, f"Running {c_bin} failed with return code {result.returncode}."

    output = result.stdout
    assert output.endswith("\n"), "Output does not have a trailing newline."

    output_stripped = output.strip()
    pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC$"
    assert re.match(pattern, output_stripped), f"Output '{output_stripped}' does not match expected format 'YYYY-MM-DD HH:MM:SS UTC'."

def test_bash_script_exists_and_executable():
    script = "/home/user/logger_script.sh"
    assert os.path.isfile(script), f"Bash script {script} is missing."

    st = os.stat(script)
    assert bool(st.st_mode & stat.S_IXUSR), f"Bash script {script} is not executable."

def test_bash_script_logic():
    script = "/home/user/logger_script.sh"
    log_file = "/home/user/server.log"
    old_log_file = "/home/user/server.log.old"

    # Clean up logs if they exist
    if os.path.exists(log_file):
        os.remove(log_file)
    if os.path.exists(old_log_file):
        os.remove(old_log_file)

    # Run 3 times
    for i in range(3):
        subprocess.run([script], check=True)

    assert os.path.isfile(log_file), f"{log_file} was not created."
    with open(log_file, "r") as f:
        lines = f.readlines()

    assert len(lines) == 3, f"Expected 3 lines in {log_file} after 3 runs, got {len(lines)}."
    for idx, line in enumerate(lines):
        assert line.strip().endswith("JST"), f"Line {idx+1} in {log_file} does not end with JST: {line.strip()}"

    # Run 4th time
    subprocess.run([script], check=True)

    assert os.path.isfile(old_log_file), f"{old_log_file} was not created after 4th run (rotation failed)."
    with open(old_log_file, "r") as f:
        old_lines = f.readlines()
    assert len(old_lines) == 3, f"Expected 3 lines in {old_log_file}, got {len(old_lines)}."

    with open(log_file, "r") as f:
        new_lines = f.readlines()
    assert len(new_lines) == 1, f"Expected 1 line in {log_file} after rotation, got {len(new_lines)}."
    assert new_lines[0].strip().endswith("JST"), f"New line in {log_file} does not end with JST: {new_lines[0].strip()}"

def test_cron_schedule():
    cron_file = "/home/user/cron_schedule"
    assert os.path.isfile(cron_file), f"Cron schedule file {cron_file} is missing."

    with open(cron_file, "r") as f:
        content = f.read().strip()

    pattern = r"^(\*/15|0,15,30,45)\s+\*\s+\*\s+\*\s+\*\s+/home/user/logger_script\.sh$"
    assert re.match(pattern, content), f"Cron schedule content '{content}' does not match expected format."