# test_final_state.py

import os
import json
import pytest

def test_legacy_builder_fixed():
    makefile_path = "/home/user/legacy_builder/Makefile"
    assert os.path.isfile(makefile_path), f"{makefile_path} is missing"
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "\t" in content, "Makefile should be fixed to use tabs instead of spaces"

    pack_c_path = "/home/user/legacy_builder/pack.c"
    assert os.path.isfile(pack_c_path), f"{pack_c_path} is missing"
    with open(pack_c_path, "r") as f:
        content = f.read()
    assert "<stdio.h>" in content, "pack.c should include <stdio.h>"

    builder_path = "/home/user/legacy_builder/builder"
    assert os.path.isfile(builder_path), f"{builder_path} executable is missing. Did you run make?"
    assert os.access(builder_path, os.X_OK), f"{builder_path} should be executable"

def test_legacy_output():
    output_path = "/home/user/legacy_output.txt"
    assert os.path.isfile(output_path), f"{output_path} is missing"
    with open(output_path, "r") as f:
        content = f.read().strip()
    assert content == "Packaging release...", f"Unexpected content in {output_path}: {content}"

def test_rust_project_exists():
    cargo_toml = "/home/user/release_eval/Cargo.toml"
    assert os.path.isfile(cargo_toml), f"{cargo_toml} is missing. Did you create the Rust project?"

    main_rs = "/home/user/release_eval/src/main.rs"
    assert os.path.isfile(main_rs), f"{main_rs} is missing"

    with open(main_rs, "r") as f:
        content = f.read()
    assert "#[test]" in content, "src/main.rs must contain at least one unit test using #[test]"

def test_input_files():
    env_path = "/home/user/release.env"
    assert os.path.isfile(env_path), f"{env_path} is missing"

    conditions_path = "/home/user/conditions.txt"
    assert os.path.isfile(conditions_path), f"{conditions_path} is missing"

def test_eval_results():
    results_path = "/home/user/eval_results.json"
    assert os.path.isfile(results_path), f"{results_path} is missing. Did you run the Rust application?"

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} does not contain valid JSON")

    expected = {
        "OS == linux": True,
        "STAGE == prod": False,
        "ARCH == x86_64 AND STAGE == beta": True
    }

    assert data == expected, f"Evaluation results in {results_path} do not match the expected output"