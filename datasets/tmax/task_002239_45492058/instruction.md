You are acting as a bioinformatics analyst. Your principal investigator (PI) has left you a voice memo at `/app/instructions.wav`. 

First, transcribe the voice memo to retrieve a specific 7-letter sequence motif and a target k-mer size ($k$) that the PI wants you to analyze.

Next, you will find a large FASTA file containing observational sequence data at `/home/user/data/sequences.fasta`. 

Your objective is to write a C++ program (using OpenMP for parallelization) that performs the following multi-stage analysis:
1. **Data Reshaping & Filtering:** Read the FASTA file and filter out any sequences that DO NOT contain the 7-letter motif mentioned in the audio.
2. **Graph/Network Construction:** For each filtered sequence, construct a directed de Bruijn-style graph using the target k-mer size $k$ (also from the audio). Calculate the stationary distribution of a random walk on this graph for each sequence to represent its structural profile as a probability distribution of k-mers.
3. **Probability Distance:** Calculate the pairwise Jensen-Shannon Divergence (JSD) between the stationary distributions of all filtered sequences.
4. **Parallelization:** Your C++ code must use OpenMP to parallelize the pairwise JSD distance matrix computation, as it will be computationally heavy. 

Your program should output the pairwise JSD distance matrix to `/home/user/output/jsd_matrix.csv`. The CSV should not have headers, and should simply be an $N \times N$ matrix of comma-separated floats, corresponding to the sequences in the order they appeared in the filtered FASTA file.

Write a bash script at `/home/user/run_analysis.sh` that compiles your C++ code with `-O3` and OpenMP flags, and then executes it. We will measure the correctness of your output matrix and the parallel efficiency of your code.