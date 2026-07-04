You are a localization engineer managing translation strings for a web application. You need to process a new batch of translations from freelance linguists, deduplicate conflicts, update the main database, generate a localized HTML template, and compute some translation text metrics.

You are restricted to using **Bash** and standard Linux utilities (e.g., `awk`, `sed`, `sqlite3`, `sort`, `grep`, `coreutils`). Python, Perl, and Ruby are strictly prohibited.

**Environment:**
- Database: `/home/user/locales.db` (SQLite3). Contains a table `translations(locale TEXT, string_key TEXT, translation TEXT, PRIMARY KEY(locale, string_key))`.
- Incoming Translations Directory: `/home/user/incoming/`. Contains TSV files named `[locale].tsv` (e.g., `es.tsv`, `jp.tsv`). Columns are `string_key \t translation`.
- HTML Template: `/home/user/template.html`. Contains placeholders in the format `__KEY__`.

**Requirements:**

**Phase 1: Deduplication & Database Bulk Import**
1. Read all TSV files in `/home/user/incoming/`. The `locale` is determined by the filename without the `.tsv` extension.
2. Deduplicate conflicts: Translators occasionally submitted multiple translations for the same `string_key` in the same locale. For any duplicate `string_key` within a locale, keep the translation with the **highest number of characters** (not bytes). 
3. Bulk update the `/home/user/locales.db` database. Insert new translations and overwrite existing ones in the `translations` table if the `(locale, string_key)` already exists. Use efficient bulk import methods available in `sqlite3`.

**Phase 2: Template-based Text Generation**
1. Generate a localized Japanese HTML file.
2. Read `/home/user/template.html` and replace all placeholders (e.g., `__TITLE__`) with their corresponding Japanese (`jp`) translations from the updated database.
3. Save the result to `/home/user/index_jp.html`.
4. *Note: If a key is missing in the `jp` translations, leave the placeholder exactly as is.*

**Phase 3: Rolling Statistics Computation**
1. Calculate a rolling average of translation string lengths for the Spanish (`es`) locale to help UX designers spot text expansion.
2. Extract all Spanish (`es`) translations from the *updated* database.
3. Sort them alphabetically by `string_key` in ascending order.
4. Compute a moving average of the string length (number of characters) with a window size of `3`.
   - For the first item, the average is just its length.
   - For the second item, the average is the mean of the first two items' lengths.
   - For the third item and onwards, the average is the mean of the current item and the previous two items' lengths.
5. Round the average to exactly one decimal place (e.g., `16.5`, `13.0`).
6. Save the output to `/home/user/es_rolling.txt` in the format: `string_key:rolling_average` (one per line).

Ensure all text processing handles UTF-8 characters correctly.