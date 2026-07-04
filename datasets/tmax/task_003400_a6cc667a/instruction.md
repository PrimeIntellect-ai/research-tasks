You are a localization engineer tasked with modernizing our translation pipeline. We are migrating away from an old, proprietary C-based localization scoring engine and need to reimplement its exact behavior in Python.

The legacy binary is located at `/app/legacy_loc_scorer`. It is a stripped binary. 

Your objective is to write a Python script at `/home/user/new_loc_scorer.py` that perfectly mimics the behavior of the legacy binary.

**Data Flow & Reshaping:**
- The binary reads data from standard input (streaming).
- The input is in a "wide" CSV format without a header. Each row has exactly 6 columns: `translation_key, english_source, french_text, spanish_text, german_text, japanese_text`.
- For each input row, the tool reshapes the data into a "long" format, emitting exactly 4 lines of output (one for each non-English target language) to standard output.
- The output lines act as a generated template containing the language code, the key, the localized string, and a custom "Distance Score" calculated between the English source and the target language string.

**Your Tasks:**
1. **Analyze the Legacy Binary:** Treat `/app/legacy_loc_scorer` as a black box (or reverse-engineer it using standard tools like `objdump`, `strings`, etc.). Feed it various inputs to deduce the mathematical formula it uses to compute the "Distance Score". 
   *Hint: The score relies on a combination of string length differences and differences in Unicode code point values between the English and target text.*
2. **Implement the Logic:** Write `/home/user/new_loc_scorer.py` to read the same wide-format CSV from `sys.stdin`, compute the exact same similarity scores, reshape the rows, and print the resulting long-format templates to `sys.stdout`.
3. **Streaming & Unicode:** Your script must process the data iteratively (line-by-line) to support extremely large files without exhausting memory, and it must correctly handle multi-language Unicode characters.

**Verification:**
An automated test suite will fuzz your script by passing thousands of randomly generated Unicode CSV lines into both the legacy binary and your Python script, comparing the standard output byte-for-byte. Your output must perfectly match the binary's output.

When you are confident your script is correct, simply leave it at `/home/user/new_loc_scorer.py`.