You are an MLOps engineer tasked with building a lightweight, reproducible artifact tracking pipeline. You have a set of high-dimensional experiment embeddings, and you need to implement a dimensionality reduction and similarity search tool, along with a pipeline reproducibility test.

You have been provided with a dataset of experiment embeddings at `/home/user/embeddings.csv`. 
Each line follows the format: `experiment_id,v1,v2,v3,v4,v5` (all values are floats, except for the string `experiment_id`).

Your objective is to complete the following three steps:

1. **Dimensionality Reduction & Similarity Search (Rust)**
Write a standalone Rust program at `/home/user/process.rs`. This program must:
- Accept a single command-line argument: the path to a CSV file.
- Read and parse the CSV file.
- Apply a deterministic dimensionality reduction to each row to project the 5D vectors into 2D space using this exact mapping:
  - `x = v1 + v2`
  - `y = v3 + v4 + v5`
- Find the experiment ID that is *most similar* (i.e., has the smallest Euclidean distance in the new 2D space) to the experiment named `target_run`. (Do not match `target_run` with itself).
- Print ONLY the ID of this closest experiment to standard output.

2. **Calculate the Target**
Compile your Rust script and run it against `/home/user/embeddings.csv`. Save the output (the ID of the closest experiment) into `/home/user/closest.txt`.

3. **Pipeline Reproducibility Testing (Bash)**
In MLOps, order-invariance is a key property of similarity search. Write a bash script at `/home/user/test_repro.sh` that validates the reproducibility of your Rust program. The script must:
- Compile `/home/user/process.rs` into `/home/user/process`.
- Run the compiled binary on `/home/user/embeddings.csv` and store the result.
- Use the `shuf` command to randomly shuffle the lines of `/home/user/embeddings.csv` and save it to `/home/user/shuffled.csv`.
- Run the compiled binary on `/home/user/shuffled.csv` and store the result.
- Compare the two results. If they are exactly the same, print `PASS` to standard output. Otherwise, print `FAIL`.

Make sure your Rust script is entirely self-contained (using standard library only, so it can be compiled directly with `rustc /home/user/process.rs`).