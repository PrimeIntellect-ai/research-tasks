You are acting as a bioinformatics analyst. We need to implement a high-performance sequence alignment tool to process a new batch of DNA sequencing data. 

Your task is to write a C++ program that computes the optimal global alignment score (using the Needleman-Wunsch algorithm) for pairs of DNA sequences. 

However, the specific penalty scores for this batch of data were sent to us as an image snippet by the lead researcher.
1. Inspect the image located at `/app/scoring_rules.png`. Extract the Match reward, Mismatch penalty, and Gap penalty (linear gap penalty) from this image.
2. Write a C++ program (using C++17) that reads pairs of DNA sequences from standard input and prints the optimal global alignment score for each pair to standard output. 
   - The input format will be: each line contains two DNA sequences separated by a comma (e.g., `ACGT,ACGG`).
   - The output format must be: a single integer score per line, corresponding exactly to the input sequence pair.
3. Save your C++ source code at `/home/user/aligner.cpp`.
4. Compile your program to the executable `/home/user/aligner`. Use `g++` with the `-O3` flag for performance.
5. We have provided a small sample dataset at `/app/sample_pairs.txt`. Run your compiled program on this file and save the output to `/home/user/sample_scores.txt`.

Our automated testing suite will evaluate your compiled `/home/user/aligner` against a hidden dataset of much larger sequence pairs to verify the analytical correctness of your dynamic programming implementation. Your program must correctly compute the exact maximum alignment score for every pair.