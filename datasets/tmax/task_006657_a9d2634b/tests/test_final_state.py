# test_final_state.py
import os
import json
import re

def test_rust_project_exists():
    cargo_toml = "/home/user/loc_tool/Cargo.toml"
    assert os.path.isfile(cargo_toml), "Rust project 'loc_tool' was not created in /home/user/loc_tool or missing Cargo.toml"

def test_output_json():
    output_path = "/home/user/output.json"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    with open(output_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{output_path} is not valid JSON."

    expected_data = [
        {
            "key": "error_not_found",
            "en": "Item {item_name} was not found.",
            "de": "Artikel {item_name} nicht gefunden."
        },
        {
            "key": "logout_btn",
            "en": "Log out",
            "es": "Log out",
            "fr": "Se déconnecter"
        },
        {
            "key": "welcome_msg",
            "en": "Welcome, {user}!",
            "es": "Bienvenido, {user}!",
            "fr": "Welcome, {user}!"
        }
    ]

    assert data == expected_data, "The contents of output.json do not match the expected normalized and imputed translations."

def test_makefile_exists():
    makefile_path = "/home/user/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile is missing at {makefile_path}."

    with open(makefile_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert re.search(r'^process:', content, re.MULTILINE), "Makefile does not contain a 'process' target."

def test_cronjob_exists():
    cronjob_path = "/home/user/cronjob"
    assert os.path.isfile(cronjob_path), f"Cronjob file is missing at {cronjob_path}."

    with open(cronjob_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # 15 3 * * 2 cd /home/user && make process
    pattern = r"^15\s+3\s+\*\s+\*\s+2\s+cd\s+/home/user\s*&&\s*make\s+process$"
    assert re.match(pattern, content), f"Cronjob file does not match the required schedule and command. Found: {content}"