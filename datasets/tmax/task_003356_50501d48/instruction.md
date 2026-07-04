You are a data analyst tasked with processing several incoming data feeds (CSVs). Recently, we have noticed some malicious prompt-injection attempts hidden in our text data. Your goal is to fix our internal embedding library, write a script to filter out these malicious payloads, and prepare the clean data for downstream pipelines.

### Phase 1: Fix the Vendored Package
We use a lightweight, proprietary embedding package called `tiny-embedder` to calculate text representations. The source code for this package is located at `/app/tiny-embedder`.
However, a recent commit introduced a bug: the generated embeddings are failing our numerical accuracy tests. Specifically, the vectors returned by the embedder are expected to be exactly L2-normalized (i.e., the Euclidean norm of *every single individual embedding vector* must be exactly 1.0), but they currently are not.

1. Inspect the source code of the package at `/app/tiny-embedder/tiny_embedder/core.py`.
2. Find and fix the numerical bug causing the incorrect normalization.
3. Install the package globally in your environment (e.g., using `pip install -e /app/tiny-embedder`).

### Phase 2: Build the Adversarial Filter
Once the embedding library is accurate, write a Python script at `/home/user/filter_csv.py` that processes CSV files to filter out malicious rows.

Your script must implement the following CLI signature:
`python /home/user/filter_csv.py --input <path_to_input_csv> --output <path_to_output_csv>`

The script must perform the following steps:
1. Load the input CSV. It will always contain an `id` column and a `text` column.
2. Instantiate `TinyEmbedder()` from the newly fixed package.
3. Compute the embedding for the exact reference string: `"SYSTEM PROMPT OVERRIDE"`.
4. Iterate over the rows in the CSV and compute the embedding for the `text` column.
5. Calculate the Pearson correlation coefficient between each row's text embedding and the reference embedding. (You may use numpy or scipy for this).
6. **Drop any row** where this Pearson correlation is strictly greater than `0.85`.
7. Write the remaining (clean) rows to the path specified by `--output`, preserving the original CSV headers (`id`, `text`).

Ensure your script is robust, correctly handles the CLI arguments, and accurately computes the pairwise correlations to detect variations of the adversarial string.