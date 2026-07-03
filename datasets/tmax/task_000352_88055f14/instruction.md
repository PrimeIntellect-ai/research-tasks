You are an AI assistant acting as a Senior Data Engineer. 

We are migrating a legacy ETL pipeline that processes mathematical formulas extracted from various multilingual documents. The old pipeline relies on a highly sensitive, proprietary compiled C utility located at `/app/bin/legacy_calc`. This utility calculates checksums for equations, but it is notoriously brittle—it crashes (segfaults) and brings down the entire pipeline if fed anything other than strict, balanced ASCII mathematical expressions.

Our incoming data is messy. Formulas are scattered across CSV, JSON, and XML files, and they contain a mix of Unicode full-width characters, superscript numerals, and invisible formatting characters (due to OCR anomalies). Furthermore, malicious actors have occasionally injected homoglyphs and malformed structural payloads (like deeply unbalanced parentheses) that trigger the crash.

Your task is to build a Python sanitization filter at `/home/user/etl_filter.py`. 

This script must:
1. Accept a single file path as a command-line argument. The file will be a plain text file containing one extracted formula per line.
2. Apply Unicode text processing to normalize the text (e.g., NFKC normalization to convert full-width characters like `＋` or `１` to their standard ASCII equivalents `+` and `1`).
3. Transform Unicode superscripts (e.g., `²`, `³`) into their caret-notation equivalents (e.g., `^2`, `^3`).
4. Strip out any zero-width or invisible formatting characters.
5. Use Regex to validate that the fully normalized string contains ONLY valid characters: alphanumeric characters, spaces, periods, and the operators `+`, `-`, `*`, `/`, `^`, `=`, `(`, `)`.
6. Ensure parentheses are perfectly balanced.
7. Print exactly `SAFE: <normalized_formula>` to standard output if the formula is completely safe and conforms to the rules. 
8. Print exactly `REJECT` to standard output if the formula is invalid, contains illegal characters after normalization, or has unbalanced parentheses.

You can use the stripped binary `/app/bin/legacy_calc` to test your assumptions. If you pass a valid ASCII formula to it via stdin (e.g., `echo "2+2" | /app/bin/legacy_calc`), it will exit cleanly with code 0. If you pass an invalid one, it will crash or return a non-zero exit code.

We have provided a set of sample data to help you refine your script:
- `/app/data/clean/`: Contains text files with valid, messy Unicode formulas that MUST be normalized and accepted (`SAFE`).
- `/app/data/evil/`: Contains text files with malicious payloads, unresolvable homoglyphs, and structural flaws that MUST be rejected (`REJECT`).

Write the complete `/home/user/etl_filter.py` script. The automated verification suite will run your script against unseen files from the clean and evil corpora.