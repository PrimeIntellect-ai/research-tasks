You are acting as a localization engineer. Our previous translation processing pipeline was a brittle script that silently dropped translation entries if they contained embedded newlines, and it failed to handle text encoding inconsistencies properly. 

We need you to build a robust, streaming data processing tool in **Go** to clean and deduplicate our raw localization files.

Here are your instructions:
1. Create a Go module in `/home/user/loc_pipeline`.
2. Write a Go program named `process.go` in that directory.
3. The program must read a CSV file from `/home/user/input/raw_translations.csv`.
4. The CSV has four columns: `EntryID`, `Context`, `SourceText`, and `Translation`.
5. Implement the following processing rules:
    * **Streaming:** Read and write the CSV record-by-record using `encoding/csv` to support large files. Do not load the entire file into memory at once.
    * **Newline Normalization:** Embedded newlines are allowed. However, any Windows-style carriage return + newline (`\r\n`) *inside* a parsed field must be converted to a standard Unix newline (`\n`).
    * **Encoding & Normalization:** Ensure all text is valid UTF-8. Replace any invalid UTF-8 byte sequences with the standard Unicode Replacement Character (`U+FFFD`). Then, normalize all text in all fields to Unicode Normalization Form C (NFC).
    * **Deduplication:** Deduplicate rows based on the combination of the cleaned `Context` and `SourceText` fields. To do this efficiently, compute the SHA-256 hash of the string formed by `<Context>|<SourceText>`. Keep only the **first** row encountered for each hash. Drop subsequent duplicates.
6. Write the cleaned, deduplicated records to `/home/user/output/clean_translations.csv` using standard CSV quoting (RFC 4180).
7. Create a shell script at `/home/user/run.sh` that builds the Go program, downloads any necessary dependencies, and executes the binary to produce the output file.

Your solution must rely on Go's `encoding/csv` and standard cryptography/text libraries (e.g., `golang.org/x/text/unicode/norm` is permitted and recommended). Do not use external CSV parsing libraries.