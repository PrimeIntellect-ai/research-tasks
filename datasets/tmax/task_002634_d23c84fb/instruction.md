You are a Machine Learning Engineer preparing a dataset for a deep learning model that classifies DNA sequences based on their structural and thermodynamic properties. Instead of feeding raw text into the model, you need to extract spectral features from the sequences and compare their distributions.

Your task is to process a provided FASTA file and generate a feature distance matrix using Python. 

Here are the specific requirements:

1. **Input Data**: A FASTA file is located at `/home/user/data/sequences.fasta`.
2. **Sequence Encoding**: Parse the FASTA file and convert each DNA sequence into a numerical signal using the Electron-Ion Interaction Potential (EIIP) values for nucleotides:
   - A = 0.1260
   - C = 0.1340
   - G = 0.0806
   - T = 0.1335
3. **Spectral Analysis**: For each numerical signal, compute the Discrete Fourier Transform (DFT). Calculate the Power Spectrum, which is the squared magnitude of the complex FFT output (i.e., $|X[k]|^2$).
4. **Probability Distribution**: Normalize the Power Spectrum for each sequence so that the sum of its values equals 1.0. This converts the spectrum into a probability mass function (PMF).
5. **Distance Metric**: Calculate the 1D Wasserstein distance (Earth Mover's Distance) between the normalized power spectrum of the **first sequence** in the FASTA file (acting as the reference) and the normalized power spectra of **all sequences** in the file (including itself). Use `scipy.stats.wasserstein_distance`.
6. **Output**: Write the results to a CSV file located exactly at `/home/user/output/spectral_distances.csv`.
   - The CSV must have two columns: `Sequence_ID` and `Wasserstein_Distance`.
   - `Sequence_ID` should match the exact FASTA header (without the `>` character).
   - Format the distance to 6 decimal places.

Create any necessary directories. You must write a Python script to perform this task and execute it to generate the final CSV.