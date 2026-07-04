# test_final_state.py
import os
import subprocess
import tempfile

def test_cargo_patch_exists_and_applies_correctly():
    patch_path = "/home/user/cargo.patch"
    assert os.path.isfile(patch_path), f"Patch file not found: {patch_path}"

    original_cargo_toml = """[package]
name = "legacy_rust_app"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = "1.0.0"
tokio = "1.8.0"
reqwest = "0.11.0"
"""

    expected_cargo_toml = """[package]
name = "legacy_rust_app"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = "1.1.0"
tokio = "1.14.2"
reqwest = "0.11.0"
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_cargo_path = os.path.join(temp_dir, "Cargo.toml")
        with open(temp_cargo_path, "w") as f:
            f.write(original_cargo_toml)

        # Apply the patch
        # The patch headers are expected to be --- Cargo.toml and +++ Cargo.toml
        # Running patch in the temp_dir so it finds Cargo.toml
        try:
            result = subprocess.run(
                ["patch", "Cargo.toml", patch_path],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            assert False, f"Failed to apply patch to Cargo.toml. Error: {e.stderr}\nOutput: {e.stdout}"

        with open(temp_cargo_path, "r") as f:
            patched_content = f.read()

        assert patched_content == expected_cargo_toml, (
            "The patched Cargo.toml does not match the expected content.\n"
            f"Expected:\n{expected_cargo_toml}\n"
            f"Got:\n{patched_content}"
        )

def test_fix_deps_script_exists():
    script_path = "/home/user/fix_deps.py"
    assert os.path.isfile(script_path), f"Python script not found: {script_path}"