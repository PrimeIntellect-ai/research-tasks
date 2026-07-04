You are an AI assistant acting as a Machine Learning Engineer. Your task is to prepare a training dataset by combining raw DNA sequence data with synthetic Raman spectroscopy signals.

You must write a Python script at `/home/user/prepare_data.py` to process the data and generate a final CSV file at `/home/user/output/training_data.csv`. 

**Initial Environment:**
- Raw sequences: `/home/user/data/sequences.fasta`
- Spectroscopy signals: `/home/user/data/signals.csv`

**Data Processing Pipeline Requirements:**

1. **Primer Alignment:**
   - Parse the `/home/user/data/sequences.fasta` file.
   - For each sequence, search for the exact primer motif: `CGTAGCTACG`.
   - Find the 0-based index of the *first* occurrence of this motif. 
   - If the motif is NOT found in a sequence, completely discard that sequence from the dataset.

2. **Signal Processing & Numerical Operations:**
   - Load `/home/user/data/signals.csv`. This file contains `SeqID`, `wavenumber`, and `intensity` columns. The wavenumbers are equally spaced integers.
   - For each sequence retained from step 1, extract its corresponding signal intensities sorted by `wavenumber` in ascending order.
   - **Numerical Integration:** Calculate the total signal area (intensity over wavenumber) using the composite Trapezoidal rule.
   - **Numerical Differentiation:** Calculate the discrete second derivative of the intensity sequence $I$ to identify sharp peaks. Use the central finite difference formula for the interior points: $I''[k] = I[k-1] - 2I[k] + I[k+1]$. Do not calculate the second derivative for the first and last points.
   - Count the number of "sharp peaks", which we define strictly as any interior point $k$ where the second derivative $I''[k] < -1.5$.

3. **Output Generation:**
   - Ensure the directory `/home/user/output/` exists.
   - Create `/home/user/output/training_data.csv` with the following exact headers: `SeqID,PrimerIndex,TotalArea,SharpPeakCount`
   - The rows must be sorted alphabetically by `SeqID`.
   - Float values (TotalArea) should be rounded to 1 decimal place.

You may install any standard Python data science libraries (e.g., `numpy`, `pandas`, `scipy`, `biopython`) if you need them, but standard library tools are also sufficient. Run your script to generate the final file.