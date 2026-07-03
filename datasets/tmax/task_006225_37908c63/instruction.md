You are a Machine Learning Engineer preparing training data for a bioinformatics model that predicts primer binding affinity. You need to process a raw list of DNA sequences, calculate their alignment scores against a target primer, split them into two statistical groups, and output a formatted dataset.

Your task is to write and execute a C++ program (`/home/user/prepare_data.cpp`) that performs the following steps:

1. **Read Data:** Read a list of DNA sequences from `/home/user/sequences.txt` (one sequence per line).
2. **Primer Alignment (Analytical Validation):** The target primer sequence is exactly `GATCGATCG` (length 9). For each sequence in the file, calculate the "Binding Score". The Binding Score is defined as the maximum number of character-by-character matches between the primer and *any* contiguous sliding window of length 9 within the sequence. 
3. **Statistical Grouping:** Calculate the GC-content of each sequence (the percentage of characters that are either 'G' or 'C', out of the total length of the sequence).
   - If the GC-content is >= 50.0%, assign the sequence to Group `A`.
   - If the GC-content is < 50.0%, assign the sequence to Group `B`.
4. **Data Export:** Generate a CSV file at `/home/user/training_data.csv` with the header `sequence,gc_percentage,group,binding_score`. The `gc_percentage` should be formatted to exactly two decimal places (e.g., `45.33`).
5. **Hypothesis Comparison:** Calculate the mean Binding Score for Group A and the mean Binding Score for Group B. Compare them to validate if the absolute difference is strictly greater than 1.0. 
   Generate a summary text file at `/home/user/stats.txt` with exactly these three lines (replace placeholders with actual values rounded to two decimal places):
   ```
   Mean Score A: [value]
   Mean Score B: [value]
   Significant Difference: [true/false]
   ```

Requirements:
- You must write the solution in C++11 or later.
- Compile your code using `g++` and run it to produce `/home/user/training_data.csv` and `/home/user/stats.txt`.
- Do not use any external non-standard C++ libraries. Standard library is fine.