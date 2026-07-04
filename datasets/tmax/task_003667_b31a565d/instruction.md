You are a bioinformatics analyst tasked with building a reproducible, notebook-based workflow to identify coding regions in genomic sequences using spectral analysis, and designing primers for the most promising candidate. 

Your task is to set up a scientific Python environment, create a Jupyter Notebook that performs the analysis, and execute the notebook in a headless manner.

**Step 1: Scientific Environment Management**
Create a Python virtual environment at `/home/user/bioenv`.
Install the necessary packages: `numpy`, `biopython`, `jupyter`, and `papermill`.

**Step 2: Notebook-based Workflow Orchestration**
Create a Jupyter Notebook named `/home/user/sequence_analysis.ipynb`. You will later run this notebook using `papermill` to produce an executed notebook at `/home/user/sequence_analysis_executed.ipynb`.

**Step 3: Spectral Analysis and Primer Design**
In your notebook, write code to perform the following:
1. Parse the FASTA file located at `/home/user/input/sequences.fasta` (you can assume this file exists and contains multiple sequences).
2. Map each sequence to a numerical array using the following translation: `A=1.0, C=2.0, G=3.0, T=4.0`.
3. For each mapped sequence array, compute the power spectrum using the Fast Fourier Transform (FFT). The power at each frequency is the squared magnitude of the FFT output (`abs(fft_output)**2`).
4. Identify the "period-3" signal strength for each sequence by extracting the power value exactly at the index `len(sequence) // 3`.
5. Determine the ID of the sequence with the highest period-3 signal strength.
6. For this "best" sequence, design a naive primer pair:
   - **Forward Primer:** The first 20 nucleotides of the sequence.
   - **Reverse Primer:** The reverse complement of the last 20 nucleotides of the sequence.

**Step 4: Numerical Stability Testing**
Within the same notebook, test the robustness of the period-3 peak for your best sequence.
1. Take the original numerical array of the best sequence.
2. Add Gaussian noise with mean $\mu = 0.0$ and standard deviation $\sigma = 0.5$ to the numerical array.
3. Recompute the FFT power spectrum of this noisy array.
4. Verify if the index of the maximum power (strictly excluding the DC component at index 0) remains unchanged compared to the maximum power index (excluding index 0) of the original un-noised array. 
5. Store this boolean result (`True` if the peak index remained the same, `False` otherwise) in a variable.

**Step 5: Output Generation**
At the end of the notebook, output the results to a JSON file at `/home/user/results.json` with the following exact keys and types:
- `"best_seq_id"`: (string) The FASTA ID of the sequence with the strongest period-3 signal.
- `"forward_primer"`: (string) The 20-bp forward primer.
- `"reverse_primer"`: (string) The 20-bp reverse primer.
- `"stability_passed"`: (boolean) The result of the numerical stability test.

**Execution:**
Once the notebook is created, use `papermill` within your virtual environment to execute `/home/user/sequence_analysis.ipynb` and save the output to `/home/user/sequence_analysis_executed.ipynb`.