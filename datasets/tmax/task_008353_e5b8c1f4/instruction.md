You are a localization engineer tasked with updating our translation database. The legacy system exported a large translation dump in a wide-format JSON-Lines file, but the native pipeline broke because it couldn't correctly parse and decode Unicode escape sequences (e.g., `\u3053`) present in the dump.

Your task is to write a C program that streams this file, properly decodes the Unicode escape sequences into UTF-8, reshapes the data from wide to long format, and then imports it into a SQLite database.

Here are the specific requirements:

1. **Input File**: There is a file at `/home/user/raw_translations.jsonl`. Each line is a strictly formatted JSON object:
   `{"id":"<msg_id>","en":"<english_text>","fr":"<french_text>","ja":"<japanese_text>"}`
   The `<japanese_text>` heavily uses `\uXXXX` unicode escape sequences.

2. **C Program (`/home/user/reshaper.c`)**:
   - Write a C program that reads the JSONL format from standard input (stdin) line by line (to handle arbitrarily large files).
   - You may use standard C libraries or install a JSON library like `libcjson-dev` or `libjansson-dev` via `apt-get` if you prefer.
   - The program must reshape the wide format (`id`, `en`, `fr`, `ja`) into a long format CSV with three columns: `msg_id`, `locale`, `translation`.
   - The program must output the generated CSV data to standard output (stdout).
   - The program MUST correctly convert `\uXXXX` sequences into valid UTF-8 characters.
   - Compile your program to `/home/user/reshaper`.

3. **Data Pipeline & Database**:
   - Run your compiled C program to process `/home/user/raw_translations.jsonl` and save the output to `/home/user/long_translations.csv`.
   - Create a SQLite database at `/home/user/translations.db`.
   - Create a table named `i18n` with the schema: `CREATE TABLE i18n (msg_id TEXT, locale TEXT, translation TEXT);`
   - Bulk import `/home/user/long_translations.csv` into the `i18n` table in SQLite.

4. **Verification**:
   - Run the following query and save the output to `/home/user/ja_check.txt`:
     `sqlite3 /home/user/translations.db "SELECT msg_id, translation FROM i18n WHERE locale='ja' ORDER BY msg_id;"`
     The output should be pipe-separated (SQLite's default).

Make sure your C program properly escapes or quotes CSV fields if necessary (though the sample text won't contain commas or quotes to keep it simple).