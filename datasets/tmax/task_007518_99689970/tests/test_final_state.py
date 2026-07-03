# test_final_state.py

import os
import pytest

def test_compile_loc_exists():
    script_path = "/home/user/loc/compile_loc.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_fr_final_content():
    final_file_path = "/home/user/loc/fr_final.txt"
    assert os.path.isfile(final_file_path), f"The final output file {final_file_path} does not exist."

    expected_content = """ERR_001=L'équation [eq_name] manque de variable [x].
ERR_002=Le déterminant de la matrice est zéro.
ERR_003=Value [val] exceeds limit [max].
ERR_004=L'algorithme [alg] a échoué à l'étape [step_id] avec le code [err_code].
ERR_005=Convergence not reached after [n] iterations.
ERR_006=Erreur de syntaxe dans l'expression [expr]."""

    with open(final_file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content == expected_content, (
        f"The content of {final_file_path} is incorrect.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{content}"
    )