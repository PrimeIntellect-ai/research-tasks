# test_final_state.py

import os
import pytest

def test_tracker_go_exists():
    filepath = "/home/user/tracker.go"
    assert os.path.isfile(filepath), f"Expected Go program at {filepath} does not exist."

def test_active_servers_txt_exists():
    filepath = "/home/user/active_servers.txt"
    assert os.path.isfile(filepath), f"Expected output file {filepath} does not exist."

def test_active_servers_txt_contents():
    filepath = "/home/user/active_servers.txt"
    assert os.path.isfile(filepath), f"Expected output file {filepath} does not exist."

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = {
        "Système de test -> https://api.test.local/v1",
        "Déploiement avancé -> https://api.prod.local/v2"
    }

    unexpected_fragments = [
        "Vieux système",
        "https://api.old.local/v1",
        "Gros fichier",
        "https://api.big.local/v1"
    ]

    actual_lines_set = set(lines)

    for expected in expected_lines:
        assert expected in actual_lines_set, f"Missing expected output line: '{expected}'"

    for line in lines:
        for frag in unexpected_fragments:
            assert frag not in line, f"Found unexpected content from filtered files: '{line}'"

    assert len(lines) == len(expected_lines), f"Expected exactly {len(expected_lines)} lines, but found {len(lines)}."