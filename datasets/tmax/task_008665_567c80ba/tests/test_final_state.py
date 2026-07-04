# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/build_graph.sh"
CYPHER_PATH = "/home/user/insert.cypher"

EXPECTED_CYPHER = """MERGE (n:Asset {id: 1, name: 'Root'});
MERGE (n:Asset {id: 2, name: 'Node_A'});
MERGE (n:Asset {id: 3, name: 'Node_B'});
MERGE (n:Asset {id: 4, name: 'Node_AA'});
MERGE (n:Asset {id: 5, name: 'Node_AB'});
MERGE (n:Asset {id: 6, name: 'Node_AAA'});
MERGE (n:Asset {id: 8, name: 'Node_C'});
MERGE (c:Asset {id: 2})-[:HAS_PARENT]->(p:Asset {id: 1});
MERGE (c:Asset {id: 3})-[:HAS_PARENT]->(p:Asset {id: 1});
MERGE (c:Asset {id: 4})-[:HAS_PARENT]->(p:Asset {id: 2});
MERGE (c:Asset {id: 5})-[:HAS_PARENT]->(p:Asset {id: 2});
MERGE (c:Asset {id: 6})-[:HAS_PARENT]->(p:Asset {id: 4});
MERGE (c:Asset {id: 8})-[:HAS_PARENT]->(p:Asset {id: 1});
"""

def test_script_exists_and_executable():
    """Check if the bash script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_script_execution_and_output():
    """Run the script and verify the generated Cypher script."""
    # Remove the output file if it exists to ensure the script generates it
    if os.path.exists(CYPHER_PATH):
        os.remove(CYPHER_PATH)

    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    assert os.path.isfile(CYPHER_PATH), f"Cypher script was not generated at {CYPHER_PATH}"

    with open(CYPHER_PATH, 'r') as f:
        actual_cypher = f.read()

    # Strip trailing whitespace/newlines for robust comparison
    actual_lines = [line.strip() for line in actual_cypher.strip().split('\n') if line.strip()]
    expected_lines = [line.strip() for line in EXPECTED_CYPHER.strip().split('\n') if line.strip()]

    assert actual_lines == expected_lines, "The generated Cypher script does not match the expected output."