You are acting as a localization engineer working on a translation platform for a mathematical learning application. You have received a large translation dump containing localized strings, but the embedded mathematical formulas are inconsistently formatted, which is breaking the UI rendering engine. 

Your task is to write a Rust application that processes these translations, normalizes the mathematical formulas, and computes summary statistics for project managers.

You must build a Rust project named `loc_processor` in `/home/user/`.

**Input:**
A JSON Lines file located at `/home/user/raw_translations.jsonl` (which will be created before you start). Each line is a JSON object with the following structure:
`{"id": "msg_01", "locale": "fr_FR", "content": "La somme est $ a + b = c $."}`

**Processing Requirements:**
1. **Large-File Streaming:** The input file could theoretically be larger than memory, so your Rust program must stream the file line-by-line rather than loading it all into memory at once.
2. **Regex & Normalization:** Use regular expressions to find all mathematical formulas embedded in the `content`. Formulas are always enclosed in single dollar signs (e.g., `$ ... $`). You must normalize these formulas by removing **all** whitespace characters inside the `$...$` blocks.
3. **Tokenization & Complexity:** For each mathematical formula, calculate a "complexity score" by counting the total number of mathematical operators: `+`, `-`, `*`, `/`, and `=`. The complexity of a message is the sum of the operators across all math blocks in that message.
4. **Text Length:** Calculate the "text length" of each message. This is the character length of the `content` string *after* completely removing the `$...$` blocks. (Do not count the math formulas or their bounding dollar signs in the text length. Strip leading and trailing whitespace from the remaining string before calculating its length).
5. **Summary Statistics:** Aggregate data per `locale` to compute:
    - `message_count`: Total number of messages processed for this locale.
    - `avg_text_length`: The average text length of messages in this locale (calculated as a standard float, but written to JSON rounded to 2 decimal places).
    - `max_math_complexity`: The highest complexity score observed in a single message for this locale.

**Output Requirements:**
Your Rust program must generate two files:
1. `/home/user/normalized_translations.jsonl`: A JSON Lines file generated using template-based generation (or JSON serialization) containing the normalized records:
   `{"id": "...", "locale": "...", "normalized_content": "..."}`
   *Example: `{"id": "msg_01", "locale": "fr_FR", "normalized_content": "La somme est $a+b=c$."}`*
2. `/home/user/locale_stats.json`: A single JSON object mapping each locale to its statistics.
   *Format example:*
   ```json
   {
     "fr_FR": {
       "message_count": 150,
       "avg_text_length": 42.50,
       "max_math_complexity": 8
     }
   }
   ```

Write, compile, and execute your Rust program to generate these files.