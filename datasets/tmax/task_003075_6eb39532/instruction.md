You are a data scientist taking over a legacy machine learning pipeline. One of the data cleaning and feature engineering steps is currently performed by an undocumented, compiled executable located at `/app/legacy_cleaner`. We need to migrate this pipeline entirely to Python to allow for future modifications and easier dependency management, but we have lost the source code for this specific binary.

Your task is to reverse-engineer the logic inside `/app/legacy_cleaner` and write a Python script at `/home/user/replicated_cleaner.py` that exactly replicates its behavior.

Here is what we know about the executable:
1. It reads a single line from Standard Input (STDIN).
2. The input format is a string of text (representing a categorical/text feature), followed by a pipe character `|`, followed by three comma-separated floats (representing a numerical feature vector). 
   Example input: `hello world|1.0,2.5,-0.5`
3. It performs some form of basic text tokenization/feature extraction on the string, combines it with a linear algebraic transformation (likely a matrix multiplication and normalization) of the 3D vector, and outputs a cleaned, transformed 3D vector.
4. It prints the resulting 3D vector to Standard Output (STDOUT) as three comma-separated floats, formatted to exactly 6 decimal places (e.g., `0.577350,0.577350,-0.577350`).

Requirements:
- Investigate the `/app/legacy_cleaner` binary (you can probe it with various inputs, use tools like `strings`, `objdump`, or write a fuzzer script to observe its inputs and outputs).
- Configure your Python environment and install any necessary numerical libraries (like `numpy`) to handle the linear algebra correctly.
- Create `/home/user/replicated_cleaner.py`. This script must read a single line from STDIN in the exact same format and print the exact same output to STDOUT.
- Your script must be bit-exact equivalent to the legacy binary for any valid input. The testing suite will fuzz your Python script against the legacy binary with thousands of random inputs.