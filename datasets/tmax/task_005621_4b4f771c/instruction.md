You are an MLOps engineer tasked with analyzing experiment artifacts. You have a directory of log files from various model training runs, and you need to build a shell-based ETL pipeline to extract metadata, perform bootstrap sampling, and retrieve the most relevant experiment description based on semantic similarity.

Your task is to write a bash script `/home/user/analyze.sh` that performs the following steps exactly:

1. **Extract (ETL):** Read all `.log` files in `/home/user/artifacts/` (which contains files named `exp_1.log` through `exp_50.log`). Extract the text from the line that begins with `Artifact-Desc: ` (excluding the prefix itself). 
2. **Sort:** Order the extracted descriptions based on their corresponding experiment file numbers (e.g., the description from `exp_1.log` should be first, `exp_2.log` second, etc.). Store this ordered list in a zero-indexed bash array.
3. **Bootstrap Sample:** In your bash script, initialize the random seed by running `RANDOM=123`. Then, generate a bootstrap sample (sampling with replacement) of exactly 20 descriptions from your ordered array. To pick an index for each of the 20 samples (in a loop from 1 to 20), use the formula `index=$((RANDOM % 50))` and append the description at that index to a new file `/home/user/sample.txt` (one description per line).
4. **Embedding Retrieval:** You have been provided with a Python script `/home/user/retrieve.py`. This script takes two arguments: a file containing a list of descriptions (one per line) and a query string. It computes basic TF-IDF embeddings and returns the description that is most similar to the query. 
   In your bash script, call this python script using your generated `/home/user/sample.txt` and the exact query string: `"robust convolutional network with dropout"`.
5. **Output:** Save the stdout output of the Python script (the best matching description) to a file `/home/user/best_match.txt`.

Ensure your bash script has execution permissions and works seamlessly when executed as `./analyze.sh`. 

**Verification:**
An automated test will run `./analyze.sh` and then verify the exact contents of `/home/user/sample.txt` and `/home/user/best_match.txt`.