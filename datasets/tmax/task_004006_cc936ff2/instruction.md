You are an automation specialist creating an ETL workflow for a legacy scientific database. You have been provided with a set of raw text reports from different laboratory machines, which unfortunately use different character encodings and inconsistent formatting. 

Your task is to write a Python script `/home/user/process_math.py` that processes these files, normalizes the text, extracts specific mathematical structures, evaluates them, and outputs a structured JSON report.

The raw data is located in `/home/user/raw_math_data/` and consists of three files:
1. `doc1.txt` 
2. `doc2.dat`
3. `doc3.log`

These files are encoded in a mix of `UTF-8`, `UTF-16`, and `ISO-8859-1`. Your script must dynamically handle or explicitly decode each file without throwing decoding errors.

Within each file, there is unstructured text containing:
1. A 2x2 integer matrix formatted somewhere in the text like `[[a, b], [c, d]]` (with varying whitespace).
2. A polynomial expression in the variable `x` (up to degree 2), representing a mathematical formula (e.g., `2x^2 + 3x - 1`, `x^2 - x`, `5x - 7`).

Your Python script must:
1. Read each file and correctly decode the text.
2. Tokenize and extract the 2x2 matrix.
3. Calculate the **trace** of the matrix (the sum of the main diagonal elements: `a + d`).
4. Extract the polynomial expression.
5. Parse the polynomial and evaluate it for **x = 10**. (Note: the polynomials will only contain integers, `+`, `-`, `x`, `x^2`, and spaces. Implicit coefficients, like `x^2` meaning `1 * x^2`, must be handled).
6. Save the results in a JSON file at `/home/user/extracted_math.json` with the exact following structure:
```json
{
  "doc1.txt": {
    "trace": <integer>,
    "poly_eval_10": <integer>
  },
  "doc2.dat": {
    "trace": <integer>,
    "poly_eval_10": <integer>
  },
  "doc3.log": {
    "trace": <integer>,
    "poly_eval_10": <integer>
  }
}
```

Make sure your script executes successfully and generates the correct `/home/user/extracted_math.json` file. You may use standard Python libraries (e.g., `re`, `json`, `codecs`); do not use external libraries like `numpy` or `sympy`.