# test_final_state.py
import os
import subprocess
import tempfile
import pytest

CLEAN_DIR = "/app/data/clean"
EVIL_DIR = "/app/data/evil"
PIPELINE_SCRIPT = "/home/user/pipeline.py"
BENCHMARK_LOG = "/home/user/benchmark_log.txt"

def test_tok_speed_installed():
    """Check that tok_speed is installed and can be imported."""
    try:
        import tok_speed
    except ImportError:
        pytest.fail("tok_speed module is not installed or cannot be imported.")

    assert hasattr(tok_speed, "tokenize"), "tok_speed does not have a tokenize function."
    tokens = tok_speed.tokenize("hello world")
    assert tokens == ["hello", "world"], f"Expected ['hello', 'world'], got {tokens}"

def test_pipeline_script_exists():
    """Check that the pipeline script exists."""
    assert os.path.isfile(PIPELINE_SCRIPT), f"Pipeline script {PIPELINE_SCRIPT} does not exist."

def test_pipeline_on_clean_corpus():
    """Check that the pipeline accepts clean files and writes the output and benchmark log."""
    assert os.path.isdir(CLEAN_DIR), f"Clean directory {CLEAN_DIR} does not exist."
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    assert len(clean_files) > 0, "No clean files found."

    import tok_speed

    failed_files = []

    # Read initial benchmark log lines if it exists
    initial_log_lines = 0
    if os.path.isfile(BENCHMARK_LOG):
        with open(BENCHMARK_LOG, "r") as f:
            initial_log_lines = len(f.readlines())

    for clean_file in clean_files:
        with tempfile.NamedTemporaryFile(delete=False) as temp_out:
            temp_out_path = temp_out.name

        try:
            result = subprocess.run(
                ["python3", PIPELINE_SCRIPT, clean_file, temp_out_path],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                failed_files.append((os.path.basename(clean_file), f"Exit code {result.returncode} instead of 0"))
                continue

            if not os.path.isfile(temp_out_path):
                failed_files.append((os.path.basename(clean_file), "Output file not created"))
                continue

            with open(clean_file, "r") as f:
                original_text = f.read()

            expected_tokens = tok_speed.tokenize(original_text)
            expected_output = " ".join(expected_tokens)

            with open(temp_out_path, "r") as f:
                actual_output = f.read()

            if actual_output != expected_output:
                failed_files.append((os.path.basename(clean_file), "Output tokens do not match expected space-separated tokens"))

        finally:
            if os.path.exists(temp_out_path):
                os.remove(temp_out_path)

    if failed_files:
        msgs = [f"{f}: {r}" for f, r in failed_files]
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/failed:\n" + "\n".join(msgs))

    # Check benchmark log
    assert os.path.isfile(BENCHMARK_LOG), f"Benchmark log {BENCHMARK_LOG} was not created."
    with open(BENCHMARK_LOG, "r") as f:
        log_lines = f.readlines()

    new_log_lines = len(log_lines) - initial_log_lines
    assert new_log_lines >= len(clean_files), f"Expected at least {len(clean_files)} new lines in benchmark log, got {new_log_lines}"

    # Check that the last lines are floats
    for line in log_lines[-len(clean_files):]:
        try:
            float(line.strip())
        except ValueError:
            pytest.fail(f"Benchmark log contains non-float value: {line.strip()}")

def test_pipeline_on_evil_corpus():
    """Check that the pipeline rejects evil files."""
    assert os.path.isdir(EVIL_DIR), f"Evil directory {EVIL_DIR} does not exist."
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    assert len(evil_files) > 0, "No evil files found."

    failed_files = []

    for evil_file in evil_files:
        with tempfile.NamedTemporaryFile(delete=False) as temp_out:
            temp_out_path = temp_out.name
        os.remove(temp_out_path) # Pipeline should not create it, or if it does, exit 1

        try:
            result = subprocess.run(
                ["python3", PIPELINE_SCRIPT, evil_file, temp_out_path],
                capture_output=True,
                text=True
            )

            if result.returncode != 1:
                failed_files.append((os.path.basename(evil_file), f"Exit code {result.returncode} instead of 1"))

            if os.path.exists(temp_out_path):
                # If it created the file but still exited 1, the prompt says "Do not create or write to the output file."
                failed_files.append((os.path.basename(evil_file), "Output file was created for rejected document"))

        finally:
            if os.path.exists(temp_out_path):
                os.remove(temp_out_path)

    if failed_files:
        msgs = [f"{f}: {r}" for f, r in failed_files]
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed/failed:\n" + "\n".join(msgs))