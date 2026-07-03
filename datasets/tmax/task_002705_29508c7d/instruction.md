You are a bioinformatics analyst working on a PCR primer design pipeline. Your principal investigator (PI) left you an audio memo with specific instructions for your next experiment, but no written notes. 

Your task is to orchestrate a complete primer discovery and evaluation pipeline using Bash. 

1. **Audio Transcription:** Listen to the audio file located at `/app/lab_notes.wav`. It contains the target gene name, the required primer length, the target annealing temperature (Tm), and the number of iterations for the Monte Carlo simulation. 
2. **Sequence Extraction & Primer Design:** Write a Bash script, `/home/user/pipeline.sh`, that parses `/app/genome.fasta` to extract the sequence for the target gene mentioned in the audio. 
3. **Array Manipulation & Linear Math:** Within your Bash script, generate all possible forward and reverse primers of the specified length from the gene sequence. Use Bash arithmetic to calculate the Tm of each candidate using the simplified Marmur-Doty formula: `Tm = 2 * (A + T) + 4 * (G + C)`. Filter candidates to keep only those with exactly the target Tm.
4. **Monte Carlo Simulation & Workflow Orchestration:** For all valid forward/reverse primer pairs, your Bash script must invoke the provided headless Jupyter notebook `/app/simulate_pcr.ipynb` (using `jupyter nbconvert --execute` or `papermill`), passing the primer pair sequences and the requested Monte Carlo iterations as parameters. The notebook simulates secondary structures and outputs an expected efficiency score.
5. **Selection:** Identify the primer pair with the highest amplification efficiency.
6. **Output:** Write the best forward and reverse primer sequences (comma-separated, e.g., `ATGCATGCATGCATGCATGC,CGTACGTACGTACGTACGTA`) to `/home/user/best_primers.txt`.

Ensure your Bash script successfully automates steps 2 through 6. The final output file will be evaluated by an automated script to ensure the primer pair achieves an efficiency score above a strict threshold.