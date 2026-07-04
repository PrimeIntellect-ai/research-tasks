You are a machine learning engineer preparing training data for a new embedding model. We have a problem with adversarial data poisoning. We need to filter out malicious vectors from our datasets before training.

Your task is to build a C-based sanitization tool that performs dimensionality reduction on the datasets, identifies vectors that fall too close to known "adversarial anchors" in the reduced space, and outputs a clean dataset.

**Step 1: Fix and Compile the SVD Library**
We use `svdlibc` (version 1.4) for dimensionality reduction. The source code is vendored at `/app/svdlibc`. However, the previous engineer left it in a broken state; it fails to compile due to a linker error. 
1. Fix the `Makefile` in `/app/svdlibc` so that it successfully compiles to a static library `libsvd.a`. 
2. Ensure you understand its C API (e.g., `svdNewSMat`, `svdLAS2A`).

**Step 2: Build the Sanitizer Tool**
Write a C program at `/home/user/sanitizer.c` and compile it to `/home/user/sanitizer`. You must link it against the fixed `libsvd.a`.
The CLI invocation must be exactly:
`./sanitizer <input_dataset.txt> <anchors.txt> <output_dataset.txt> <experiment_log.json>`

**Sanitizer Logic:**
1. **Data Parsing:** Read `<input_dataset.txt>` and `<anchors.txt>`. Both files contain rows of whitespace-separated floats (all vectors have 50 dimensions). Let $N$ be the number of rows in the input dataset, and $M$ be the number of rows in the anchors file.
2. **Dimensionality Reduction:** Combine the input dataset and anchors into a single $ (N+M) \times 50 $ matrix. Use `svdlibc` to compute the Singular Value Decomposition, keeping only the top $k=3$ dimensions (compute the first 3 singular vectors).
3. **Similarity Search (Filtering):** Project all vectors (dataset and anchors) into this new 3-dimensional space. For each vector in the *input dataset*, calculate the Euclidean distance to every *anchor* vector in the 3D space. 
4. **Validation/Rejection:** If a dataset vector has a Euclidean distance strictly less than `1.50` to *any* anchor vector in the 3D space, it is considered "poisoned" and must be rejected.
5. **Output:** Write the preserved (clean) vectors to `<output_dataset.txt>` in the original 50-dimensional format (whitespace-separated). Do not write the anchors or rejected vectors.
6. **Experiment Tracking:** Write a JSON file to `<experiment_log.json>` containing the metrics of the run. It must match this exact schema:
```json
{
  "total_input_vectors": 1000,
  "rejected_vectors": 45,
  "top_singular_value": 14.562
}
```
*(Float precision for the singular value in the JSON should be at least 3 decimal places).*

**Step 3: Test Against the Corpora**
We have provided sample training data in `/home/user/corpora/`.
- `/home/user/corpora/clean/`: Contains 5 CSVs of clean text embeddings. Your tool must preserve 100% of the rows in these files.
- `/home/user/corpora/evil/`: Contains 5 CSVs where adversarial vectors were injected. Your tool must reject the poisoned vectors.
- The known anchors are located at `/home/user/corpora/anchors.txt`.

Our automated verifier will build your tool and test it against a hidden evaluation set of clean and evil corpora using the exact CLI signature above. Good luck!