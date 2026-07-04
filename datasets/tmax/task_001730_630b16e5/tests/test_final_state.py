# test_final_state.py
import os

def test_script_exists():
    script_path = "/home/user/parse_docs.py"
    assert os.path.exists(script_path), f"Script not found at {script_path}"
    assert os.path.isfile(script_path), f"{script_path} is not a file"

def test_compiled_docs_exists():
    output_path = "/home/user/compiled_docs.md"
    assert os.path.exists(output_path), f"Output file not found at {output_path}"
    assert os.path.isfile(output_path), f"{output_path} is not a file"

def test_compiled_docs_content():
    output_path = "/home/user/compiled_docs.md"

    expected_content = (
        "### FILE: alpha.md\n"
        "# Alpha\n"
        "This is the alpha doc.\n\n"
        "### FILE: beta.md\n"
        "# Beta\n"
        "Beta documentation.\n\n"
        "### FILE: delta.md\n"
        "# Delta\n"
        "Delta notes.\n\n"
        "### FILE: gamma.md\n"
        "# Gamma\n"
        "Gamma notes.\n\n"
    )

    with open(output_path, "r", encoding="utf-8") as f:
        actual_content = f.read()

    assert actual_content == expected_content, (
        "The contents of compiled_docs.md do not match the expected output. "
        "Ensure all .md files are extracted, sorted by basename, and formatted correctly."
    )