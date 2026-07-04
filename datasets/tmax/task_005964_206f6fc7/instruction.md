You are a localization engineer tasked with updating the translation strings for a C++ application. 

You have received a messy raw export of translations in a CSV file at `/home/user/raw_translations.csv`. The file contains keys, language codes, and the translated text. However, it has several issues:
1. It contains duplicates (the same key and language appear multiple times).
2. The translated texts have inconsistent spacing (leading/trailing spaces, and multiple consecutive spaces between words).
3. It contains multi-byte UTF-8 characters (e.g., Japanese, Arabic).

Your task is to write a C++ program (e.g., `/home/user/generate_i18n.cpp`) that reads this CSV, cleans the data, and generates a C++ header file `/home/user/i18n_data.h` containing the cleaned strings.

Here are the exact requirements for your C++ data processing:
1. **Input Format:** The CSV uses commas as separators. The first line is the header: `KEY,LANG,TEXT`.
2. **Cleaning:** For the `TEXT` field, trim all leading and trailing ASCII spaces (` `). Collapse any multiple consecutive ASCII spaces *inside* the text into a single space. (Do not modify non-space whitespace like tabs or newlines, though none exist in the file, and ensure your space-collapsing doesn't corrupt UTF-8 bytes).
3. **Deduplication:** If a `KEY` and `LANG` pair appears multiple times, keep ONLY the **last** occurrence in the file.
4. **Sorting:** In the generated output, the languages must be sorted alphabetically. Within each language block, the keys must be sorted alphabetically.
5. **Output Format:** Generate a file exactly matching the structure below. Pay strict attention to indentation (4 spaces per level) and syntax.

Template for `/home/user/i18n_data.h`:
```cpp
#ifndef I18N_DATA_H
#define I18N_DATA_H

#include <string>
#include <unordered_map>

struct I18nData {
    static std::unordered_map<std::string, std::unordered_map<std::string, std::string>> get_strings() {
        return {
            {"lang1", {
                {"KEY_A", "Cleaned Text A"},
                {"KEY_B", "Cleaned Text B"}
            }},
            {"lang2", {
                {"KEY_A", "Cleaned Text C"}
            }}
        };
    }
};

#endif // I18N_DATA_H
```
*Note: Ensure trailing commas are handled correctly (no trailing comma on the last element of a map initialization).*

Compile your C++ program using `g++ -std=c++17` and run it to produce the final `/home/user/i18n_data.h` file.