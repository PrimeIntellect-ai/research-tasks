# test_final_state.py

import os
import re

def test_script_exists_and_executable():
    script_path = "/home/user/scripts/process_locales.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_master_prop_content():
    prop_path = "/home/user/locales/processed/master.prop"
    assert os.path.isfile(prop_path), f"Output file {prop_path} does not exist."

    with open(prop_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = {
        'farewell_fr="Au revoir"',
        'error_404_fr="Non trouvé"',
        'midnight_fr="Minuit"',
        'greeting_es="Hola"',
        'button_save_es="Guardar"',
        'new_year_es="Feliz Año"'
    }

    unexpected_lines = {
        'greeting_fr="Bonjour"',
        'old_key_es="Viejo"'
    }

    actual_lines_set = set(lines)

    for expected in expected_lines:
        assert expected in actual_lines_set, f"Expected line '{expected}' missing from {prop_path}."

    for unexpected in unexpected_lines:
        assert unexpected not in actual_lines_set, f"Unexpected line '{unexpected}' found in {prop_path}."

    assert len(lines) == 6, f"Expected exactly 6 valid entries in {prop_path}, but found {len(lines)}."

def test_crontab_dump():
    dump_path = "/home/user/crontab_dump.txt"
    assert os.path.isfile(dump_path), f"Crontab dump file {dump_path} does not exist."

    with open(dump_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match exactly "30 2 * * * /home/user/scripts/process_locales.sh" with some flexibility for spacing
    pattern = r"^30\s+2\s+\*\s+\*\s+\*\s+(?:.*)?/home/user/scripts/process_locales\.sh$"

    match = False
    for line in content.splitlines():
        if re.match(pattern, line.strip()):
            match = True
            break

    assert match, "Crontab dump does not contain the correct cron job scheduling (30 2 * * * /home/user/scripts/process_locales.sh)."