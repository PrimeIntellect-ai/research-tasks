You are a data engineer tasked with building an ETL pipeline to process a large, noisy dataset of mathematical expressions extracted from scientific texts. 

The dataset is located at `/home/user/data/equations.jsonl`. It contains metadata and mathematical formulas. However, the extraction process that generated this file had a bug: it sometimes produced malformed unicode escape sequences in the JSON strings (e.g., truncated sequences like `\u221` instead of `\u2211`, or invalid hex like `\uXXYZ`). Because of this, standard JSON parsers (like Python's `json.loads`) will crash with a `JSONDecodeError` on about 5% of the lines.

Your objective is to write and execute a Python script that accomplishes the following:

1. **Robust Parsing (Extraction):**
   Read `/home/user/data/equations.jsonl`. You must handle or fix the malformed unicode escapes so you can extract the `"equation"` field from every line. Lines that are completely unrecoverable (not valid dictionaries even after basic string sanitization) should be skipped, but you must strive to recover all lines where only the unicode escape is broken (e.g., by replacing invalid `\uXXXX` sequences with a standard placeholder like `?` or simply removing the backslash, before parsing).

2. **Tokenization and Normalization:**
   For each extracted equation string, normalize it into a structural template to identify algebraically similar equations. Apply these exact rules in order:
   * Remove all whitespace characters.
   * Replace any sequence of alphabetic characters (a-z, A-Z) with the literal string `VAR`.
   * Replace any sequence of digits (0-9), optionally including a single decimal point `.`, with the literal string `NUM`.
   * Keep all other characters (operators, parentheses, math symbols, commas) exactly as they are.
   
   *Example:* 
   Original: `f(x) = a * x^2 + b * x + c`
   No-space: `f(x)=a*x^2+b*x+c`
   Normalized: `VAR(VAR)=VAR*VAR^NUM+VAR*VAR+VAR`

3. **Aggregation and Sorting:**
   Count the frequencies of each unique normalized equation template across the entire dataset. 
   Sort the aggregated templates primarily by their frequency in **descending** order. If there is a tie in frequency, sort them alphabetically by the normalized template string in **ascending** order.

4. **Output:**
   Write the top 100 most frequent normalized templates to a CSV file located exactly at `/home/user/top_templates.csv`.
   The CSV must have exactly two columns with the header `template,count`.
   Use standard comma separation.

**Constraints & Notes:**
* You have full access to a Linux terminal to write, run, and debug your Python script.
* Use Python 3 standard libraries. No external libraries (like pandas) are strictly required, but you can install them if you wish.
* Do not write the output anywhere else. The automated verification will strictly check the contents and order of `/home/user/top_templates.csv`.