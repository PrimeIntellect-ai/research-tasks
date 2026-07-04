You are an AI assistant helping a data scientist clean a dataset and perform a simple hyperparameter grid search using Bash.

You have been provided with a raw text file located at `/home/user/raw_data.txt`. Your objective is to tokenize this file, split it into 3 cross-validation folds, and find the best frequency threshold hyperparameter based on the training folds.

Please accomplish the following:
1. **Tokenization and Preparation**: 
   - Convert all text in `/home/user/raw_data.txt` to lowercase.
   - Replace all non-alphabetic characters (anything that is not `a-z`) with a single space.
   - Split the text so that there is exactly one word per line.
   - Remove any empty lines.
   - Save this intermediate result to `/home/user/tokenized.txt`.

2. **Cross-Validation Splitting**:
   - Distribute the lines from `/home/user/tokenized.txt` into 3 separate fold files using a strict round-robin sequence.
   - The 1st line goes to `/home/user/fold_1.txt`, the 2nd line to `/home/user/fold_2.txt`, the 3rd line to `/home/user/fold_3.txt`, the 4th line to `/home/user/fold_1.txt`, and so forth.

3. **Hyperparameter Tuning**:
   - Define your "training set" as the combination of `fold_1.txt` and `fold_2.txt`.
   - Consider a frequency threshold hyperparameter `T` (where `T` is an integer between 1 and 5). `T` defines the minimum number of times a word must appear in the training set to be included in the vocabulary.
   - You need to find the exact value of `T` that results in a vocabulary size of exactly **4 unique words** in the training set.
   - Write this single integer value `T` to `/home/user/best_param.txt`.

4. **Numerical Library Configuration**:
   - Write all your commands into an executable shell script at `/home/user/process.sh`.
   - The script must explicitly export `OMP_NUM_THREADS=1` at the very top to simulate strict single-threaded numerical environment constraints.

Make sure your script can be run to produce all required output files (`tokenized.txt`, `fold_1.txt`, `fold_2.txt`, `fold_3.txt`, and `best_param.txt`).