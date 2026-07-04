I am a bioinformatics analyst working on a custom primer design pipeline. We have a legacy proprietary tool located at `/app/primer_oracle` that evaluates the stability of a given DNA sequence. The tool takes a single DNA sequence (containing A, C, G, T) as a command-line argument and prints a floating-point score to standard output. 

Unfortunately, we lost the source code for this tool. It is a stripped binary, and we need to port its logic to a portable Bash script so we can integrate it into our new distributed workflow without dealing with binary compatibility issues across different architectures.

Your task is to:
1. Analyze the `/app/primer_oracle` executable to determine the mathematical model it uses to compute the sequence score. It calculates a specific ratio based on the sequence composition, and then solves a non-linear equation using an iterative numerical method (specifically 10 iterations of Newton-Raphson) to find a scaling factor, which is then multiplied by the sequence length.
2. Write a Bash script at `/home/user/my_primer_oracle.sh` that exactly replicates the behavior and output of the legacy binary. The script should take a single sequence as its first argument and output the score to 6 decimal places. You may use standard Unix tools like `awk` or `bc` within your Bash script.
3. Ensure your script handles inputs exactly like the oracle.

Make sure the script is executable. I need the new script to be a drop-in replacement that produces bit-exact equivalent outputs for any given valid DNA sequence of length 10 to 50.