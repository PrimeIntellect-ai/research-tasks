You are a localization engineer managing a translation memory for a math tutoring platform. You need to build a data pipeline that processes incoming translation JSON files, sanitizes them, and normalizes their features. 

However, the internal parser we use for this, `loc-math-parser` (version 0.1.0), has a bug in its current vendored release that prevents timestamp parsing from working. 

Your tasks are as follows:

1. **Fix and Install the Vendored Package:**
   You will find the source code for `loc-math-parser` at `/app/vendored/loc-math-parser-0.1.0`. There is a deliberate typo in the timestamp parsing utility (`loc_math_parser/utils.py`) that raises an attribute error when parsing times. Find it, fix it, and install the package in your environment so it can be imported as `loc_math_parser`.

2. **Create the Data Processing Pipeline:**
   Write a Python script at `/home/user/process_translations.py` that takes exactly two command-line arguments: an input directory and an output directory.
   `python /home/user/process_translations.py <input_dir> <output_dir>`

   The script must read all `.json` files in the `<input_dir>`. Each input JSON has the following structure:
   ```json
   {
       "id": "msg_123",
       "timestamp": "2023-10-25 14:30:00",
       "math_text": "Calculate the area if x = 5. Contact tutor@math.com for help."
   }
   ```

3. **Classification and Sanitization (Adversarial Filtering):**
   * **REJECT (Evil):** If the `math_text` contains *any* email address (e.g., `user@domain.com`) or *any* HTML/XML tags (e.g., `<script>`, `<b>`, `</a>`), the file is considered poisoned/sensitive. You must **reject** it. Do NOT write an output file for it.
   * **PRESERVE (Clean):** If the `math_text` is safe, you must process it and write the result to `<output_dir>/<id>.json`.

4. **Processing Clean Data:**
   For accepted files, transform the data:
   * **Timestamp Alignment:** Use the fixed `loc_math_parser.utils.parse_time(data['timestamp'])` to parse the string into a datetime object, then format it to an ISO 8601 string (e.g., `2023-10-25T14:30:00`).
   * **Tokenization:** Use `loc_math_parser.tokenizer.tokenize_math(data['math_text'])` to get a list of string tokens.
   * **Output Format:** Save the processed data as a JSON file named `<id>.json` in the output directory:
     ```json
     {
         "id": "msg_123",
         "iso_timestamp": "2023-10-25T14:30:00",
         "tokenized": ["Calculate", "the", "area", "if", "x", "=", "5."]
     }
     ```

Make sure your script gracefully handles all files in the given input directory.