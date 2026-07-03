# test_final_state.py

import os

def test_i18n_data_h_exists_and_correct():
    """Test that the generated i18n_data.h file exists and has the correct content."""
    path = "/home/user/i18n_data.h"
    assert os.path.exists(path), f"File {path} does not exist. Did you run your C++ program?"
    assert os.path.isfile(path), f"Path {path} is not a regular file."

    expected_content = """#ifndef I18N_DATA_H
#define I18N_DATA_H

#include <string>
#include <unordered_map>

struct I18nData {
    static std::unordered_map<std::string, std::unordered_map<std::string, std::string>> get_strings() {
        return {
            {"ar", {
                {"ERR_01", "خطأ"}
            }},
            {"en", {
                {"BTN_CANCEL", "Cancel"},
                {"BTN_OK", "OK"},
                {"MENU_FILE", "File Menu"}
            }},
            {"es", {
                {"BTN_CANCEL", "Cancelar"},
                {"BTN_OK", "Aceptar Definitivo"}
            }},
            {"ja", {
                {"GREETING", "こんにちは 世界 (override)"}
            }}
        };
    }
};

#endif // I18N_DATA_H"""

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Normalize line endings and strip trailing/leading whitespace from the whole string
    content_normalized = "\n".join(line.rstrip() for line in content.strip().splitlines())
    expected_normalized = "\n".join(line.rstrip() for line in expected_content.strip().splitlines())

    assert content_normalized == expected_normalized, f"The content of {path} does not match the expected output. Please check indentation, sorting, deduplication, and text cleaning."