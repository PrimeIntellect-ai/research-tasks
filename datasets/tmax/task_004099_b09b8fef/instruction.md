You are a data scientist working on a biological kinetics project. We rely on a proprietary, legacy, compiled tool located at `/app/kinetics_fitter` to calculate reaction rates and sequence alignment affinities from our experimental datasets. 

Recently, we've encountered a problem: some of our datasets contain subtle experimental artifacts ("evil" datasets) that cause `/app/kinetics_fitter` to produce silent, highly corrupted posterior estimates or hang entirely. We have a set of verified "clean" datasets in `/home/user/data/clean/` and a set of known artifactual datasets in `/home/user/data/evil/`.

Your task is to write a Python CLI script at `/home/user/filter.py` that acts as a pre-filter or sanitiser for these datasets. 

Your script must:
1. Accept an input directory and an output directory as command-line arguments: `python3 /home/user/filter.py <input_dir> <output_dir>`
2. Read all `.csv` files in the `<input_dir>`.
3. Perform a quick non-linear equation sanity check and density estimation on the dataset (representing initial MCMC posterior trace distributions) to determine if it is "clean" or "evil".
4. Copy ONLY the "clean" `.csv` files to `<output_dir>`, preserving their filenames.

You can use the provided `/app/kinetics_fitter` as a black-box oracle during your development to understand how the clean vs. evil files behave (e.g., exit codes or output anomalies). The binary takes a single file argument: `/app/kinetics_fitter <file.csv>`. 

Requirements:
- Your script must be written in Python.
- You should use libraries like `scipy`, `numpy`, or `pymc` (you may install them via pip).
- Ensure your script correctly preserves 100% of clean files and rejects 100% of evil files when run against the evaluation corpora.