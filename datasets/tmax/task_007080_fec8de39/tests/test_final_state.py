# test_final_state.py
import os

def test_bash_script_exists_and_executable():
    script_path = "/home/user/build_and_test.sh"
    assert os.path.isfile(script_path), f"Bash script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Bash script {script_path} is not executable."

def test_rust_source_exists():
    rust_path = "/home/user/obfuscate_patch.rs"
    assert os.path.isfile(rust_path), f"Rust source code {rust_path} does not exist."

def test_executable_exists():
    exe_path = "/home/user/obfuscate_patch"
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"Compiled executable {exe_path} is not executable."

def test_artifact_content():
    input_path = "/home/user/test.patch"
    artifact_path = "/home/user/artifact.patch"

    assert os.path.isfile(input_path), f"Input file {input_path} is missing."
    assert os.path.isfile(artifact_path), f"Output artifact {artifact_path} is missing."

    with open(input_path, "r", encoding="utf-8") as f:
        input_lines = f.readlines()

    expected_lines = []
    for line in input_lines:
        stripped_newline = line.endswith("\n")
        content = line.rstrip("\n")

        if content.startswith("+") and not content.startswith("+++"):
            hex_encoded = content[1:].encode('utf-8').hex()
            expected_line = "+" + hex_encoded
        elif content.startswith("-") and not content.startswith("---"):
            hex_encoded = content[1:].encode('utf-8').hex()
            expected_line = "-" + hex_encoded
        else:
            expected_line = content

        if stripped_newline:
            expected_line += "\n"

        expected_lines.append(expected_line)

    expected_output = "".join(expected_lines)

    with open(artifact_path, "r", encoding="utf-8") as f:
        actual_output = f.read()

    assert actual_output == expected_output, "The contents of artifact.patch do not match the expected hex-encoded output."