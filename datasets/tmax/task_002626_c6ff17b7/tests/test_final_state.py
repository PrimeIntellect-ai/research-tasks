# test_final_state.py
import os
import subprocess
import tempfile

def test_analyze_script_exists_and_executable():
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_analyze_script_logic():
    script_path = "/home/user/analyze.sh"

    test_csv_content = """10,20
20,30
10,40
40,30
30,50
60,20
"""

    expected_degrees = """node,in_degree,out_degree
10,0,2
20,2,1
30,2,1
40,1,1
50,1,0
60,0,1
"""

    expected_paths = """a,b,c
10,20,30
10,40,30
20,30,50
40,30,50
60,20,30
"""

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as tmp:
        tmp.write(test_csv_content)
        tmp_path = tmp.name

    try:
        # Run the script
        result = subprocess.run([script_path, tmp_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nStderr: {result.stderr}"

        # Check degrees.csv
        degrees_path = "/home/user/degrees.csv"
        assert os.path.isfile(degrees_path), f"Output file {degrees_path} was not created."
        with open(degrees_path, "r") as f:
            degrees_content = f.read()
        assert degrees_content.strip() == expected_degrees.strip(), f"Content of {degrees_path} is incorrect.\nExpected:\n{expected_degrees}\nGot:\n{degrees_content}"

        # Check paths.csv
        paths_path = "/home/user/paths.csv"
        assert os.path.isfile(paths_path), f"Output file {paths_path} was not created."
        with open(paths_path, "r") as f:
            paths_content = f.read()
        assert paths_content.strip() == expected_paths.strip(), f"Content of {paths_path} is incorrect.\nExpected:\n{expected_paths}\nGot:\n{paths_content}"

    finally:
        os.remove(tmp_path)