# test_final_state.py

import os
import subprocess

def test_cypher_query_exists_and_valid():
    """Verify that the Cypher query file exists and contains a MATCH clause."""
    cypher_path = '/home/user/chain.cypher'
    assert os.path.exists(cypher_path), f"{cypher_path} does not exist."

    with open(cypher_path, 'r') as f:
        content = f.read().upper()
    assert "MATCH" in content, "The Cypher query does not contain a MATCH clause."

def test_c_pipeline_exists_and_uses_window_function():
    """Verify that the C pipeline source exists and uses a SQL Window Function."""
    c_path = '/home/user/pipeline.c'
    assert os.path.exists(c_path), f"{c_path} does not exist."

    with open(c_path, 'r') as f:
        content = f.read().upper()
    assert "OVER" in content, "The C program does not seem to use a SQL Window Function (missing OVER clause)."

def test_pipeline_execution_and_output():
    """Compile the C program, run it with mock input, and verify the output."""
    c_path = '/home/user/pipeline.c'
    exe_path = '/home/user/pipeline'

    # Ensure the source file exists before trying to compile
    assert os.path.exists(c_path), f"Cannot compile because {c_path} is missing."

    # Compile the C program
    compile_proc = subprocess.run(['gcc', c_path, '-o', exe_path, '-lsqlite3'], capture_output=True)
    assert compile_proc.returncode == 0, f"Failed to compile pipeline.c:\n{compile_proc.stderr.decode()}"

    # Run the compiled program with mock data
    input_data = "bkp_105\nbkp_104\nbkp_103\nbkp_102\nbkp_101\nbkp_100\n"
    run_proc = subprocess.run([exe_path], input=input_data.encode(), capture_output=True)
    assert run_proc.returncode == 0, f"Pipeline execution failed:\n{run_proc.stderr.decode()}"

    # Check the output file
    out_path = '/home/user/restore_cost.txt'
    assert os.path.exists(out_path), f"{out_path} was not created by the pipeline."

    with open(out_path, 'r') as f:
        cost = f.read().strip()

    assert cost == "5900", f"Expected restore cost to be 5900, but got '{cost}'."