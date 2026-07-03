# test_final_state.py
import os
import subprocess

def test_embeddings_file_exists():
    """Check if the input embeddings file exists."""
    assert os.path.isfile('/home/user/artifacts/embeddings.csv'), "The /home/user/artifacts/embeddings.csv file is missing."

def test_process_script_exists_and_executable():
    """Check if the process script exists and is executable."""
    script_path = '/home/user/process.sh'
    assert os.path.isfile(script_path), f"The script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_process_script_output():
    """Run the script and verify the output matches the expected L2 norms."""
    script_path = '/home/user/process.sh'
    output_path = '/home/user/processed_norms.csv'

    # Run the script to ensure it generates the correct file
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    assert os.path.isfile(output_path), f"The output file {output_path} was not generated."

    with open(output_path, 'r') as f:
        content = f.read().strip()

    expected_content = "id,l2_norm\nexp1,3.20\nexp2,4.03\nexp3,1.12\nexp4,1.80"

    assert content == expected_content, f"The content of {output_path} does not match the expected output.\nExpected:\n{expected_content}\nGot:\n{content}"