You are a localization engineer managing translation strings for a mathematical software suite. You have received a wide-format CSV file containing new translation strings, which include Unicode mathematical symbols. Your task is to process this data using only Bash shell built-ins, standard coreutils (like `awk`, `sed`, `grep`), and `sqlite3` to reshape the data, extract features, compute summary statistics, and load it into a SQLite database.

**Initial Setup**
An input file is located at `/home/user/locales_wide.csv` with the following header:
`msg_id,en,fr,es,zh`
Each row contains a translation key and the corresponding text for English, French, Spanish, and Chinese. The text contains Unicode characters, including mathematical symbols.

**Phase 1: Wide-to-Long Reshaping**
Convert `/home/user/locales_wide.csv` into a long-format CSV file saved at `/home/user/locales_long.csv`.
- The new header must be: `msg_id,lang,translation`
- Skip the header row from the input when generating the data rows, but ensure the new header is written first.
- `lang` should be one of `en`, `fr`, `es`, `zh`.

**Phase 2: Unicode Feature Extraction**
Read `/home/user/locales_long.csv` and create a new file `/home/user/locales_features.csv` with the header: `msg_id,lang,translation,char_len,math_sym_count`.
- `char_len`: The length of the translation string in **characters** (not bytes).
- `math_sym_count`: The total count of specific mathematical symbols in the translation. The symbols to check for are: `∑`, `√`, `≈`, `∞`, `±`.
- Ensure you process the UTF-8 strings correctly.

**Phase 3: Mathematical Summary Statistics**
Read `/home/user/locales_features.csv` and generate summary statistics per language. Save the results to `/home/user/locales_stats.csv` with the header: `lang,avg_char_len,total_math_sym`.
- `avg_char_len`: The average `char_len` for that language, mathematically rounded to exactly 2 decimal places (e.g., `5.50`, `6.33`).
- `total_math_sym`: The sum of `math_sym_count` for that language.
- The rows should be sorted alphabetically by `lang`.

**Phase 4: Database Bulk Import**
Create a new SQLite database at `/home/user/loc_metrics.db`.
Create two tables and import your data:
1. Table `translations` with columns `msg_id TEXT`, `lang TEXT`, `translation TEXT`, `char_len INTEGER`, `math_sym_count INTEGER`.
2. Table `language_stats` with columns `lang TEXT`, `avg_char_len REAL`, `total_math_sym INTEGER`.
- Import the data from `/home/user/locales_features.csv` into `translations` (ignoring the CSV header).
- Import the data from `/home/user/locales_stats.csv` into `language_stats` (ignoring the CSV header).

**Constraints**
- Do NOT use Python, Perl, Ruby, or Node.js. You must solve this using Bash, `awk`, `sed`, `grep`, `sqlite3`, etc.
- Make sure to correctly handle the multi-byte Unicode characters. Ensure your environment uses `LC_ALL=C.UTF-8` if needed.