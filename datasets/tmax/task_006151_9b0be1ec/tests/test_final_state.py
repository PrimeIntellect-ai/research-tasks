# test_final_state.py

import os
import pytest

def test_clean_pdb_exists_and_filtered():
    path = "/home/user/clean.pdb"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        lines = f.read().splitlines()

    # Check headers and footers are preserved
    assert any(line.startswith("HEADER") for line in lines), "clean.pdb missing HEADER line"
    assert any(line.startswith("TITLE") for line in lines), "clean.pdb missing TITLE line"
    assert any(line.startswith("END") for line in lines), "clean.pdb missing END line"

    # Check duplicate atoms are removed (based on coordinates)
    coords_seen = set()
    atom_count = 0
    for line in lines:
        if line.startswith("ATOM  ") or line.startswith("HETATM"):
            atom_count += 1
            if len(line) >= 54:
                coord = line[30:54]
                assert coord not in coords_seen, f"Duplicate coordinates found in clean.pdb: {coord}"
                coords_seen.add(coord)

    assert atom_count == 5, f"Expected 5 ATOM lines in clean.pdb, found {atom_count}"

def test_solution_txt_exists_and_correct():
    path = "/home/user/solution.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "Matrix factorization successful." in content, "solution.txt missing success message"
    assert "Domain decomposed into 8x8x8 mesh." in content, "solution.txt missing domain decomposition message"
    assert "Valid atoms processed: 5" in content, "solution.txt missing or incorrect valid atoms count"
    assert "Trace: 15.7079" in content, "solution.txt missing or incorrect trace value"