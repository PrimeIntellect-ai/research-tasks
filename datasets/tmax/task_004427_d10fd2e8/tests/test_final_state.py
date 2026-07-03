# test_final_state.py

import os
import time
import subprocess
import sqlite3
import pytest

def generate_golden(db_path, golden_csv_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        SELECT n1.id, SUM(n3.value * e1.weight * e2.weight) as score
        FROM Nodes n1
        JOIN Edges e1 ON n1.id = e1.source
        JOIN Edges e2 ON e1.target = e2.source
        JOIN Nodes n3 ON e2.target = n3.id
        WHERE n1.type = 'AUTHOR' AND n3.type = 'ARTICLE'
        GROUP BY n1.id
        ORDER BY score DESC, n1.id ASC
        LIMIT 100
    ''')
    res = c.fetchall()
    with open(golden_csv_path, 'w') as f:
        for r in res:
            f.write(f"{r[0]},{r[1]:.4f}\n")
    conn.close()

def test_query_optimizer_performance_and_correctness():
    cpp_source = "/home/user/query_optimizer.cpp"
    binary_path = "/home/user/query_optimizer"
    results_csv = "/home/user/results.csv"
    generator_path = "/app/data_generator"
    work_dir = "/home/user"
    db_path = os.path.join(work_dir, "graph.db")
    golden_csv = os.path.join(work_dir, "golden.csv")

    assert os.path.exists(cpp_source), f"Source file {cpp_source} does not exist."

    # Compile the C++ program
    compile_cmd = ["g++", "-O3", cpp_source, "-lsqlite3", "-o", binary_path]
    comp_res = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert comp_res.returncode == 0, f"Compilation failed:\n{comp_res.stderr}"
    assert os.path.exists(binary_path), "Compiled binary was not created."

    # Generate fresh DB
    if os.path.exists(db_path):
        os.remove(db_path)
    gen_res = subprocess.run([generator_path], cwd=work_dir, capture_output=True)
    assert gen_res.returncode == 0, f"Data generator failed."
    assert os.path.exists(db_path), "graph.db was not created by data generator."

    # Generate golden reference
    generate_golden(db_path, golden_csv)

    # Re-generate fresh DB for the agent's run to measure index creation time
    if os.path.exists(db_path):
        os.remove(db_path)
    subprocess.run([generator_path], cwd=work_dir, capture_output=True)

    if os.path.exists(results_csv):
        os.remove(results_csv)

    # Time the execution
    start_time = time.time()
    exec_res = subprocess.run([binary_path], cwd=work_dir, capture_output=True)
    duration = time.time() - start_time

    assert exec_res.returncode == 0, f"Program execution failed with return code {exec_res.returncode}"
    assert os.path.exists(results_csv), f"Results file {results_csv} was not created."

    # Verify correctness
    with open(results_csv, 'r') as f1, open(golden_csv, 'r') as f2:
        ag_lines = [l.strip() for l in f1.readlines() if l.strip()]
        gd_lines = [l.strip() for l in f2.readlines() if l.strip()]

    assert ag_lines == gd_lines, "The output CSV does not match the golden reference."

    # Verify performance threshold
    threshold = 1.5
    assert duration <= threshold, f"Execution time {duration:.4f}s exceeded the threshold of {threshold}s."