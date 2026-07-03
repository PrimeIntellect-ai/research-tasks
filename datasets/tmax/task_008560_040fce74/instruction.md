You are a data engineer optimizing a new ETL pipeline. We have a mathematical transformation step that scores incoming data records, and we need to benchmark its inference performance in C++ to track our experiments.

Please write and execute a C++ program that simulates the scoring inference, measures its performance, and logs the experiment.

Here are the exact requirements:

1. Create a C++ source file at `/home/user/etl_inference.cpp`.
2. The program must generate a batch of `1000000` (1 million) simulated records. The value of the $i$-th record (0-indexed) should be a `double` calculated as: $x_i = i \times 0.001$.
3. Implement the scoring function that takes $x$ and calculates: $f(x) = 3.5x^3 - 1.2x^2 + 0.8x - 4.1$.
4. Iterate through the batch, compute the score for each record, and calculate the sum of all scores (use `double` precision for all calculations and the sum).
5. Using `std::chrono`, measure the time taken **only** for the inference loop (the loop where you compute $f(x)$ and add it to the sum). Do not include the time taken to initialize the array or write the output.
6. The program must write the results to a JSON experiment tracking file at `/home/user/experiment_log.json`. The JSON must exactly match this format:
```json
{
  "language": "C++",
  "batch_size": 1000000,
  "inference_time_sec": <time_in_seconds_as_float>,
  "sum_scores": <computed_sum_as_float>
}
```
7. Compile the program using `g++` with the `-O3` optimization flag. The output executable must be saved as `/home/user/etl_inference`.
8. Execute the compiled binary so that the JSON log file is produced.