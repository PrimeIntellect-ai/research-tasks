# test_final_state.py
import os
import subprocess
import glob

def test_go_httpbin_compiled():
    binary_path = '/app/go-httpbin/httpbin'
    assert os.path.isfile(binary_path), f"The binary {binary_path} was not compiled."
    assert os.access(binary_path, os.X_OK), f"The binary {binary_path} is not executable."

    result = subprocess.run([binary_path, '-h'], capture_output=True, text=True)
    assert result.returncode == 0, f"Running '{binary_path} -h' failed with exit code {result.returncode}."

def test_gateway_filter_exists_and_executable():
    script_path = '/home/user/gateway_filter.sh'
    assert os.path.isfile(script_path), f"The script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_gateway_filter_against_corpora():
    script_path = '/home/user/gateway_filter.sh'
    clean_dir = '/app/corpora/clean/'
    evil_dir = '/app/corpora/evil/'

    clean_files = glob.glob(os.path.join(clean_dir, '*'))
    evil_files = glob.glob(os.path.join(evil_dir, '*'))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}."
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}."

    clean_failed = []
    for f in clean_files:
        if not os.path.isfile(f): continue
        with open(f, 'r') as fd:
            payload = fd.read()
        result = subprocess.run(['bash', script_path], input=payload, capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "ACCEPT":
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        if not os.path.isfile(f): continue
        with open(f, 'r') as fd:
            payload = fd.read()
        result = subprocess.run(['bash', script_path], input=payload, capture_output=True, text=True)
        if result.returncode != 1 or result.stdout.strip() != "REJECT":
            evil_failed.append(os.path.basename(f))

    error_msgs = []
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified or rejected: {', '.join(clean_failed)}")

    if error_msgs:
        raise AssertionError(" | ".join(error_msgs))

def test_benchmark_artifacts():
    bench_script = '/home/user/benchmark.sh'
    bench_results = '/home/user/benchmark_results.txt'

    assert os.path.isfile(bench_script), f"The benchmark script {bench_script} is missing."
    assert os.path.isfile(bench_results), f"The benchmark results file {bench_results} is missing."

    with open(bench_results, 'r') as f:
        content = f.read().strip()
    assert len(content) > 0, f"The benchmark results file {bench_results} is empty."