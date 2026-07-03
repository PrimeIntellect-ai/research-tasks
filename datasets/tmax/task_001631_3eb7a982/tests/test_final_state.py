# test_final_state.py
import os
import json
import math

def test_final_state():
    results_file = "/home/user/results.json"
    pdb_file = "/home/user/protein.pdb"

    assert os.path.exists(results_file), f"Missing results file: {results_file}"

    with open(results_file, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not a valid JSON file.")

    assert "center" in results, "Missing 'center' in results.json"
    assert "R_max" in results, "Missing 'R_max' in results.json"
    assert "final_mesh_size" in results, "Missing 'final_mesh_size' in results.json"
    assert "root" in results, "Missing 'root' in results.json"

    # Parse PDB to get exact expected values
    assert os.path.exists(pdb_file), f"Missing PDB file: {pdb_file}"
    ca_coords = []
    with open(pdb_file, 'r') as f:
        for line in f:
            if line.startswith("ATOM") and line[12:16].strip() == "CA":
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                ca_coords.append((x, y, z))

    assert len(ca_coords) > 0, "No CA atoms found in PDB file."

    N = len(ca_coords)
    c_x = sum(c[0] for c in ca_coords) / N
    c_y = sum(c[1] for c in ca_coords) / N
    c_z = sum(c[2] for c in ca_coords) / N

    distances = [
        math.sqrt((c[0] - c_x)**2 + (c[1] - c_y)**2 + (c[2] - c_z)**2)
        for c in ca_coords
    ]
    r_max = max(distances)

    def g(r):
        return sum(math.exp(-0.5 * (r - d)**2) for d in distances)

    mesh = [0.0, r_max]
    for _ in range(4):
        new_points = []
        for j in range(len(mesh) - 1):
            r_j = mesh[j]
            r_j1 = mesh[j+1]
            if abs(g(r_j1) - g(r_j)) > 1.0:
                new_points.append((r_j + r_j1) / 2.0)
        mesh.extend(new_points)
        mesh.sort()

    expected_mesh_size = len(mesh)

    # Simple bisection to find root as a fallback/validation (brentq is standard but bisection works for validation)
    a, b = r_max / 2.0, r_max
    fa, fb = g(a) - 2.0, g(b) - 2.0

    # We will just check if the student's root evaluates to ~0
    student_root = results["root"]
    g_root = g(student_root) - 2.0

    assert isinstance(results["center"], list) and len(results["center"]) == 3, "'center' must be a list of 3 floats"
    assert round(results["center"][0], 4) == round(c_x, 4), "Incorrect X coordinate for center"
    assert round(results["center"][1], 4) == round(c_y, 4), "Incorrect Y coordinate for center"
    assert round(results["center"][2], 4) == round(c_z, 4), "Incorrect Z coordinate for center"

    assert round(results["R_max"], 4) == round(r_max, 4), "Incorrect R_max value"
    assert results["final_mesh_size"] == expected_mesh_size, f"Incorrect final_mesh_size. Expected {expected_mesh_size}, got {results['final_mesh_size']}"

    assert abs(g_root) < 1e-3, f"Root {student_root} does not solve g(r) - 2.0 = 0. g(root) - 2.0 = {g_root}"
    assert r_max / 2.0 <= student_root <= r_max, "Root is not within the specified interval [R_max/2, R_max]"