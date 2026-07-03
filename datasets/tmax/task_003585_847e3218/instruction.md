You are an integration developer testing APIs for a data processing pipeline. We have a proprietary expression evaluation engine provided by a vendor as a compiled binary at `/app/vendor_eval`. We currently shell out to this binary to process mathematical expressions, but the overhead of starting a subprocess for every request is causing severe bottlenecks in our API.

Your objective is to replace the vendor binary with a fast, native Python implementation. 

Here are the specific steps:

1. **Environment Setup**: Create a virtual environment at `/home/user/venv` and install any necessary Python packages for parsing (e.g., `lark`, `pyparsing`) and testing.
2. **Diff/Patch Processing**: You will find a base file of expressions at `/home/user/data/base_expressions.txt` and a patch file at `/home/user/data/updates.patch`. Apply the patch to generate the final list of expressions to evaluate. Save the patched file as `/home/user/data/final_expressions.txt`.
3. **Reverse Engineer the Oracle**: The stripped binary `/app/vendor_eval` takes a single expression string as a command-line argument and prints the integer result. Test it to understand its syntax. It supports standard arithmetic (`+`, `-`, `*`, `/` for integer division) and two custom functions: `SUM_SQ(a, b)` which computes $a^2 + b^2$, and `MOD(a, b)` which computes $a \pmod b$. Parentheses are used for grouping.
4. **Implementation & Validation**: Write a Python script at `/home/user/fast_eval.py`. This script must:
    * Read expressions line-by-line from a given file.
    * Validate the input: Skip empty lines or lines starting with `#`.
    * Evaluate the expression exactly as `/app/vendor_eval` would.
    * Simulate rate limiting / batching: Process the lines in chunks. 
    * Output the results to a specified output file, one integer per line.
5. **CLI Interface**: `/home/user/fast_eval.py` should accept two arguments: `<input_file>` and `<output_file>`.

For the final evaluation, your Python implementation will be tested against the binary on a hidden dataset of 10,000 expressions. Because the goal is API optimization, your script must complete the processing significantly faster than shelling out to the binary.

Generate the output for `/home/user/data/final_expressions.txt` and save it to `/home/user/data/results.txt`.