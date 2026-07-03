You are a localization engineer trying to clean up data after a faulty ETL pipeline run. The ETL job was supposed to extract updated localization strings, but a retry loop bug caused it to output duplicate records for some translations.

You need to write a C program that processes this data, cleans it, extracts a specific feature, and generates a SQL bulk import script.

You have two input files in `/home/user/`:

1. `/home/user/base_strings.csv`
Format: `string_id,default_text`
Contains the base English strings.

2. `/home/user/translations_raw.csv`
Format: `string_id,locale,translated_text,timestamp`
Contains the incoming translations. Because of the ETL bug, there may be multiple rows for the same `string_id` and `locale`. You must only keep the translation with the **highest** `timestamp` (an integer).

Write a C program at `/home/user/process.c` that performs the following:
1. **Deduplicate**: Read `translations_raw.csv` and keep only the latest translation for each `(string_id, locale)` pair.
2. **Join & Extract Feature**: Join the deduplicated translations with `base_strings.csv` on `string_id`. Calculate the "word count" of the English `default_text` (number of space-separated words. For example, "File not found" has 3 words).
3. **Transform for DB Export**: Generate a SQL bulk insert file at `/home/user/bulk_import.sql` containing standard SQL INSERT statements. Because the `translated_text` might contain single quotes (e.g., `D'accord`), you must escape them by doubling them (e.g., `D''accord`) to produce valid SQL.

The output file `/home/user/bulk_import.sql` must contain exactly one line per final translation record in this exact format:
`INSERT INTO loc_data (string_id, locale, word_count, translated_text) VALUES ('<string_id>', '<locale>', <word_count>, '<escaped_translated_text>');`

Compile and run your C program to generate `/home/user/bulk_import.sql`.
Order of the INSERT statements in the output file does not matter. Assume fields in the CSV do not contain commas within the data itself.