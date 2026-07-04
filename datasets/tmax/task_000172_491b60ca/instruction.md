You are a Machine Learning Engineer tasked with building a lightweight, Bash-orchestrated ETL and hyperparameter tuning pipeline for a text retrieval system.

Your goal is to prepare the data, reduce the dimensionality of the embeddings, and find the best hyperparameters using Bash scripts.

**Initial State:**
You have the following files in `/home/user/`:
1. `raw_data.csv`: A raw dataset with columns `id,split,text`.
2. `embed.py`: A script that takes a TSV file (`id,text`) and outputs a CSV file with 10 embedding columns (`id,e1,e2,...,e10`).
3. `evaluate.py`: A script to test retrieval accuracy. Usage: `python3 evaluate.py <train_embeddings_csv> <test_embeddings_csv> <K> <T>`. It outputs a single float representing the accuracy score.

**Step 1: ETL Pipeline (`/home/user/etl.sh`)**
Write a Bash script named `etl.sh` that processes `raw_data.csv`:
- Filter out any rows where the `text` column is empty or only whitespace.
- Filter out any rows where the `split` is "ignore".
- Separate the remaining rows into `/home/user/clean_train.tsv` (where split is "train") and `/home/user/clean_test.tsv` (where split is "test").
- The output TSV files should not have headers, and should only contain two columns separated by a tab: `id` and `text`.

**Step 2: Embedding Generation**
Run the provided `/home/user/embed.py` on both `clean_train.tsv` and `clean_test.tsv` to generate `/home/user/train_embed.csv` and `/home/user/test_embed.csv`. (You can do this manually in the terminal or add it to your scripts).

**Step 3: Dimensionality Reduction (`/home/user/reduce.sh`)**
Write a Bash script named `reduce.sh` that takes a CSV file of embeddings and an integer `K`.
Usage: `./reduce.sh <input.csv> <K> > <output.csv>`
It should output a new CSV containing only the `id` column and the first `K` embedding columns (i.e., columns 1 through K+1 of the input CSV).

**Step 4: Hyperparameter Tuning (`/home/user/tune.sh`)**
Write a Bash script named `tune.sh` that performs a grid search to find the best hyperparameters for the retrieval system.
- Iterate over $K \in \{2, 4, 6, 8\}$.
- Iterate over Threshold $T \in \{0.1, 0.5, 0.9\}$.
- For each combination, use `reduce.sh` to create temporary reduced embedding files for both train and test.
- Call `python3 evaluate.py` with the reduced files, `K`, and `T` to get the score.
- Keep track of the highest score and its corresponding `K` and `T`.

**Final Output:**
Once `tune.sh` finishes running, it must create a file at `/home/user/best_params.txt` containing exactly one line in this format:
`K=<best_K>,T=<best_T>,Score=<highest_score>`

Ensure all your bash scripts are executable (`chmod +x`). 
Do not modify `embed.py` or `evaluate.py`.