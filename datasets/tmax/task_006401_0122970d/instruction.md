You are an AI assistant acting as a bioinformatics analyst. 

We have a multifasta file located at `/home/user/sequences.fasta`. We also have a Python sequence analysis script at `/home/user/calc_gc.py` that computes the GC content of a single FASTA sequence. 

To process this efficiently, you need to use a domain decomposition approach to process the file in parallel:
1. Create a directory called `/home/user/chunks`.
2. Split the multifasta file `/home/user/sequences.fasta` into individual fasta files inside `/home/user/chunks/` (one file per sequence). You can name the files whatever you like, but they must end in `.fa`.
3. Use `xargs` with up to 4 parallel processes (`-P 4`) to execute `/home/user/calc_gc.py` on every `.fa` file in the `/home/user/chunks/` directory. 
4. The Python script outputs a tab-separated line for each file: `SequenceID    GC_Content_Ratio`.
5. Capture these results and perform a simple thresholding (statistical anomaly detection): find all sequences where the GC content ratio is strictly greater than `0.60`.
6. Extract **only the Sequence IDs** of these anomalous sequences, sort them alphabetically, and write them to a log file at `/home/user/high_gc_anomalies.txt`.

Ensure your final output file contains exactly one sequence ID per line and nothing else.