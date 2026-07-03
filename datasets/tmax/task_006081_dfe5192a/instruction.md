You are an MLOps engineer responsible for ensuring the reproducibility of a C-based feature engineering and dimensionality reduction pipeline. 

We have a partially written C program at `/home/user/pipeline/project.c` that reads a set of feature vectors, subtracts a bias vector (feature engineering/centering), and projects the centered vectors onto a 1D space using a weight vector (dimensionality reduction). 

Your task:
1. Complete the code in `/home/user/pipeline/project.c`. Specifically, use the correct GNU Scientific Library (GSL) BLAS function to compute the dot product of the centered feature vector and the weight vector.
2. Compile the C program into an executable named `/home/user/pipeline/project`. You will need to correctly configure and link the required GSL numerical libraries.
3. Run the compiled executable to process the artifact data. The program should read `/home/user/pipeline/input.csv`, use `/home/user/pipeline/weights.csv` and `/home/user/pipeline/bias.csv`, and output the 1D projected values to `/home/user/pipeline/output.txt`.

The output file `/home/user/pipeline/output.txt` must contain one projected value per line, formatted to exactly two decimal places (e.g., `1.50`). 

All input files (input.csv, weights.csv, bias.csv) have the same format: comma-separated floats. 
`input.csv` has one feature vector per line. `weights.csv` and `bias.csv` contain exactly one line. The dimensionality of the vectors is 3.

Verify your output to ensure the pipeline is reproducible and mathematically sound.