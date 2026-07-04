# test_final_state.py
import os
import json
import subprocess

def test_files_exist():
    """Check that all required files have been created."""
    assert os.path.exists("/home/user/router_solver.cpp"), "/home/user/router_solver.cpp is missing"
    assert os.path.exists("/home/user/router_solver"), "/home/user/router_solver is missing"
    assert os.path.exists("/home/user/test.sh"), "/home/user/test.sh is missing"
    assert os.path.exists("/home/user/output.json"), "/home/user/output.json is missing"

def test_executables():
    """Check that the compiled binary and the shell script are executable."""
    assert os.access("/home/user/router_solver", os.X_OK), "/home/user/router_solver is not executable"
    assert os.access("/home/user/test.sh", os.X_OK), "/home/user/test.sh is not executable"

def test_output_json_content():
    """Check that output.json contains the correct solution."""
    with open("/home/user/output.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "/home/user/output.json does not contain valid JSON"

    assert "x" in data and "y" in data, "output.json must contain 'x' and 'y' keys"
    assert data["x"] == 3, f"Expected x to be 3, got {data['x']}"
    assert data["y"] == 4, f"Expected y to be 4, got {data['y']}"

def test_router_solver_logic_bad_route():
    """Test the router_solver executable with an invalid route."""
    cmd = ["/home/user/router_solver", "/bad/route?eq=x+y&res=5&range=1,10"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 1, "Expected exit code 1 for invalid route"
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, "Output for invalid route is not valid JSON"
    assert data.get("error") == "not found", "Expected error: 'not found' for invalid route"

def test_router_solver_logic_no_solution():
    """Test the router_solver executable with an equation that has no solution."""
    cmd = ["/home/user/router_solver", "/route/calc?eq=x+y&res=100&range=1,10"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, "Expected exit code 0 for valid route but no solution"
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, "Output for no solution is not valid JSON"
    assert data.get("error") == "no solution", "Expected error: 'no solution' when no solution exists"

def test_router_solver_logic_valid_solution():
    """Test the router_solver executable with another valid equation."""
    cmd = ["/home/user/router_solver", "/route/calc?eq=x*y+y&res=27&range=1,10"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, "Expected exit code 0 for valid route"
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, "Output for valid solution is not valid JSON"

    # x*y+y = 27, min<=x<=y<=max.
    # For range 1..10:
    # x=2, y=9 -> 2*9+9 = 27
    assert data.get("x") == 2, f"Expected x=2, got {data.get('x')}"
    assert data.get("y") == 9, f"Expected y=9, got {data.get('y')}"