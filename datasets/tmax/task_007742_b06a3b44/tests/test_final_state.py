# test_final_state.py

import os
import json
import re
import subprocess
import pytest

def test_script_exists():
    assert os.path.isfile("/home/user/update_translations.py"), "The script /home/user/update_translations.py does not exist."

def test_locales_directory_exists():
    assert os.path.isdir("/home/user/locales"), "The directory /home/user/locales does not exist."

def test_json_files_exist_and_correct():
    expected_data = {
        "es": {
            "apple": "Manzana",
            "farewell": "Adiós",
            "greeting": "Hola",
            "zebra": "Cebra"
        },
        "zh": {
            "apple": "苹果",
            "farewell": "再见",
            "greeting": "你好",
            "zebra": "斑马"
        },
        "ar": {
            "apple": "تفاحة",
            "farewell": "وداعا",
            "greeting": "مرحبًا",
            "zebra": "حمار وحشي"
        }
    }

    for lang, expected_dict in expected_data.items():
        file_path = f"/home/user/locales/{lang}.json"
        assert os.path.isfile(file_path), f"The file {file_path} does not exist."

        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pytest.fail(f"The file {file_path} does not contain valid JSON.")

        assert data == expected_dict, f"The content of {file_path} is incorrect."

        # Check if keys are sorted alphabetically
        keys = list(data.keys())
        assert keys == sorted(keys), f"The keys in {file_path} are not sorted alphabetically."

def test_crontab_schedule():
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        crontab_output = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Ensure the crontab is set up for the current user.")

    # Regex to match: 15 3 * * * followed by any characters and the script path
    pattern = re.compile(r"^15\s+3\s+\*\s+\*\s+\*.*?/home/user/update_translations\.py(\s|$)", re.MULTILINE)
    assert pattern.search(crontab_output), "The crontab does not contain the correct schedule (15 3 * * *) or does not point to the absolute path of the script."