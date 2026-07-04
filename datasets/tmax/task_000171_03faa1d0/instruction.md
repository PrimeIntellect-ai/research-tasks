You are a data scientist preparing a dataset for a new language model. You need to build a lightweight ETL and tokenization pipeline in Python that processes raw text, filters it, tokenizes it, and benchmarks the processing speed.

A raw text file is located at `/home/user/raw_data.txt`. 

Write and execute a Python script that does the following:
1. **Extract & Filter**: Read `/home/user/raw_data.txt`. Keep only the lines that contain the exact case-sensitive substring `"AI"` AND have strictly more than 5 words (words are separated by whitespace).
2. **Transform (Tokenize)**: For the kept lines, convert the text to lowercase, remove all punctuation (`.`, `,`, `!`, `?`), and split the text into a list of words.
3. **Load**: Save the processed lines into `/home/user/clean_data.jsonl` where each line is a JSON object in the format: `{"tokens": ["word1", "word2", ...]}`.
4. **Benchmark**: Measure the wall-clock time taken strictly for the filtering and tokenization loop (exclude imports and I/O setup if possible, but measure the processing over all lines). Calculate the throughput as `Total Raw Lines / Elapsed Seconds`.
5. **Report**: Save the throughput metric to a file named `/home/user/benchmark.txt` exactly in the format: `Throughput: X.XX lines/sec` (where X.XX is the float value rounded to exactly 2 decimal places).

Ensure your script processes the data and generates both `/home/user/clean_data.jsonl` and `/home/user/benchmark.txt`.