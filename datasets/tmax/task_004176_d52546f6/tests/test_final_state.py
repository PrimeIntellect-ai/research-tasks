# test_final_state.py
import os
import hashlib

def test_extracted_valid_files():
    intro_path = "/home/user/docs_safe/intro.md"
    api_path = "/home/user/docs_safe/api/reference.txt"

    assert os.path.isfile(intro_path), f"{intro_path} was not extracted."
    with open(intro_path, "r") as f:
        assert f.read() == "Introduction\n", f"Content of {intro_path} is incorrect."

    assert os.path.isfile(api_path), f"{api_path} was not extracted."
    with open(api_path, "r") as f:
        assert f.read() == "API Reference\n", f"Content of {api_path} is incorrect."

def test_ignored_files():
    logo_path = "/home/user/docs_safe/images/logo.png"
    assert not os.path.exists(logo_path), f"{logo_path} should not have been extracted (not .md or .txt)."

def test_zip_slip_prevention():
    escaped_path = "/home/user/escaped.txt"
    passwd_override = "/etc/passwd.override.md"

    assert not os.path.exists(escaped_path), f"{escaped_path} exists! Zip Slip vulnerability triggered."
    assert not os.path.exists(passwd_override), f"{passwd_override} exists! Zip Slip vulnerability triggered."

def test_manifest():
    manifest_path = "/home/user/docs_safe/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} does not exist."

    with open(manifest_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Recompute hashes to match the expected format
    def get_sha256(text):
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    intro_hash = get_sha256("Introduction\n")
    api_hash = get_sha256("API Reference\n")

    expected_lines = [
        f"{api_hash}  api/reference.txt",
        f"{intro_hash}  intro.md"
    ]

    assert lines == expected_lines, f"Manifest contents are incorrect or not properly sorted. Expected:\n{expected_lines}\nGot:\n{lines}"