# test_final_state.py

import os
import stat
import time
import subprocess

def test_parse_logs_performance_and_output():
    script_path = "/home/user/parse_logs.py"
    assert os.path.isfile(script_path), f"Parsing script {script_path} does not exist."

    summary_path = "/home/user/summary.csv"
    if os.path.exists(summary_path):
        os.remove(summary_path)

    start_time = time.time()
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    duration = time.time() - start_time

    assert result.returncode == 0, f"parse_logs.py failed with error:\n{result.stderr}"

    assert duration < 1.5, f"Execution time {duration:.2f}s exceeded the 1.5s threshold. The ijson C-extension might not be built correctly or pure Python fallback was used."

    expected_path = "/tmp/expected_summary.csv"
    assert os.path.isfile(summary_path), f"Output file {summary_path} was not created."
    assert os.path.isfile(expected_path), f"Expected summary file {expected_path} is missing."

    with open(summary_path, "r") as f:
        actual_content = f.read().strip()
    with open(expected_path, "r") as f:
        expected_content = f.read().strip()

    assert actual_content == expected_content, f"The contents of summary.csv do not match the expected output.\nExpected:\n{expected_content}\nActual:\n{actual_content}"

def test_backup_script():
    backup_script = "/home/user/backup.sh"
    assert os.path.isfile(backup_script), f"Backup script {backup_script} does not exist."

    st = os.stat(backup_script)
    assert bool(st.st_mode & stat.S_IXUSR), f"Backup script {backup_script} is not executable."

    src_dir = "/tmp/test_backup_src"
    dest_dir = "/tmp/test_backup_dest"
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(dest_dir, exist_ok=True)

    test_file = os.path.join(src_dir, "test.txt")
    with open(test_file, "w") as f:
        f.write("test data")

    result1 = subprocess.run([backup_script, src_dir, dest_dir], capture_output=True, text=True)
    assert result1.returncode == 0, f"Backup script failed on first run:\n{result1.stderr}"

    backups1 = sorted(os.listdir(dest_dir))
    assert len(backups1) == 1, "Expected exactly one backup folder after first run."

    time.sleep(1.1) 
    result2 = subprocess.run([backup_script, src_dir, dest_dir], capture_output=True, text=True)
    assert result2.returncode == 0, f"Backup script failed on second run:\n{result2.stderr}"

    backups2 = sorted(os.listdir(dest_dir))
    assert len(backups2) == 2, "Expected exactly two backup folders after second run."

    file1 = os.path.join(dest_dir, backups2[0], "test.txt")
    file2 = os.path.join(dest_dir, backups2[1], "test.txt")

    assert os.path.isfile(file1), "File missing in first backup."
    assert os.path.isfile(file2), "File missing in second backup."

    stat1 = os.stat(file1)
    stat2 = os.stat(file2)

    assert stat1.st_ino == stat2.st_ino, "The second backup did not create hard links to the first backup. Did you use --link-dest correctly?"