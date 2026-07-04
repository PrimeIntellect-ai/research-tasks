# test_final_state.py
import os
import re
import subprocess
import tempfile

def test_scripts_exist_and_executable():
    scripts = [
        "/home/user/tokenize.sh",
        "/home/user/bootstrap.sh",
        "/home/user/inference.sh",
        "/home/user/run_experiment.sh"
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Script {script} does not exist."
        assert os.access(script, os.X_OK), f"Script {script} is not executable."

def test_raw_data_exists_and_valid():
    raw_data_path = "/home/user/raw_data.txt"
    assert os.path.isfile(raw_data_path), f"{raw_data_path} does not exist."
    with open(raw_data_path, "r") as f:
        lines = f.readlines()
    assert len(lines) >= 10, f"{raw_data_path} must contain at least 10 lines."

def test_artifacts_exist():
    artifacts_dir = "/home/user/artifacts"
    assert os.path.isdir(artifacts_dir), f"Artifacts directory {artifacts_dir} does not exist."

    files = ["tokenized.txt", "baseline_score.txt", "bootstrap_scores.txt"]
    for file in files:
        assert os.path.isfile(os.path.join(artifacts_dir, file)), f"Artifact {file} is missing."

def test_tokenized_format():
    tokenized_path = "/home/user/artifacts/tokenized.txt"
    with open(tokenized_path, "r") as f:
        content = f.read()

    # Check for uppercase letters or punctuation (except spaces and newlines)
    assert not re.search(r'[A-Z]', content), "tokenized.txt contains uppercase letters."
    assert not re.search(r'[^a-z0-9 \n]', content), "tokenized.txt contains punctuation or invalid characters."

    # Check for consecutive spaces or leading/trailing spaces on lines
    for line in content.split('\n'):
        if line:
            assert not line.startswith(' '), "tokenized.txt contains leading spaces."
            assert not line.endswith(' '), "tokenized.txt contains trailing spaces."
            assert '  ' not in line, "tokenized.txt contains consecutive spaces."

def test_baseline_score_format():
    baseline_path = "/home/user/artifacts/baseline_score.txt"
    with open(baseline_path, "r") as f:
        content = f.read().strip()

    assert re.match(r'^-?[0-9]+\.[0-9]{4}$', content), f"baseline_score.txt does not contain a valid 4-decimal number: {content}"

def test_bootstrap_scores_format():
    bootstrap_path = "/home/user/artifacts/bootstrap_scores.txt"
    with open(bootstrap_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 5, f"bootstrap_scores.txt must contain exactly 5 lines, found {len(lines)}."
    for line in lines:
        assert re.match(r'^-?[0-9]+\.[0-9]{4}$', line), f"Invalid score format in bootstrap_scores.txt: {line}"

def test_tokenize_script_logic():
    input_text = "  Hello, World! This is a TEST...  \n  Another line!!!  \n"
    expected_output = "hello world this is a test\nanother line\n"

    result = subprocess.run(
        ["/home/user/tokenize.sh"],
        input=input_text,
        text=True,
        capture_output=True
    )

    assert result.stdout == expected_output, "tokenize.sh logic failed to properly clean and format text."

def test_inference_script_logic():
    # Test 1: single line
    input_text1 = "critical error warning info success resolved unknown\n"
    # -5 -3 -1 +0.5 +2 +3 +0 = -3.5000
    result1 = subprocess.run(
        ["/home/user/inference.sh"],
        input=input_text1,
        text=True,
        capture_output=True
    )
    assert result1.stdout.strip() == "-3.5000", f"inference.sh failed on single line test. Got {result1.stdout.strip()}"

    # Test 2: multiple lines
    input_text2 = "critical error\nsuccess resolved\n"
    # Line 1: -8.0
    # Line 2: 5.0
    # Mean: -1.5000
    result2 = subprocess.run(
        ["/home/user/inference.sh"],
        input=input_text2,
        text=True,
        capture_output=True
    )
    assert result2.stdout.strip() == "-1.5000", f"inference.sh failed on multi-line test. Got {result2.stdout.strip()}"

def test_bootstrap_script_logic():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
        for i in range(10):
            tmp.write(f"line {i}\n")
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            ["/home/user/bootstrap.sh", tmp_path],
            text=True,
            capture_output=True
        )
        output_lines = result.stdout.strip().split('\n')
        assert len(output_lines) == 10, "bootstrap.sh did not return the same number of lines as input."
        for line in output_lines:
            assert line.startswith("line "), "bootstrap.sh output contains invalid data."
    finally:
        os.remove(tmp_path)