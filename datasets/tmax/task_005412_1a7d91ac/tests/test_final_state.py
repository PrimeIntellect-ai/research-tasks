# test_final_state.py

import os
import re

def test_rayon_in_cargo_toml():
    """Verify that rayon was added to Cargo.toml."""
    cargo_path = "/home/user/protein_network/Cargo.toml"
    assert os.path.isfile(cargo_path), "Cargo.toml is missing."
    with open(cargo_path, 'r') as f:
        content = f.read()
    assert "rayon" in content, "The 'rayon' crate is missing from Cargo.toml dependencies."

def test_rayon_in_main_rs():
    """Verify that rayon is used in main.rs for parallelization."""
    main_path = "/home/user/protein_network/src/main.rs"
    assert os.path.isfile(main_path), "main.rs is missing."
    with open(main_path, 'r') as f:
        content = f.read()
    assert "par_iter" in content or "par_iter_mut" in content or "rayon" in content, \
        "Could not find evidence of rayon parallel iterators (e.g., par_iter) in main.rs."

def test_pagerank_logic_in_main_rs():
    """Verify that the damping factor logic is present in main.rs."""
    main_path = "/home/user/protein_network/src/main.rs"
    with open(main_path, 'r') as f:
        content = f.read()

    assert "0.85" in content, "The damping factor 0.85 is missing from main.rs."
    assert "0.15" in content, "The teleportation factor 0.15 is missing from main.rs."

def test_output_file_exists_and_correct():
    """Verify that the output file exists and contains the correct top residues."""
    output_path = "/home/user/top_residues.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} was not created."

    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = ["B:1", "B:2", "B:3"]
    assert len(lines) >= 3, f"Expected at least 3 lines in the output, found {len(lines)}."

    assert lines[:3] == expected, f"The top 3 residues are incorrect. Expected {expected}, got {lines[:3]}."