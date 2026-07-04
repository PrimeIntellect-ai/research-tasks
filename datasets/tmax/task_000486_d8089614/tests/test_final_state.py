# test_final_state.py
import os
import glob
import subprocess
import tempfile
import shutil

def test_detector_executable_exists():
    assert os.path.isfile("/home/user/detector"), "The compiled tool /home/user/detector is missing."
    assert os.access("/home/user/detector", os.X_OK), "/home/user/detector is not executable."

def test_detector_accuracy():
    clean_dir = "/home/user/corpus/clean"
    evil_dir = "/home/user/corpus/evil"

    clean_files = [os.path.basename(f) for f in glob.glob(os.path.join(clean_dir, "*.json"))]
    evil_files = [os.path.basename(f) for f in glob.glob(os.path.join(evil_dir, "*.json"))]

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    with tempfile.TemporaryDirectory() as temp_input_dir:
        # Copy all files to a single temp directory
        for f in clean_files:
            shutil.copy(os.path.join(clean_dir, f), os.path.join(temp_input_dir, f))
        for f in evil_files:
            shutil.copy(os.path.join(evil_dir, f), os.path.join(temp_input_dir, f))

        temp_output_log = os.path.join(temp_input_dir, "results.log")

        # Run the detector
        cmd = ["/home/user/detector", "-input", temp_input_dir, "-output", temp_output_log]
        result = subprocess.run(cmd, capture_output=True, text=True)

        assert result.returncode == 0, f"Detector failed to run. stderr: {result.stderr}"
        assert os.path.isfile(temp_output_log), "Detector did not create the output log file."

        with open(temp_output_log, "r") as f:
            log_lines = f.read().strip().splitlines()

        results_map = {}
        for line in log_lines:
            parts = line.split(":")
            if len(parts) == 2:
                filename = parts[0].strip()
                status = parts[1].strip()
                results_map[filename] = status

        # Verify clean files
        clean_modified = []
        for cf in clean_files:
            if results_map.get(cf) != "CLEAN":
                clean_modified.append(cf)

        # Verify evil files
        evil_bypassed = []
        for ef in evil_files:
            if results_map.get(ef) != "EVIL":
                evil_bypassed.append(ef)

        error_msg = []
        if clean_modified:
            error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (flagged as EVIL or missing): {', '.join(clean_modified)}")
        if evil_bypassed:
            error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed (flagged as CLEAN or missing): {', '.join(evil_bypassed)}")

        assert not clean_modified and not evil_bypassed, " | ".join(error_msg)