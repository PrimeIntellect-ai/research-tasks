# test_final_state.py

import os
import pytest

def test_parser_c_exists():
    assert os.path.isfile("/home/user/parser.c"), "The C source file /home/user/parser.c is missing."

def test_output_tsv_exists_and_content():
    output_file = "/home/user/output.tsv"
    assert os.path.isfile(output_file), f"The output file {output_file} is missing."

    expected_lines = [
        "1\tElectronics\tGreat TV but costs 500€. Highly recommended.",
        "2\tBooks\tCopyright © 2023. Good read.",
        "3\tHome\tThe temperature is 20°C.",
        "4\tMisc\tLeading and trailing",
        "5\tEdgeCases\tLook at this: ✨ magic! A"
    ]
    expected_content = "\n".join(expected_lines) + "\n"

    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Sometimes students might not output a trailing newline, so we can be slightly forgiving or strict.
    # The bash verification script uses diff -u with EOF, which includes a trailing newline.
    assert content.strip() == expected_content.strip(), f"The contents of {output_file} do not match the expected TSV format or unescaped values."