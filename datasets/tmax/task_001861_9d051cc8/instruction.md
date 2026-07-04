You are an AI assistant helping a research scientist organize and sanitize a disorganized collection of sensor datasets.

The researcher has instrument logs scattered across `/app/raw_data/`. Some of these archives are valid dataset bundles, while others are corrupted backups. The valid dataset bundles are `.tar.gz` files that have been marked as executable (i.e., they have the `+x` permission bit set).

Your task has several stages:

**1. Metadata Search and Extraction**
Find all `.tar.gz` files inside `/app/raw_data/` (and its subdirectories) that have the executable permission bit set.
Extract the contents of these specific archives into `/home/user/extracted/`. You will find several binary `.dat` files inside.

**2. Decoding the Binary Files**
The instrument manufacturer provided a proprietary, stripped binary decoder located at `/app/decoder.bin`.
You must use this binary to decode the `.dat` files. 
Usage: `/app/decoder.bin <path_to_dat_file>` 
It outputs decoded multi-line log records to standard output (`stdout`).

**3. Developing the C Sanitizer**
Unfortunately, the instrument frequently suffered from memory corruption, and the decoded output contains both valid and "evil" (corrupted/malformed) records. You must write a C program, saved as `/home/user/sanitizer.c` and compiled to `/home/user/sanitizer`, that reads these multi-line logs from `stdin` and writes ONLY strictly valid records to `stdout`.

A valid record consists of exactly 5 lines in the following precise order:
Line 1: `[RECORD]`
Line 2: `SEQ:<unsigned integer>` (must be a valid positive integer)
Line 3: `OBS:<string>` (The string must be between 1 and 64 characters long, containing ONLY alphanumeric characters and spaces. No punctuation, no special characters, no newlines.)
Line 4: `VAL:<float>` (must be a valid floating-point number)
Line 5: `[/RECORD]`

Any record that deviates from this format (missing lines, wrong order, invalid sequence numbers, invalid floats, strings containing unauthorized characters like shell metacharacters or punctuation, or strings exceeding 64 characters) MUST be completely discarded. Only output perfectly valid 5-line records exactly as they came in.

**4. Final Integration**
For every `.dat` file extracted in step 1, decode it using `/app/decoder.bin`, pipe the output through your `/home/user/sanitizer`, and append the sanitized output to a single file at `/home/user/master_clean.log`.

**Automated Verification:**
Your `/home/user/sanitizer` executable will be tested against a hidden adversarial corpus. It must perfectly preserve 100% of the valid records in the clean corpus, and completely drop 100% of the malformed/evil records in the evil corpus.