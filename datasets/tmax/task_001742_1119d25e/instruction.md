You are a QA engineer tasked with setting up a performance and data-validation test environment for a new expression-evaluation engine.

We need to process a batch of mathematical expressions, evaluate them, and identify which expressions evaluate to a prime number. Because the real pipeline will process millions of rows, your prototype must utilize a concurrent Producer-Consumer pattern in Python (analogous to Go's goroutines and channels) and profile the system's memory consumption.

Your task is to write a Python script at `/home/user/benchmark_processor.py` that does the following:

1. **Read Data**: Read a list of arithmetic expressions from `/home/user/test_data.txt`. Each line contains one expression (e.g., `15 + 2 * 3`). All operations will result in positive integers.
2. **Concurrent Evaluation**: 
   - Use Python's `multiprocessing` module (specifically `multiprocessing.Queue` and `Process`) to implement a worker pool pattern.
   - You must have 1 producer that reads the file and puts expressions into a "jobs" queue.
   - You must have exactly 4 consumer workers that read from the jobs queue, parse and evaluate the mathematical expression (following standard order of operations), and determine if the resulting integer is a prime number.
   - Put the results into a "results" queue.
3. **Memory Profiling**: Use Python's built-in `tracemalloc` library in the main process to track the peak memory usage of your script's orchestration (start tracking before the producer starts, and stop after all results are collected).
4. **Reporting**: The main process must aggregate the results and write a JSON report to `/home/user/qa_report.json`. 

The JSON file `/home/user/qa_report.json` must have exactly the following structure:
```json
{
  "peak_memory_bytes": 123456,
  "prime_count": 42,
  "top_5_primes": [97, 89, 83, 79, 73]
}
```
*Notes on output:*
- `peak_memory_bytes`: The peak memory usage in bytes as reported by `tracemalloc.get_traced_memory()`.
- `prime_count`: The total number of expressions from the file that evaluated to a prime number.
- `top_5_primes`: A list of the 5 largest prime *values* found across all evaluated expressions, sorted in descending order. If there are duplicates, include them (e.g., if the highest prime is 97 and two expressions evaluated to 97, the list should start with `[97, 97, ...]`).

Ensure your script runs successfully and creates the `/home/user/qa_report.json` file.