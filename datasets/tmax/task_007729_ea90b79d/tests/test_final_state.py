# test_final_state.py

import os
import stat
import pytest

def test_prob_B_better_output():
    filepath = '/home/user/prob_B_better.txt'
    assert os.path.isfile(filepath), f"File {filepath} does not exist. The Bayesian inference script may not have run or saved the output correctly."

    with open(filepath, 'r') as f:
        content = f.read().strip()

    assert content == "0.9413", f"Expected probability in {filepath} to be '0.9413', but got '{content}'."

def test_posterior_plot_generated():
    filepath = '/home/user/posterior_plot.png'
    assert os.path.isfile(filepath), f"Plot file {filepath} does not exist. The plotting script may not have run or failed."

    # A purely blank/empty plot or failed save usually results in a very small file.
    # A typical matplotlib plot with lines and text is > 5KB.
    size = os.path.getsize(filepath)
    assert size > 5000, f"Plot file {filepath} is suspiciously small ({size} bytes). It might be blank or corrupted."

    # Check PNG magic number to ensure it's actually a PNG file
    with open(filepath, 'rb') as f:
        header = f.read(8)
    assert header == b'\x89PNG\r\n\x1a\n', f"File {filepath} is not a valid PNG image."

def test_run_pipeline_script_exists_and_executable():
    filepath = '/home/user/run_pipeline.sh'
    assert os.path.isfile(filepath), f"Pipeline script {filepath} does not exist."

    # Check if the file is executable
    st = os.stat(filepath)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"Pipeline script {filepath} is not executable. Please run 'chmod +x {filepath}'."

def test_plot_results_script_fixed():
    filepath = '/home/user/scripts/plot_results.py'
    assert os.path.isfile(filepath), f"Script {filepath} is missing."

    with open(filepath, 'r') as f:
        content = f.read()

    # The original script had plt.show() before plt.savefig(), which causes a blank image or crash in headless mode.
    # While the actual fix can vary (removing plt.show, moving it after savefig, or using 'Agg' backend),
    # the success is primarily proven by test_posterior_plot_generated.
    # However, we can assert that it doesn't do the exact broken sequence.
    broken_sequence = "plt.show()\nplt.savefig"
    assert broken_sequence not in content.replace(" ", ""), f"Script {filepath} still appears to call plt.show() immediately before plt.savefig(), which clears the canvas."