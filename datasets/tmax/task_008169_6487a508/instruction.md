You are acting as an MLOps engineer tasked with tracking and validating artifact metadata from recent experiments. 

We have experiment data split across two sources in `/home/user/data/`:
1. `experiments.jsonl`: Contains `experiment_id`, `desc` (text description of the architecture), and `baseline_score` (float).
2. `metrics.jsonl`: Contains `experiment_id` and `weights` (an array of exactly 5 floats).
There is also a vocabulary file for tokenization at `/home/user/data/vocab.txt` where each line is formatted as `<word> <token_id>`.

Your objective is to write a Go program (`/home/user/mlops_tracker.go`) that acts as an artifact pipeline. The program must:
1. **Multi-source Data Joining**: Read and join `experiments.jsonl` and `metrics.jsonl` on `experiment_id`. Ignore any records that don't exist in both files.
2. **Tokenization**: Parse the `desc` field of each joined record. Lowercase the text, split by single spaces, and map each word to its integer token ID using `vocab.txt`. Any word not in the vocabulary should be mapped to `0`. Pad the resulting sequence with `0`s at the end, or truncate it, so that every sequence is exactly length 5.
3. **Model Architecture Reconstruction**: We are evaluating a trivial linear model projection. For each experiment, compute the `computed_score` as the dot product between the token ID array (converted to floats) and the `weights` array.
4. **Inference Performance Benchmarking**: Measure the total time taken to compute the scores for all joined records (excluding file I/O and tokenization overhead—just the inference loop over the pre-processed arrays). Calculate the average inference time per record in nanoseconds.
5. **Numerical Accuracy Testing**: Calculate the Mean Squared Error (MSE) between the `computed_score` and the `baseline_score` across all joined experiments.

The Go program must output a final report to `/home/user/report.json` in the following exact JSON format:
```json
{
  "mse": 4.333333333333333,
  "average_inference_ns": 150.5,
  "results": [
    {
      "experiment_id": "exp1",
      "computed_score": 60.0
    },
    ...
  ]
}
```
*Note: Sort the `results` array alphabetically by `experiment_id`.*

Write, compile, and execute the Go program so that `/home/user/report.json` is generated successfully. Do not use external Go libraries outside the standard library.