You are a data scientist working on a reproducible computation pipeline for structural bioinformatics. 

Your goal is to parse observational structural data, reshape it, and fit a statistical model using a provided Rust pipeline. However, the current model fitting implementation diverges due to an improper step-size adaptation (learning rate explosion) in the optimization loop.

Here are the specific steps you must complete:

1. **Observational Data Reshaping**:
   You have two files located in `/home/user/data/`:
   - `sequence.fasta`: A standard FASTA file containing a protein sequence.
   - `structure.pdb`: A standard PDB file containing structural data for the same protein.

   Write a script to parse these files and generate a reshaped CSV dataset at `/home/user/data/combined.csv`. 
   The CSV must have a header `index,fasta_char,pdb_res_name,b_factor` and follow these rules:
   - Extract only the `CA` (Alpha Carbon) atoms from the PDB file.
   - `index` is the 1-based residue sequence number (from the PDB file).
   - `fasta_char` is the single-letter amino acid code from the FASTA file at that index (1-based).
   - `pdb_res_name` is the 3-letter residue name from the PDB file.
   - `b_factor` is the temperature factor (B-factor) column from the PDB file.

2. **Fixing the Rust Statistical Model Fitter**:
   There is a Rust project located at `/home/user/fitter/`. It reads a CSV file and fits a linear statistical model (`B-factor = alpha + beta * index`) using Gradient Descent.
   Currently, the numerical optimizer diverges (produces `NaN` or `inf`) because the gradient step-size (learning rate) is set too high for the scale of the indices.
   
   - Inspect and modify `/home/user/fitter/src/main.rs`.
   - Adjust the step-size adaptation or learning rate so that the gradient descent successfully converges (loss stops exploding and minimizes properly over 50000 iterations).

3. **Running the Pipeline**:
   - Compile and run the Rust project, passing your generated CSV file as the argument.
   - Ensure the Rust program outputs the final fitted parameters to a log file at `/home/user/output/model_results.txt`.
   - The output file must contain exactly two lines in this format:
     ```
     alpha: <value>
     beta: <value>
     ```
     (Replace `<value>` with the converged floating-point numbers rounded to 4 decimal places).

Create the `/home/user/output` directory if it does not exist. Your final result will be evaluated based on the correct generation of `combined.csv` and the convergence of `model_results.txt` to the correct statistical fit.