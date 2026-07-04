# test_final_state.py

import os
import glob
import tempfile
import subprocess
import pytest

def test_correlation_plot_generated():
    """Verify that the plot_correlations.py script generates a non-empty image."""
    plot_script = "/app/plot_correlations.py"
    output_image = "/home/user/correlation.png"

    # Run the script if the image doesn't exist yet, but ideally the user should have run it.
    # The prompt says "Fix the script so it correctly renders and saves...". 
    # Let's check if the image exists and is non-empty.
    if not os.path.exists(output_image):
        # Maybe the user didn't run it, let's run it to be sure
        subprocess.run(["python3", plot_script], capture_output=True)

    assert os.path.isfile(output_image), f"{output_image} does not exist."
    assert os.path.getsize(output_image) > 1000, f"{output_image} seems to be empty or invalid (size: {os.path.getsize(output_image)} bytes)."

def test_adversarial_corpus_filtering():
    """Verify the filter_datasets.py script correctly filters clean and evil corpora."""
    filter_script = "/home/user/filter_datasets.py"
    assert os.path.isfile(filter_script), f"Filter script {filter_script} does not exist."

    clean_corpus = "/app/corpus/clean"
    evil_corpus = "/app/corpus/evil"

    with tempfile.TemporaryDirectory() as eval_clean, tempfile.TemporaryDirectory() as eval_evil:
        # Run on clean corpus
        res_clean = subprocess.run(["python3", filter_script, clean_corpus, eval_clean], capture_output=True, text=True)
        assert res_clean.returncode == 0, f"Script failed on clean corpus: {res_clean.stderr}"

        # Run on evil corpus
        res_evil = subprocess.run(["python3", filter_script, evil_corpus, eval_evil], capture_output=True, text=True)
        assert res_evil.returncode == 0, f"Script failed on evil corpus: {res_evil.stderr}"

        # Check clean corpus: all 10 files should be preserved
        clean_input_files = set(os.path.basename(f) for f in glob.glob(os.path.join(clean_corpus, "*.npy")))
        clean_output_files = set(os.path.basename(f) for f in glob.glob(os.path.join(eval_clean, "*.npy")))

        missing_clean = clean_input_files - clean_output_files
        assert len(clean_output_files) == len(clean_input_files), f"{len(missing_clean)} of {len(clean_input_files)} clean files modified/rejected: {missing_clean}"

        # Check evil corpus: 0 files should be preserved
        evil_input_files = set(os.path.basename(f) for f in glob.glob(os.path.join(evil_corpus, "*.npy")))
        evil_output_files = set(os.path.basename(f) for f in glob.glob(os.path.join(eval_evil, "*.npy")))

        assert len(evil_output_files) == 0, f"{len(evil_output_files)} of {len(evil_input_files)} evil files bypassed: {evil_output_files}"

def test_benchmark_file_exists_and_valid():
    """Verify the benchmark.txt file exists and contains a valid float."""
    benchmark_file = "/home/user/benchmark.txt"
    assert os.path.isfile(benchmark_file), f"Benchmark file {benchmark_file} does not exist."

    with open(benchmark_file, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
        assert val > 0, "Benchmark time should be greater than 0."
    except ValueError:
        pytest.fail(f"Benchmark file does not contain a valid float. Content: '{content}'")