# test_final_state.py
import os
import subprocess
import tempfile
import filecmp
import pytest

def test_vendored_package_installed():
    try:
        import fast_log_parser
    except ImportError:
        pytest.fail("The vendored package 'fast_log_parser' is not installed or cannot be imported.")

def test_sanitizer_script_exists():
    path = "/home/user/log_sanitizer/sanitizer.py"
    assert os.path.isfile(path), f"Sanitizer script not found at {path}"

def test_sanitizer_functionality():
    script_path = "/home/user/log_sanitizer/sanitizer.py"
    clean_in = "/app/corpora/clean"
    evil_in = "/app/corpora/evil"

    assert os.path.isdir(clean_in), f"Clean corpus missing at {clean_in}"
    assert os.path.isdir(evil_in), f"Evil corpus missing at {evil_in}"

    with tempfile.TemporaryDirectory() as clean_out, tempfile.TemporaryDirectory() as evil_out:
        # Run script on clean corpus
        res_clean = subprocess.run(
            ["python3", script_path, clean_in, clean_out],
            capture_output=True, text=True
        )
        assert res_clean.returncode == 0, f"Script failed on clean corpus:\n{res_clean.stderr}"

        # Run script on evil corpus
        res_evil = subprocess.run(
            ["python3", script_path, evil_in, evil_out],
            capture_output=True, text=True
        )
        assert res_evil.returncode == 0, f"Script failed on evil corpus:\n{res_evil.stderr}"

        # Verify clean corpus
        clean_in_files = set(f for f in os.listdir(clean_in) if f.endswith('.log'))
        clean_out_files = set(f for f in os.listdir(clean_out) if f.endswith('.log'))

        missing_clean = clean_in_files - clean_out_files
        assert not missing_clean, f"Clean output is missing files: {missing_clean}"

        modified_clean = []
        for f in clean_in_files:
            in_file = os.path.join(clean_in, f)
            out_file = os.path.join(clean_out, f)
            if not filecmp.cmp(in_file, out_file, shallow=False):
                modified_clean.append(f)

        # Verify evil corpus
        evil_in_files = set(f for f in os.listdir(evil_in) if f.endswith('.log'))
        evil_out_files = set(f for f in os.listdir(evil_out) if f.endswith('.log'))

        bypassed_evil = []
        for f in evil_in_files:
            out_file = os.path.join(evil_out, f)
            if os.path.exists(out_file) and os.path.getsize(out_file) > 0:
                bypassed_evil.append(f)

        # Summary assertions
        error_msgs = []
        if bypassed_evil:
            error_msgs.append(f"{len(bypassed_evil)} of {len(evil_in_files)} evil bypassed: {', '.join(bypassed_evil)}")
        if modified_clean:
            error_msgs.append(f"{len(modified_clean)} of {len(clean_in_files)} clean modified: {', '.join(modified_clean)}")

        if error_msgs:
            pytest.fail(" | ".join(error_msgs))