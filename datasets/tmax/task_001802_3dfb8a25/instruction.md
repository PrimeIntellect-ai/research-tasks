You are a localization engineer managing a translation pipeline. You have two large translation files (without headers):
1. `/home/user/locales/base.csv` - The existing translation database.
2. `/home/user/locales/update.csv` - New and updated translations provided by linguists.

The CSV format is: `msg_id,language_code,translation_text`

Your task is to write a Bash script (or use Bash one-liners) to perform the following ETL and data manipulation pipeline:

1. **Merge and Override:** Combine `base.csv` and `update.csv`. If a `msg_id` + `language_code` combination exists in both, the text from `update.csv` must override the one in `base.csv`.
2. **Regex Filtering:** Retain only the rows where the `msg_id` matches the exact pattern of the word `ERR_` followed by exactly three digits (e.g., `ERR_100`, `ERR_404`). Drop all other `msg_id`s (like `SYS_01`).
3. **Gap-Filling:** The project officially supports three languages: `en`, `es`, and `fr`. Look at all the valid `ERR_` message IDs present in your filtered dataset. If any of those IDs are missing a translation for any of the three required languages, insert a gap-filler row for that language with the translation text `UNTRANSLATED`.
4. **Output Final Data:** Save the fully merged, filtered, and gap-filled dataset to `/home/user/locales/final.csv`. The file must be sorted alphabetically by `msg_id`, then by `language_code`.
5. **Stratified Sampling:** For QA review, generate a sample file at `/home/user/locales/review.csv`. This file must contain exactly the first 2 rows for each language (based on the alphabetical sorting of `msg_id`) from your `final.csv`. The `review.csv` should be sorted by `language_code`, then `msg_id`.

Ensure you use standard Linux utilities (like `awk`, `sort`, `grep`, `join`, etc.) as these files can be large and should be processed efficiently.