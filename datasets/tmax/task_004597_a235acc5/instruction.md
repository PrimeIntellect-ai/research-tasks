You are a localization engineer. You have been given a JSON-lines file containing localization strings, but some of the entries are corrupted or do not follow our schema.

Your task is to write a C++ program that processes this large file, validates the entries, and generates C++ header files for each language using a specific template.

File locations:
- Input translations: `/home/user/translations.jsonl`
- JSON library: `/home/user/json.hpp` (nlohmann/json, already downloaded for you)
- Output directory for headers: `/home/user/locales/` (you must create this directory)
- Your C++ source file: `/home/user/generate_locales.cpp`

Input format (`translations.jsonl`):
Each line is a JSON object with three string fields: `key`, `lang`, and `text`.
Example:
`{"key": "btn_submit", "lang": "en", "text": "Submit"}`

Validation constraints (if any of these fail, or if the JSON is malformed, skip the line):
1. `key` must consist only of alphanumeric characters and underscores (`a-z`, `A-Z`, `0-9`, `_`).
2. `lang` must be exactly 2 lowercase English letters (`a-z`).
3. `text` must be successfully parsed by the JSON library. Specifically, some lines contain malformed unicode escapes (e.g., `\u00ZZ`) which will cause the JSON parser to throw an exception. Catch these exceptions and skip the line.

Output requirements:
For each valid `lang` discovered, generate a header file named `/home/user/locales/{lang}.h`.
The header file must use the following template structure:

```cpp
#pragma once
#include <string>

namespace i18n_{lang} {
const std::string {key1} = "{text1}";
const std::string {key2} = "{text2}";
// ...
}
```
The keys inside each namespace must be sorted alphabetically.
If a key appears multiple times for the same language, use the last valid occurrence in the file.

Write, compile, and run your C++ program to generate the header files. You can compile your code with `g++ -std=c++17 -o generate_locales generate_locales.cpp`.