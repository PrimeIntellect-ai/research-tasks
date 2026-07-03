# test_final_state.py
import os
import subprocess

def test_processed_corpus_parquet_exists_and_valid():
    path = '/home/user/processed_corpus.parquet'
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

    with open(path, 'rb') as f:
        magic = f.read(4)
        assert magic == b'PAR1', f"File {path} is not a valid Parquet file (missing PAR1 magic bytes)."

def test_parquet_contents_via_subprocess():
    # Since we can only use standard library in the test, we use subprocess 
    # to run a Python snippet that utilizes pandas (which the student installed).
    script = """
import sys
try:
    import pandas as pd
except ImportError:
    sys.exit("pandas not installed")

try:
    df = pd.read_parquet('/home/user/processed_corpus.parquet')
except Exception as e:
    sys.exit(f"Failed to read parquet: {e}")

if len(df) != 5:
    sys.exit(f"Expected 5 rows, got {len(df)}")

expected_cols = {'article_id', 'text', 'source', 'tokens', 'token_count'}
if not expected_cols.issubset(df.columns):
    sys.exit(f"Missing columns. Expected at least {expected_cols}, got {list(df.columns)}")

a001 = df[df['article_id'] == 'A001']
if len(a001) == 0:
    sys.exit("Row with article_id 'A001' not found.")

a001 = a001.iloc[0]
expected_tokens = ["data", "science", "is", "the", "sexiest", "job", "of", "the", "21st", "century", "100", "true"]

if list(a001['tokens']) != expected_tokens:
    sys.exit(f"Tokenization failed for A001. Got {list(a001['tokens'])}")

if a001['token_count'] != 12:
    sys.exit(f"token_count failed for A001. Expected 12, got {a001['token_count']}")
"""
    result = subprocess.run(['python3', '-c', script], capture_output=True, text=True)
    assert result.returncode == 0, f"Parquet content validation failed:\n{result.stderr}\n{result.stdout}"

def test_token_distribution_png_exists():
    path = '/home/user/token_distribution.png'
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

    with open(path, 'rb') as f:
        header = f.read(8)
        assert header == b'\x89PNG\r\n\x1a\n', f"File {path} is not a valid PNG file."

def test_plot_distribution_script_fixed():
    path = '/home/user/plot_distribution.py'
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    assert 'savefig' in content, f"The script {path} does not contain 'savefig'."

    for line in content.splitlines():
        if 'show()' in line:
            assert line.lstrip().startswith('#'), f"Found active 'show()' in {path}, which will fail in a headless environment. It must be removed or commented out."