# test_final_state.py
import os
import subprocess
import re

def test_directories_exist():
    dirs = [
        "/home/user/pipeline/input",
        "/home/user/pipeline/output",
        "/home/user/pipeline/archive",
        "/home/user/pipeline/bin"
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory missing: {d}"

def test_detector_compiles_and_process_script_runs():
    detector_bin = "/home/user/pipeline/bin/detector"
    process_script = "/home/user/pipeline/bin/process.sh"

    assert os.path.isfile(detector_bin), f"C executable missing: {detector_bin}"
    assert os.access(detector_bin, os.X_OK), f"C executable not executable: {detector_bin}"

    assert os.path.isfile(process_script), f"Bash script missing: {process_script}"
    assert os.access(process_script, os.X_OK), f"Bash script not executable: {process_script}"

    # Create dummy data 1 (with anomalies)
    csv1_path = "/home/user/pipeline/input/test1.csv"
    with open(csv1_path, "w") as f:
        f.write("1000,10.0,10.0\n")
        f.write("1001,12.0,11.0\n")
        f.write("1002,100.0,11.0\n")
        f.write("1003,101.0,12.0\n")
        f.write("1004,101.0,90.0\n")

    # Create dummy data 2 (no anomalies)
    csv2_path = "/home/user/pipeline/input/test2.csv"
    with open(csv2_path, "w") as f:
        f.write("2000,10.0,10.0\n")
        f.write("2001,12.0,11.0\n")

    # Run the script
    result = subprocess.run([process_script], capture_output=True, text=True)
    assert result.returncode == 0, f"process.sh failed with exit code {result.returncode}\nStderr: {result.stderr}"

    # Check output 1
    out1_path = "/home/user/pipeline/output/test1.out"
    assert os.path.isfile(out1_path), f"Output file missing: {out1_path}"
    with open(out1_path, "r") as f:
        out1_content = f.read()

    assert "Mean X: 64.80" in out1_content, f"test1.out missing 'Mean X: 64.80'. Got:\n{out1_content}"
    assert "Mean Y: 26.80" in out1_content, f"test1.out missing 'Mean Y: 26.80'. Got:\n{out1_content}"
    assert "Anomaly Count: 2" in out1_content, f"test1.out missing 'Anomaly Count: 2'. Got:\n{out1_content}"
    assert "Anomaly Timestamps: 1002,1004" in out1_content, f"test1.out missing 'Anomaly Timestamps: 1002,1004'. Got:\n{out1_content}"

    # Check output 2
    out2_path = "/home/user/pipeline/output/test2.out"
    assert os.path.isfile(out2_path), f"Output file missing: {out2_path}"
    with open(out2_path, "r") as f:
        out2_content = f.read()

    assert "Mean X: 11.00" in out2_content, f"test2.out missing 'Mean X: 11.00'. Got:\n{out2_content}"
    assert "Mean Y: 10.50" in out2_content, f"test2.out missing 'Mean Y: 10.50'. Got:\n{out2_content}"
    assert "Anomaly Count: 0" in out2_content, f"test2.out missing 'Anomaly Count: 0'. Got:\n{out2_content}"
    assert "Anomaly Timestamps: None" in out2_content, f"test2.out missing 'Anomaly Timestamps: None'. Got:\n{out2_content}"

    # Check that files were moved to archive
    assert not os.path.isfile(csv1_path), f"File {csv1_path} was not moved out of input directory"
    assert not os.path.isfile(csv2_path), f"File {csv2_path} was not moved out of input directory"
    assert os.path.isfile("/home/user/pipeline/archive/test1.csv"), "test1.csv not found in archive directory"
    assert os.path.isfile("/home/user/pipeline/archive/test2.csv"), "test2.csv not found in archive directory"

def test_cron_file():
    cron_file = "/home/user/pipeline.cron"
    assert os.path.isfile(cron_file), f"Cron file missing: {cron_file}"

    with open(cron_file, "r") as f:
        content = f.read().strip()

    # Check for */5 * * * * or 0,5,10,... * * * *
    cron_pattern = r"^(?:\*/5|0,5,10,15,20,25,30,35,40,45,50,55)\s+\*\s+\*\s+\*\s+\*\s+/home/user/pipeline/bin/process\.sh"

    match = False
    for line in content.splitlines():
        if re.search(cron_pattern, line.strip()):
            match = True
            break

    assert match, f"Cron file does not contain the correct 5-minute schedule for process.sh. Got:\n{content}"