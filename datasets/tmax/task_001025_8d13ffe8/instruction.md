You are an AI assistant acting as a Machine Learning Engineer preparing training data for a new semantic search model. We have strict protocols to prevent data leakage between our training and test sets. Recently, we discovered that some automated ETL pipelines have been inadvertently injecting duplicated or near-duplicate test set examples into our training corpora, effectively leaking the test data.

Your objective is to fix our vector similarity dependency, construct an embedding index of the test set, and write a Python detector script that identifies and rejects leaked data in training corpora.

**Step 1: Fix and Install the Vendored Dependency**
We use the `annoy` library for fast approximate nearest neighbor (ANN) search. Due to our strict air-gapped environment, we have vendored the source code at `/app/annoy-1.17.3`. However, the previous engineer accidentally introduced a bug in its `setup.py` while trying to modify compiler flags, and it currently fails to build or install the C++ extension properly. 
1. Identify and fix the perturbation in `/app/annoy-1.17.3/setup.py`. 
2. Install the package locally in the system Python environment without using the internet (`pip install -e .` or similar).

**Step 2: Build the Test Set Index**
You are provided with:
- `/app/data/test_set_embeddings.csv`: A CSV file containing the test set. Each row has the format `ID,f1,f2,...,f128` representing a 128-dimensional embedding vector.
Write a script to load these vectors and build an Annoy index using the "angular" metric. Save this index to `/home/user/test_index.ann`. 

**Step 3: Create the Leakage Detector**
Write a script at `/home/user/detector.py` that acts as a filter for our training corpora.
Your script must be invokable via the CLI as follows:
`python3 /home/user/detector.py <input_corpus_dir> <output_json_log>`

- `<input_corpus_dir>` will contain multiple `.csv` files formatted identically to the test set (`ID,f1,f2,...,f128`).
- The script should load the test set Annoy index you built.
- For every row in every CSV file in the `<input_corpus_dir>`, query the test set index. If a training vector has an angular distance of **less than 0.05** to ANY vector in the test set, that training row is considered a "leak" (evil).
- If a CSV file contains **one or more** leaked rows, the entire file should be flagged as rejected. If it contains zero leaked rows, it should be flagged as accepted.
- The script must write a JSON dictionary to `<output_json_log>` mapping the absolute path of each processed CSV file to a boolean: `true` if the file is clean/accepted, and `false` if the file is rejected due to leakage.

Ensure your code is efficient and handles file paths correctly. We will run an automated test that passes a directory containing both clean and deliberately leaked (evil) CSV files to your `detector.py` script to verify it successfully isolates the clean files from the evil ones.