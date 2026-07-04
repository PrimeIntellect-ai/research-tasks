You are a data scientist working on biophysical modeling. You need to estimate the secondary structure fractions of several proteins by fitting their Circular Dichroism (CD) spectra to known basis spectra.

You are provided with the following files in `/home/user/data/`:
1. `sequences.fasta`: A FASTA file containing the sequences of the proteins.
2. `spectra.csv`: A CSV file containing the CD spectra for each protein. Columns: `seq_id`, `wavelength`, `intensity`.
3. `basis.csv`: A CSV file containing reference basis spectra for alpha-helix, beta-sheet, and random coil. Columns: `wavelength`, `alpha`, `beta`, `coil`.

Your task is to write and execute a bash script `/home/user/run_pipeline.sh` that does the following:
1. Sets up a Python virtual environment at `/home/user/venv` and installs the necessary scientific packages (`numpy`, `scipy`, `biopython`, `pandas`).
2. Runs a Python script `/home/user/fit_spectra.py` (which you must create) that:
   - Parses `sequences.fasta` to extract the `seq_id` for each protein.
   - For each protein, solves the overdetermined linear system $B \mathbf{c} = \mathbf{S}$ using ordinary least squares to find the coefficients $\mathbf{c} = [c_{\text{alpha}}, c_{\text{beta}}, c_{\text{coil}}]$. Here, $B$ is the matrix of basis spectra and $\mathbf{S}$ is the intensity spectrum of the protein.
   - Normalizes the resulting coefficients so that their sum equals exactly 1.0. (If any coefficients are negative, just normalize the raw least-squares values by their sum: $c_i' = c_i / \sum c_j$).
   - Computes the fits in parallel using Python's `multiprocessing.Pool` with exactly 4 worker processes.
   - Saves the final normalized coefficients to `/home/user/results.csv` with columns `seq_id,alpha,beta,coil`, rounded to 4 decimal places, sorted alphabetically by `seq_id`.

Ensure your bash script executes successfully and generates the `/home/user/results.csv` file.

Permissions and environment:
- You may use standard system tools to create the scripts.
- Ensure your scripts are executable.