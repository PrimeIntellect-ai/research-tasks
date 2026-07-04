You are acting as an AI assistant for a localization engineer. I need you to write a Go program to process a multilingual translation file and create an execution pipeline based on some mathematical properties of the text.

I have a CSV file at `/home/user/locales.csv` with the following columns: `id`, `lang`, `text`.

Write a Go script at `/home/user/process.go` that does the following:
1. Parses the CSV.
2. For the `text` field of each row, calculate the "digit sum". To do this, iterate over all Unicode characters in the string. If a character belongs to the Unicode category `Nd` (Number, Decimal Digit), extract its numeric value (0-9) and add it to a running total for that row. Note that this must support multi-language digits, such as full-width Japanese digits (e.g., '９') and Eastern Arabic numerals (e.g., '٥').
3. Group the rows by the `lang` column.
4. For each language, sample exactly ONE row: the one with the highest digit sum. If there is a tie for the highest digit sum, pick the one with the lowest `id` (treated as an integer).
5. Generate a Make-based execution pipeline (a DAG) by writing a `Makefile` to `/home/user/Makefile`. 
   - The Makefile must have an `all` target that depends on a target for each language present in the file (e.g., `process_en`, `process_ja`, etc.).
   - Each language's target (e.g., `process_en:`) must contain a single command that writes the winning `id` for that language into a text file named `/home/user/result_<lang>.txt`. For example: `echo "102" > /home/user/result_en.txt`.

After writing the Go program, run it to generate the `Makefile`, and then execute `make` in the terminal to produce the final result files.