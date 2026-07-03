You are a machine learning engineer preparing synthetic spectroscopy data for a new protein sequence model. You need to parse a FASTA file containing protein sequences, simulate a synthetic NMR spectroscopy signal for each sequence, apply a smoothing filter, and save the formatted training data. You also need to write a regression test for your pipeline.

Perform the following steps:

1. **Environment Setup**
Create an isolated environment (e.g., a virtual environment or local project directory) for your work at `/home/user/ml_env`. You may use any programming language you prefer to implement the solution, but ensure all dependencies are installed locally in your workspace or via system packages without requiring `sudo` root access. 

2. **Signal Generation and Processing**
Write a script to process the FASTA file located at `/home/user/data/input.fasta`.
For each sequence in the FASTA file, generate a synthetic spectroscopy signal array where each element corresponds to an amino acid in the sequence. 
Compute the "Raw" signal value for the character at 0-based index `i` using the following formula:
`Raw[i] = (ASCII_value_of_character * 10) + (sin(i) * 5.0)`
(Note: Use radians for the sine function).

Next, apply a moving average filter of window size 3 to smooth the signal. For each index `i`:
`Filtered[i] = (Raw[i-1] + Raw[i] + Raw[i+1]) / 3.0`
If `i-1` or `i+1` is out of bounds (i.e., less than 0 or greater than/equal to the sequence length), treat the missing `Raw` value as `0.0`. You must still divide by `3.0`.

Round each element in the `Filtered` array to exactly 2 decimal places.

3. **Output Generation**
Your script must output a JSON file at `/home/user/output/training_data.json`.
The JSON should be an object mapping the FASTA sequence IDs (without the `>`) to their corresponding `Filtered` numeric arrays.

4. **Regression Testing**
To ensure the pipeline is robust, create a shell script at `/home/user/test_pipeline.sh` that acts as a regression test. 
When executed, this script should:
- Run your pipeline on a test file `/home/user/data/test.fasta`.
- Compare the generated JSON output against the expected baseline at `/home/user/data/expected_test.json`.
- Exit with code `0` if the output matches the baseline exactly, and a non-zero exit code if they differ.

Note: All input files (`input.fasta`, `test.fasta`, and `expected_test.json`) have already been created for you in `/home/user/data/`. Ensure your script outputs to the `/home/user/output/` directory, which also already exists.