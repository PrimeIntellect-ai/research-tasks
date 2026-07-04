You are acting as a bioinformatics analyst. We are building a reproducible sequence processing pipeline. A downstream matrix factorization step is crashing because of near-singular input matrices, which are caused by highly degenerate/biased DNA sequences. 

Your task is to create a robust Bash script that acts as a sequence sanitizer.

1. First, check the image file located at `/app/threshold.png`. This contains the mathematical definition of the degeneracy threshold (a nonlinear equation you must solve) and the exact filtering rule based on nucleotide frequencies. You will need to extract this information (OCR tools like `tesseract` are available).
2. Write a Bash script at `/home/user/filter_fasta.sh` that takes a single FASTA file path as its first argument.
3. The script must read the FASTA file, calculate the overall proportions of A, C, G, and T (ignoring case and newlines, counting only A, C, G, T to find the total), and evaluate the mathematical rule found in the image.
4. The script must output exactly the word `ACCEPT` to standard output if the sequence passes the check, or `REJECT` if it violates the threshold. 

Your script will be tested against two sets of corpora: a "clean" dataset of normal sequences, and an "evil" dataset of degenerate sequences. It must strictly separate them based on the mathematical threshold extracted from the image. 

Ensure your script handles standard FASTA formats properly (skipping the header lines starting with `>`).