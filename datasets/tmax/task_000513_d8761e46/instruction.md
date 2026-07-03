You are a data scientist tasked with preparing a text dataset for a lightweight custom C-based LLM inference engine. You need to build a fast data cleaning and tokenization pipeline in C, benchmark its performance, and compute statistical confidence intervals on the throughput.

I have placed two raw dataset files in your home directory:
1. `/home/user/raw_small.txt` (used for correctness testing)
2. `/home/user/raw_large.txt` (used for benchmarking)

Your tasks are:

**Phase 1: Dataset Preparation (C Tokenizer)**
Write a C program named `/home/user/tokenizer.c` and compile it to `/home/user/tokenizer`.
The program must take exactly two command-line arguments: the input file path and the output file path (e.g., `./tokenizer input.txt output.txt`).
It must process the text with the following rules:
1. Convert all ASCII letters (A-Z) to lowercase.
2. Replace any non-alphanumeric character (anything that is not a-z, 0-9, or a space) with a single space.
3. Reduce any occurrences of multiple consecutive spaces to a single space.
4. Trim leading and trailing spaces from the entire file output.
Run your compiled tokenizer on `/home/user/raw_small.txt` and output the result to `/home/user/cleaned_small.txt`.

**Phase 2: Performance Benchmarking**
Write a shell script `/home/user/benchmark.sh` that runs your tokenizer exactly 30 times on `/home/user/raw_large.txt`, redirecting the output to `/dev/null`.
For each run, measure the wall-clock execution time in milliseconds. Save these 30 timing results (one per line) to `/home/user/times.txt`.

**Phase 3: Statistical Analysis (C Stats)**
Write another C program named `/home/user/stats.c` and compile it to `/home/user/stats`.
This program must read the 30 integer values from `/home/user/times.txt` and compute:
1. The sample mean execution time.
2. The sample standard deviation (using $N-1$).
3. The 95% Confidence Interval for the mean. Use the Z-score for 95% confidence ($Z = 1.96$) and the formula: $CI = Mean \pm 1.96 \times \frac{StdDev}{\sqrt{N}}$.

The program should output the results exactly in this format to a file named `/home/user/benchmark_stats.txt`:
`Mean: <mean> ms, 95% CI: [<lower_bound> ms, <upper_bound> ms]`
(Format all floating-point numbers to exactly 2 decimal places).

Execute all phases so that `/home/user/cleaned_small.txt` and `/home/user/benchmark_stats.txt` are created.