I am a data scientist trying to perform matrix factorization on some genetic sequence data to fit a clustering model. Unfortunately, my factorization algorithm is failing because the input matrix is near-singular—this is happening because there are several identical sequences in the observational data, creating linear dependencies.

I need you to write a C program that preprocesses this data to fix the singularity issue. 

Here is what you need to do:
1. Parse the FASTA file located at `/home/user/raw_sequences.fasta`. (You can assume all sequences are of the exact same length, and the sequence data for each record is entirely on a single line).
2. Convert the sequences into a numeric matrix of `double` precision values. Use the following mapping for the nucleotide bases (ignore case, assume only these 4 bases exist):
   - 'A' or 'a' = 1.0
   - 'C' or 'c' = 2.0
   - 'G' or 'g' = 3.0
   - 'T' or 't' = 4.0
3. Reshape the observational data by identifying and keeping only the unique rows (sequences). When a duplicate is found, keep the first occurrence and discard the subsequent identical sequences.
4. Save the deduplicated $M \times N$ matrix (where $M$ is the number of unique sequences and $N$ is the sequence length) to an HDF5 file at `/home/user/cleaned_data.h5`. The matrix must be saved as an HDF5 dataset named exactly `/unique_matrix` using the `H5T_NATIVE_DOUBLE` datatype.

You must write the solution in C (e.g., save it as `/home/user/preprocess.c`), compile it, and run it successfully so that `/home/user/cleaned_data.h5` is produced. 

Ensure your C program is self-contained. The system will have standard C libraries and the HDF5 C development headers installed.