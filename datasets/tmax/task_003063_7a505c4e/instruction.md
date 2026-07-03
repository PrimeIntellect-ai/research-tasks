You are acting as a localization engineer managing an ETL pipeline that processes translation files. We are experiencing two issues: our extraction tool is producing duplicate records on transient failures, and bad translations are crashing our downstream systems.

Your task consists of two parts:

**Part 1: Fix the Vendored Package**
We use a vendored Python package called `loctool` located at `/app/loctool-1.0.0/` for extracting translation data. 
There is a bug in `/app/loctool-1.0.0/loctool/extractor.py`. When a transient error occurs during extraction (simulated in our environment by the `SIMULATE_FLAKE=1` environment variable), the retry logic kicks in but produces duplicate records in the final output because it appends to the internal records list without clearing previous failed attempt data.
Diagnose and fix the bug in `extractor.py` so that retries do not result in duplicate records. You do not need to reinstall the package if you edit the source files directly.

**Part 2: Implement a Quality Gate (Adversarial Verifier)**
Downstream systems are failing because third-party translators often upload malformed translation files. 
Create a Python script at `/home/user/validate.py` that acts as a quality gate.
The script must have the following CLI signature:
`python3 /home/user/validate.py --source <path_to_english_json> --target <path_to_translation_json>`

The script must validate the target translation JSON against the source English JSON based on the following rules:
1. **Key Parity**: The target JSON must contain the exact same top-level keys as the source JSON. No missing keys, no extra keys.
2. **Placeholder Parity**: The target string for each key must contain the exact same Python format string placeholders (e.g., `{user_name}`, `{count}`) as the source string. The order of placeholders in the target string does not matter, but the set of placeholder names must be identical. Ignore any non-placeholder text.

If the target file passes all validation rules, the script MUST exit with status code `0`.
If the target file fails ANY validation rule, the script MUST exit with a non-zero status code (e.g., `1`).

We will test your `validate.py` script against a hidden suite of clean and evil JSON translation files. To succeed, your script must accept 100% of the clean translations and reject 100% of the evil translations.