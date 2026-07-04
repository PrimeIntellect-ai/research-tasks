You are acting as a bioinformatics software developer. You need to write a C program to perform a mathematical analysis of DNA sequence composition and generate a visual heatmap of their similarity. 

We have a set of DNA sequences in `/home/user/sequences.txt`. Each line contains a single sequence consisting of the characters A, C, G, and T.

Your task is to write a C program that:
1. Reads `/home/user/sequences.txt`.
2. For each sequence, computes the frequency of all 16 possible overlapping 2-mers (di-nucleotides: AA, AC, AG, AT, CA, CC, etc.).
3. Calculates the pairwise Manhattan distance between every pair of sequences based on their 16-dimensional 2-mer frequency vectors.
4. Outputs the resulting $N \times N$ distance matrix to a CSV file at `/home/user/matrix.csv` (where N is the number of sequences). The CSV must not have a header, and values should be comma-separated integers.
5. Generates a Portable Gray Map (PGM) image file at `/home/user/heatmap.pgm` to visualize the distance matrix. 
   - The PGM must be in ASCII format (magic number `P2`).
   - The width and height must match the number of sequences $N$.
   - The maximum gray value must be 255.
   - You must scale the distances so that the maximum distance present in the entire matrix maps to exactly 255, and a distance of 0 maps to 0. Use integer division for scaling: `pixel_value = (distance * 255) / max_distance`. (Assume the maximum distance is greater than 0).

You should compile your C program to `/home/user/analyze` using `gcc` and execute it to produce the two output files. Ensure all operations and file creations happen within `/home/user`.