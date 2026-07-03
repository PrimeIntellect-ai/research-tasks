You are an ML Engineer preparing a dataset to train a model that predicts DNA primer binding efficiencies. You have a raw dataset containing primer sequences, target sequences, and temperature/concentration experimental data points. You need to extract features from this raw data to use in your model.

Your task is to write a C++ program that processes this data, performing basic sequence alignment and curve fitting, and outputs a feature CSV file.

**Input Data:**
A tab-separated file will be provided at `/home/user/raw_data.tsv` containing three columns:
1. `primer_sequence`: A short DNA string (e.g., "ATGC").
2. `target_sequence`: A DNA string of the exact same length as the primer.
3. `experimental_data`: A semicolon-separated list of `x,y` coordinate pairs representing experimental assay results, where `x` is concentration and `y` is the measured melting temperature (e.g., "1.0,2.1;2.0,4.0;3.0,6.2").

**Processing Requirements:**
Write a C++ program at `/home/user/feature_extractor.cpp` that reads `/home/user/raw_data.tsv` line by line and computes two features for each row:
1. **Alignment Score:** The number of matching nucleotides at the exact same string indices between the `primer_sequence` and `target_sequence` (i.e., the string length minus the Hamming distance).
2. **Regression Slope:** The slope ($m$) of the line of best fit ($y = mx + b$) for the `experimental_data` coordinates, using simple ordinary least squares linear regression. 

**Output Requirements:**
Your C++ program must write the computed features to `/home/user/features.csv`.
- Each line in the CSV must correspond to the respective line in the input TSV.
- The format must be strictly: `alignment_score,slope`
- The `slope` must be formatted to exactly 2 decimal places.
- Do not include headers in the output file.

**Execution:**
Compile your C++ program using `g++` (standard C++17) and run it to generate the `/home/user/features.csv` file. Ensure the final CSV file exists and has the correct permissions to be read.