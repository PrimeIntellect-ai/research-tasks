You are a localization engineer managing text updates for a UI system with strict space constraints. You have received three translation files in different character encodings, located in `/home/user/translations/`:

1. `en.csv` - English source strings (UTF-8 encoding)
2. `fr.csv` - French translated strings (ISO-8859-1 encoding)
3. `jp.csv` - Japanese translated strings (UTF-16LE encoding)

All files use the simple CSV format: `KEY,TEXT` (no header, no quoted fields, no commas inside text).

Your task is to identify any localized strings that have mathematically expanded too much compared to the English source text, which might break the UI layout.

Requirements:
1. Convert all files to UTF-8.
2. Calculate the character count (not byte count) of the `TEXT` field for each key.
3. Find all translations where the character count of the localized text is strictly greater than 2 times (`> 2 *`) the character count of the corresponding English text.
4. Output these violations to a file named `/home/user/overflow_report.csv`.
5. The output must be in the format `lang,KEY` (where `lang` is either `fr` or `jp`).
6. The final output must be sorted alphabetically (standard Linux `sort`).

Use only bash built-ins, coreutils, and standard command-line tools (e.g., `iconv`, `awk`, `sort`). Ensure your environment uses `LC_ALL=C.UTF-8` so character counts are evaluated correctly.