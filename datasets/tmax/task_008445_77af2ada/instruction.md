You are tasked with building a small C++ utility for a configuration management system. The system receives configuration update files containing multi-language text. You need to build a single C++ program that processes these files through a multi-stage validation and analysis pipeline, calculating rolling statistics on the configuration changes.

Your C++ program should be written to `/home/user/config_tracker.cpp`, compiled, and executed to produce an output file at `/home/user/stats_output.csv`.

Here are the requirements for the pipeline stages:

**Stage 1: Ingestion & Validation Gate**
* The program must read all `.txt` files in the directory `/home/user/config_updates/` in alphabetical order.
* **Validation Checkpoint:** Validate the file content. If a file contains the byte `0xFF`, it is considered a corrupted update. The file must be completely rejected and skipped for any statistical calculations.

**Stage 2: Extraction & Unicode Processing**
* For valid files, parse each line. Lines follow the format `key=value`. (Assume no `=` exists inside the key).
* For every parsed line, calculate the string length of the `value` in **Unicode characters** (not bytes!). Assume all valid files are encoded in UTF-8. 
* Ignore empty lines or lines without an `=` sign.

**Stage 3: Rolling Statistics Computation**
* Compute a rolling average of the `value` character lengths over a sliding window of the **last 3 valid update files**.
* The rolling average is defined as: `(Sum of all valid value character lengths in the current and up to 2 previous valid files) / (Total number of valid keys in those same files)`.

**Output Formatting (Stage 4)**
Write the results to `/home/user/stats_output.csv`.
For each file processed (in alphabetical order), append a line to the CSV:
`filename,status,valid_keys_count,rolling_avg_char_length`

* `filename`: The name of the file (e.g., `update_01.txt`).
* `status`: `VALID` or `INVALID`.
* `valid_keys_count`: The number of `key=value` pairs found in the file (0 if INVALID).
* `rolling_avg_char_length`: The rolling average calculated at Stage 3, formatted to exactly 2 decimal places (e.g., `7.50`). If the status is INVALID, or if there are no keys in the window, output `0.00`.

*Hint: In UTF-8, you can count the number of characters by counting bytes that do not match the bit pattern `10xxxxxx` (i.e., bytes where `(byte & 0xC0) != 0x80`).*

Write the C++ code, compile it (e.g., using `g++`), and run it to produce the final CSV.