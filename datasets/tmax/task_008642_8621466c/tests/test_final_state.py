# test_final_state.py
import os
import subprocess
import tempfile

def test_source_file_exists():
    assert os.path.isfile("/home/user/etl_pipeline.cpp"), "/home/user/etl_pipeline.cpp does not exist."

def test_executable_exists():
    assert os.path.isfile("/home/user/etl_pipeline"), "/home/user/etl_pipeline does not exist. Did you compile it?"
    assert os.access("/home/user/etl_pipeline", os.X_OK), "/home/user/etl_pipeline is not executable."

def test_etl_results_content():
    expected_content = "user_id,weighted_out_degree\n106,1000\n101,900\n104,300\n102,200"
    assert os.path.isfile("/home/user/etl_results.csv"), "/home/user/etl_results.csv does not exist."
    with open("/home/user/etl_results.csv", "r") as f:
        content = f.read().strip()
    assert content == expected_content, "The content of /home/user/etl_results.csv is incorrect for the provided dataset."

def test_etl_pipeline_logic_hidden_dataset():
    """Verify the executable logic using a dynamically generated hidden dataset."""
    with tempfile.TemporaryDirectory() as tmpdir:
        entities_path = os.path.join(tmpdir, "entities.dat")
        edges_path = os.path.join(tmpdir, "edges.dat")
        out_path = os.path.join(tmpdir, "out.csv")

        # Create hidden entities
        with open(entities_path, "w") as f:
            f.write("201,Zack,Engineering,Manager\n")
            f.write("202,Yara,Engineering,Dev\n")
            f.write("203,Xena,Sales,Rep\n")

        # Create hidden edges
        with open(edges_path, "w") as f:
            f.write("m1,201,202,100,50\n")
            f.write("m2,201,203,110,25\n")
            f.write("m3,202,201,120,100\n")

        # Run the executable
        result = subprocess.run(
            ["/home/user/etl_pipeline", entities_path, edges_path, out_path],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Executable failed with return code {result.returncode}. Stderr: {result.stderr}"
        assert os.path.isfile(out_path), "Executable did not create the output file when run on the hidden dataset."

        with open(out_path, "r") as f:
            content = f.read().strip()

        expected_content = "user_id,weighted_out_degree\n202,100\n201,75"
        assert content == expected_content, f"The logic of the ETL pipeline is incorrect on a hidden dataset.\nExpected:\n{expected_content}\nGot:\n{content}"