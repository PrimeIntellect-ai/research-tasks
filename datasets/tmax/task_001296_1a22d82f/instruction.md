You are an automation specialist tasked with modernizing our data infrastructure. We currently rely on an undocumented, legacy binary located at `/app/legacy_processor` to parse real-time sensor logs. 

This binary reads messy log text from standard input (`stdin`), extracts specific sensor readings using pattern matching, applies a mathematical transformation to the values, reshapes the data from a wide format into a normalized long format, and writes the CSV results to standard output (`stdout`).

Because the binary is unmaintained and we need to run it on new architectures, your task is to reverse-engineer its exact behavior and replace it with a pure Python script.

Requirements:
1. Write a Python script at `/home/user/pipeline.py` that reads from `stdin` and writes to `stdout`.
2. Your script must be a BIT-EXACT drop-in replacement for `/app/legacy_processor`. For any given input log stream, your script must produce the exact same output.
3. The script must be capable of processing arbitrarily large streams (Large-file streaming). Do not read the entire `stdin` into memory at once.
4. You will need to interact with the binary in the terminal, feed it crafted inputs, and deduce:
   - The regex rules it uses to find the sensor ID and the variables `X` and `Y` within messy log lines.
   - The exact mathematical formulas it applies to `X` and `Y` to produce the output metrics (let's call them `Alpha` and `Beta`).
   - How it reshapes the output (the binary outputs multiple rows per input line).

You can use standard Linux CLI tools (like `echo`, `cat`, `awk`, etc.) and Python to probe the binary and verify your findings before writing the final script.

Make sure your script handles rounding and formatting exactly as the binary does.