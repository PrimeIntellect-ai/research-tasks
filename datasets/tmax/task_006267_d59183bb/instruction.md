As a bioinformatics analyst, you are tasked with identifying the most closely related pair of DNA sequences in a large dataset, which could indicate a recent duplication event. 

You have been provided with a dataset of 10,000 DNA sequences, each 50 bases long, located at `/home/user/dataset.txt`. 

Your objective is to write a Rust program that computes the all-pairs Hamming distance between these sequences and finds the pair with the minimum distance. Because the dataset is large, calculating the distance matrix requires $10,000 \times 9,999 / 2 \approx 50,000,000$ comparisons. You must use parallel computing to speed up the process.

Please complete the following steps:
1. Initialize a new Rust project named `seq_match` in `/home/user/seq_match`.
2. Add the `rayon` crate to your project to enable parallelization.
3. Write a Rust program that reads `/home/user/dataset.txt`, computes the Hamming distances between all unique pairs of sequences in parallel, and finds the pair with the absolute minimum distance.
4. If there are multiple pairs with the same minimum distance, pick the one where the first index is smallest, and then the second index is smallest.
5. Output the result to a file at `/home/user/result.txt` in the exact format: `index1,index2,distance` (using 0-based indices, where `index1 < index2`).

Compile your Rust project in release mode and run it to produce the `result.txt` file.