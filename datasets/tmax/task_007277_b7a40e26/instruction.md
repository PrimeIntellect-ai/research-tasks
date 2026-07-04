You are a data scientist working on cleaning a dataset of mathematical formulas extracted from international forums. The text contains inline equations that use a mix of standard ASCII characters and fullwidth Unicode characters (often used in East Asian typography).

Your task is to extract, clean, validate, and evaluate these mathematical expressions using Python. 

Here are the requirements:
1. **Input File:** You have a file at `/home/user/raw_equations.txt`.
2. **Extraction:** Find all mathematical expressions enclosed within the exact delimiters `MATH[[` and `]]`. Some lines may contain multiple expressions or none.
3. **Unicode Normalization:** Convert all fullwidth characters (e.g., `１`, `＋`, `（`) to their standard ASCII equivalents. (Hint: NFKC normalization is useful here).
4. **Cleaning:** Remove all whitespace characters from the extracted expressions.
5. **Deduplication:** Remove any duplicate expressions (after normalization and whitespace removal).
6. **Validation Gate:** An expression is considered valid ONLY if:
   - After cleaning, it contains strictly ASCII digits (`0-9`), standard operators (`+`, `-`, `*`, `/`), and parentheses (`(`, `)`). No letters or other symbols are allowed.
   - It is a syntactically valid mathematical expression that can be evaluated without throwing errors (e.g., filter out mismatched parentheses or division by zero).
7. **Evaluation:** Mathematically evaluate the valid expressions.
8. **Output:** Write the successful results to `/home/user/processed_equations.csv`. 
   - The CSV must have the header `Equation,Value`.
   - The `Equation` column should be the cleaned, normalized string.
   - The `Value` column should be the numerical result formatted to exactly two decimal places (e.g., `40.00`, `2.50`).
   - The rows must be sorted alphabetically by the `Equation` column.

Write and execute a Python script to accomplish this.