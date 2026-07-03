You are acting as a Machine Learning Engineer who is preparing a training dataset for a sequence classification model. You need to extract features from raw bioinformatics data and merge them with observational labels. 

Your raw data consists of two files:
1. `/home/user/data/sequences.fasta`: A FASTA format file containing DNA sequences.
2. `/home/user/data/observational.tsv`: A tab-separated file containing observational labels for each sequence. The format is `SeqID\tObservationLabel`.

Your objective is to write a C program that calculates a specific biological feature, merges it with the observational data, and outputs a properly shaped CSV file for model training. Because the dataset is expected to grow significantly, you must parallelize the feature extraction step using OpenMP.

**Requirements:**
1. Create a C program at `/home/user/src/prepare_dataset.c`.
2. The program must parse the FASTA file and the TSV file.
3. For each sequence, calculate the **Purine Ratio**: `(Count of 'A' + Count of 'G') / Total Sequence Length`. 
4. The calculation of the Purine Ratio across sequences **must** be parallelized using OpenMP (`#pragma omp parallel for`).
5. Combine the computed feature with the corresponding label from the TSV file.
6. The program must write the joined results to `/home/user/output/ml_features.csv`.
7. The output CSV format must be exactly: `SeqID,PurineRatio,ObservationLabel` (with a header row). 
8. `PurineRatio` must be formatted to exactly 4 decimal places (e.g., `0.5432`).
9. Compile your program to an executable at `/home/user/bin/prepare_dataset` using GCC with the appropriate OpenMP flags. Run the program to generate the output CSV.
10. The output CSV should be sorted alphabetically by `SeqID` (if your program doesn't sort, you can sort it using standard bash tools after it's generated, but the final file at `/home/user/output/ml_features.csv` must have the header first, followed by sorted data rows).

Ensure all required directories (`/home/user/src`, `/home/user/bin`, `/home/user/output`) exist before compiling and running your code.