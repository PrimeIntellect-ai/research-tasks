You are an AI assistant helping a data researcher organize a growing collection of dataset descriptions. The researcher wants a lightweight, reproducible bash-based data processing pipeline to index dataset descriptions and recommend similar datasets based on query text.

We have a local tool that computes embedding vectors for text. 
It is located at `/home/user/embed.py`. You can call it by passing a text string:
`python3 /home/user/embed.py "Your text here"`
It will output a JSON array of 5 floats.

Your task is to build a full pipeline consisting of three Bash scripts in `/home/user/`.

**Phase 1: Embedding Computation & Indexing**
Write a script `/home/user/build_index.sh`.
1. It must read all `.txt` files in `/home/user/datasets/`.
2. For each file, read its content, call `/home/user/embed.py` to get the vector.
3. Save the results to `/home/user/index.tsv`.
   - The format of `index.tsv` must be tab-separated: `<filename> \t <comma_separated_vector>`
   - Example: `dataset_A.txt\t0.1,0.2,0.3,0.4,0.5`
   - Sort the file alphabetically by filename.

**Phase 2: Similarity Search & Recommendation**
Write a script `/home/user/recommend.sh` that takes exactly one argument (a query string).
1. Compute the embedding for the query string using `embed.py`.
2. Compute the cosine similarity between the query vector and every dataset vector in `/home/user/index.tsv`. You may use Python, `awk`, or `bc` invoked from within your Bash script to do the math.
3. Find the top 2 most similar datasets.
4. Output just the filenames of these top 2 datasets, one per line, sorted from highest similarity to lowest, into `/home/user/recommendations.txt`.

**Phase 3: Pipeline Reproducibility Testing**
Write a script `/home/user/test_reproducibility.sh`.
1. It should run `/home/user/build_index.sh` and save the output to `index_run1.tsv`.
2. It should run `/home/user/build_index.sh` again and save to `index_run2.tsv`.
3. It must perform a numerical accuracy test: verify that the L2 distance between corresponding vectors in the two files is exactly 0.0 for all rows.
4. If they match perfectly, echo "PASS" > `/home/user/test_result.txt`. Otherwise, echo "FAIL" > `/home/user/test_result.txt`.

**Execution:**
Once you have written the scripts, run them to process the data:
1. Run `bash /home/user/build_index.sh`
2. Run `bash /home/user/recommend.sh "Genomic and RNA sequencing"`
3. Run `bash /home/user/test_reproducibility.sh`

Ensure all output files (`index.tsv`, `recommendations.txt`, `test_result.txt`) are correctly generated in `/home/user/`.