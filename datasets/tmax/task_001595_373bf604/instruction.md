You are an MLOps engineer tasked with building a lightweight, Bash-only experiment tracking pipeline. Because this pipeline must run on restricted edge devices, you cannot use Python, R, or standard ML libraries. You must implement tokenization, dataset bootstrapping, model inference, and artifact tracking entirely using standard Linux utilities (Bash, awk, sed, tr, bc, etc.).

Your goal is to write a complete pipeline that processes a raw dataset, runs inference using a hardcoded text-scoring "model", and logs the artifacts.

**Phase 1: Dataset Preparation & Tokenization**
Write a script `/home/user/tokenize.sh` that reads from standard input and writes to standard output.
- It must convert all text to lowercase.
- It must remove all punctuation and non-alphanumeric characters *except* spaces and newlines.
- Multiple consecutive spaces should be condensed to a single space, and leading/trailing spaces on each line should be removed.

**Phase 2: Bootstrap Sampling**
Write a script `/home/user/bootstrap.sh` that takes a file path as its first argument and outputs a bootstrapped sample (random sampling *with replacement*) of the file to standard output.
- The output must have the exact same number of lines as the input file.
- Use `shuf -r -n <num_lines>` (or an equivalent awk method) to achieve this.

**Phase 3: Model Architecture Reconstruction (Inference)**
Write a script `/home/user/inference.sh` that reads a tokenized dataset from standard input, scores each line, and outputs the average score of all lines to 4 decimal places using `bc` (e.g., `1.2500`).
The "model" is a Bag-of-Words linear scorer with the following token weights:
- "critical": -5.0
- "error": -3.0
- "warning": -1.0
- "info": 0.5
- "success": 2.0
- "resolved": 3.0
All other words have a weight of 0.0.
The score of a line is the sum of the weights of its words.

**Phase 4: Execution and Artifact Tracking**
Write a master script `/home/user/run_experiment.sh` that does the following:
1. Creates an artifact directory `/home/user/artifacts/`.
2. Reads the raw dataset from `/home/user/raw_data.txt`.
3. Tokenizes it and saves it to `/home/user/artifacts/tokenized.txt`.
4. Calculates the mean model score on the *entire* `tokenized.txt` dataset using `inference.sh`, and saves this single number to `/home/user/artifacts/baseline_score.txt`.
5. Generates 5 distinct bootstrap samples of `tokenized.txt`. For each sample (1 to 5), it calculates the mean score using `inference.sh`, and appends the result on a new line to `/home/user/artifacts/bootstrap_scores.txt`.

Before running your master script, create the raw dataset file `/home/user/raw_data.txt` with at least 10 lines of mock system logs containing a mix of the weighted keywords and punctuation. Make sure your scripts are executable. Run `run_experiment.sh` so the artifacts are generated.