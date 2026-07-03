You are a data analyst working on a probabilistic embedding retrieval system. You have a dataset of 100 items with pre-computed 3D embeddings and binary labels (0 or 1). 

Your objective is to build a C-based analysis tool to perform hyperparameter tuning using Bayesian-inspired score thresholding. 

Here are the requirements:
1. **The Mathematical Model**: 
   For each row in the dataset, calculate the Euclidean distance $D$ between its embedding $(x_1, x_2, x_3)$ and a target vector $T = (1.0, 1.0, 1.0)$.
   Compute the probabilistic score $S = e^{-D} \times \alpha$, where $\alpha$ is a hyperparameter representing the prior probability weight.
   If $S > 0.1$, the predicted label is 1. Otherwise, the predicted label is 0.

2. **C Implementation**:
   Write a C program at `/home/user/model.c` that compiles to `/home/user/model`.
   The program must take two command-line arguments: `<dataset_csv_path>` and `<alpha_value>`.
   It should read the CSV file, compute the predictions, calculate the overall accuracy (number of correct predictions divided by total rows in the provided CSV), and print ONLY the accuracy as a floating-point number (e.g., `0.75`).
   
3. **Cross-Validation Setup**:
   The primary dataset is located at `/home/user/embeddings.csv`. It has no header row. The columns are: `id,x1,x2,x3,label`.
   You need to perform a 5-fold cross-validation over the dataset to tune the hyperparameter $\alpha$.
   The folds should be created sequentially (Fold 1: rows 1-20, Fold 2: rows 21-40, Fold 3: rows 41-60, Fold 4: rows 61-80, Fold 5: rows 81-100).
   
4. **Hyperparameter Tuning Shell Script**:
   Write a bash script at `/home/user/tune.sh` that:
   - Compiles the C program using `gcc -o /home/user/model /home/user/model.c -lm`.
   - Splits `/home/user/embeddings.csv` into 5 training/validation splits based on the sequential folds defined above.
   - Evaluates the $\alpha$ values: `0.1, 0.3, 0.5, 0.7, 0.9`.
   - For each $\alpha$, calculates the average validation accuracy across the 5 folds.
   - Identifies the $\alpha$ value with the highest average cross-validation accuracy. (If there's a tie, pick the lowest $\alpha$).
   - Writes the best $\alpha$ value and its average validation accuracy (formatted to 2 decimal places, separated by a comma) to `/home/user/best_model.txt`. Example content: `0.5,0.82`

Execute your shell script to generate the final `/home/user/best_model.txt` file.