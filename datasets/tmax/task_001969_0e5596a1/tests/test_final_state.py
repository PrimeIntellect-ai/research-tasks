# test_final_state.py
import os
import stat
import subprocess
import tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def test_process_doc_script_exists_and_executable():
    script_path = Path("/home/user/process_doc.sh")
    assert script_path.exists(), f"Script not found at {script_path}"
    assert script_path.is_file(), f"{script_path} is not a file"
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable"

def run_script(input_path, output_path):
    script_path = "/home/user/process_doc.sh"
    result = subprocess.run(
        ["bash", script_path, str(input_path), str(output_path)],
        capture_output=True,
        text=True
    )
    return input_path, result.returncode, result.stdout, result.stderr

def test_adversarial_corpus_and_concurrency():
    clean_dir = Path("/app/corpus/clean")
    evil_dir = Path("/app/corpus/evil")
    index_file = Path("/home/user/master_index.txt")

    # Clear index file if it exists, to ensure a clean run for the test
    if index_file.exists():
        index_file.unlink()

    clean_files = list(clean_dir.iterdir()) if clean_dir.exists() else []
    evil_files = list(evil_dir.iterdir()) if evil_dir.exists() else []

    assert len(clean_files) > 0, "No clean files found to test."
    assert len(evil_files) > 0, "No evil files found to test."

    futures = []
    results = []

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit clean files
            for cf in clean_files:
                out_path = tmp_path / f"out_{cf.name}"
                futures.append(executor.submit(run_script, cf, out_path))

            # Submit evil files
            for ef in evil_files:
                out_path = tmp_path / f"out_{ef.name}"
                futures.append(executor.submit(run_script, ef, out_path))

            for future in as_completed(futures):
                results.append(future.result())

        # Analyze results
        clean_failed = []
        evil_bypassed = []

        clean_out_basenames = []

        for input_path, retcode, stdout, stderr in results:
            if str(clean_dir) in str(input_path):
                if retcode != 0:
                    clean_failed.append(input_path.name)
                else:
                    out_path = tmp_path / f"out_{input_path.name}"
                    assert out_path.exists(), f"Output file {out_path} was not created for clean file {input_path.name}"
                    content = out_path.read_text(errors="replace")
                    assert content.startswith("TECHDOC-V1"), f"Decoded content for {input_path.name} does not start with 'TECHDOC-V1'"
                    clean_out_basenames.append(out_path.name)
            elif str(evil_dir) in str(input_path):
                if retcode == 0:
                    evil_bypassed.append(input_path.name)

        # Reporting
        if clean_failed or evil_bypassed:
            msg = []
            if evil_bypassed:
                msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
            if clean_failed:
                msg.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/failed: {', '.join(clean_failed)}")
            raise AssertionError(" | ".join(msg))

        # Check index file
        assert index_file.exists(), f"Master index file {index_file} was not created."
        index_contents = index_file.read_text().splitlines()

        # Check that index contains exactly the expected basenames
        expected_basenames = sorted(clean_out_basenames)
        actual_basenames = sorted([line.strip() for line in index_contents if line.strip()])

        assert expected_basenames == actual_basenames, (
            f"Index file contents do not match expected output basenames.\n"
            f"Expected: {expected_basenames}\n"
            f"Actual: {actual_basenames}"
        )