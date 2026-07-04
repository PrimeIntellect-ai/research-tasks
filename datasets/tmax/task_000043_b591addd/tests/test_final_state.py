# test_final_state.py

import os
import pytest

def test_libgraph_so_exists():
    assert os.path.isfile("/home/user/libgraph.so"), "/home/user/libgraph.so is missing. Did you compile the C library?"

def test_integration_test_exists():
    assert os.path.isfile("/home/user/integration_test.py"), "/home/user/integration_test.py is missing."

def test_execution_plan_correct():
    log_path = "/home/user/execution_plan.log"
    assert os.path.isfile(log_path), f"{log_path} is missing. The integration test script did not create it."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_plan = "AuthService,DataFetch,DataClean,FeatureEng,ModelTrain"
    assert content == expected_plan, f"Execution plan in {log_path} is incorrect. Expected '{expected_plan}', got '{content}'."

def test_libgraph_c_fixed():
    c_path = "/home/user/libgraph.c"
    assert os.path.isfile(c_path), f"{c_path} is missing."

    with open(c_path, "r") as f:
        content = f.read()

    # The original file had: int* result = (int*)malloc(num_nodes * sizeof(int));
    # The fix should allocate more memory, e.g., (num_nodes + 1)
    # Just checking that it's no longer exactly the buggy line, or that it successfully ran without segfault
    # The successful generation of execution_plan.log is the main proof, but we can verify it was changed.
    assert "int* result = (int*)malloc(num_nodes * sizeof(int));" not in content or "calloc(num_nodes + 1" in content or "malloc((num_nodes + 1)" in content, \
        "The memory allocation bug for 'result' in libgraph.c does not appear to be fixed."