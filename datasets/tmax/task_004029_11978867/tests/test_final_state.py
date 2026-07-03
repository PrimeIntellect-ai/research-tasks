# test_final_state.py
import os
import shutil
import subprocess
import tempfile

def test_wal_filter():
    go_file = "/home/user/wal_filter.go"
    assert os.path.isfile(go_file), f"The required Go program {go_file} does not exist."

    clean_corpus = "/app/corpus/clean"
    evil_corpus = "/app/corpus/evil"

    assert os.path.isdir(clean_corpus), f"Clean corpus directory {clean_corpus} is missing."
    assert os.path.isdir(evil_corpus), f"Evil corpus directory {evil_corpus} is missing."

    clean_files = set(os.listdir(clean_corpus))
    evil_files = set(os.listdir(evil_corpus))

    with tempfile.TemporaryDirectory() as temp_in, \
         tempfile.TemporaryDirectory() as temp_out, \
         tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_log:

        log_path = temp_log.name

        # Populate the input directory with both clean and evil files
        for f in clean_files:
            shutil.copy(os.path.join(clean_corpus, f), os.path.join(temp_in, f))
        for f in evil_files:
            shutil.copy(os.path.join(evil_corpus, f), os.path.join(temp_in, f))

        # Execute the agent's Go program
        try:
            subprocess.run(
                ["go", "run", go_file, "-in", temp_in, "-out", temp_out, "-log", log_path],
                check=True,
                capture_output=True,
                text=True,
                timeout=30
            )
        except subprocess.CalledProcessError as e:
            assert False, f"Go program failed to execute or compile:\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
        except subprocess.TimeoutExpired:
            assert False, "Go program timed out after 30 seconds."

        # Parse the log file
        with open(log_path, 'r') as f:
            log_lines = f.read().splitlines()

        log_entries = {}
        for line in log_lines:
            if ":" in line:
                fname, status = line.split(":", 1)
                log_entries[fname.strip()] = status.strip()

        out_files = set(os.listdir(temp_out))

        evil_bypassed = []
        clean_modified_or_missing = []

        # Verify evil files were rejected and logged correctly
        for f in evil_files:
            if f in out_files:
                evil_bypassed.append(f"{f} (copied to out dir)")
            elif log_entries.get(f) != "EVIL":
                evil_bypassed.append(f"{f} (not logged as EVIL)")

        # Verify clean files were preserved and logged correctly
        for f in clean_files:
            if f not in out_files:
                clean_modified_or_missing.append(f"{f} (missing from out dir)")
            else:
                orig = os.path.join(clean_corpus, f)
                copied = os.path.join(temp_out, f)
                with open(orig, 'rb') as f1, open(copied, 'rb') as f2:
                    if f1.read() != f2.read():
                        clean_modified_or_missing.append(f"{f} (content modified)")

            if log_entries.get(f) != "CLEAN":
                clean_modified_or_missing.append(f"{f} (not logged as CLEAN)")

        error_msgs = []
        if evil_bypassed:
            error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
        if clean_modified_or_missing:
            error_msgs.append(f"{len(clean_modified_or_missing)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified_or_missing)}")

        if error_msgs:
            assert False, " | ".join(error_msgs)