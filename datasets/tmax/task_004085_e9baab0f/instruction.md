I'm working on a protein dynamics simulation pipeline. Our core numerical integrator, which is a legacy compiled application (`/app/run_sim`), often diverges and crashes due to wrong step-size adaptation when it encounters certain "anomalous" sequences in FASTA files. I don't have the source code for the integrator; it's a stripped binary. 

Your task is to build a robust Bash-based data sanitization pipeline to filter out anomalous observational FASTA sequences before they reach the integrator. You will write a script, `/home/user/sanitize_fasta.sh`, that takes an input FASTA file path and an output FASTA file path as arguments, and writes only the "clean" sequences to the output.

A sequence is considered "anomalous" (and should be rejected) if:
1. The sequence contains any characters other than standard amino acids (A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y).
2. The sequence length is less than 20 or greater than 500 amino acids.
3. The GC-equivalent content (for this context, the combined frequency of G, C, P, and W) exceeds 60% of the sequence length.

I have provided two directories containing observational FASTA data:
- `/home/user/data/clean/`: Contains 50 valid FASTA files.
- `/home/user/data/evil/`: Contains 50 anomalous FASTA files that cause the integrator to fail.

Requirements:
1. Write `/home/user/sanitize_fasta.sh`. It must accept exactly two arguments: `<input_fasta>` `<output_fasta>`.
2. The script must parse the input FASTA file, evaluate the sequences according to the rules above, and append the passing sequence(s) and their headers to `<output_fasta>`.
3. You must use Bash (awk/sed/grep are allowed, but no Python/Perl scripts).
4. Run your script against all files in `/home/user/data/clean/` and `/home/user/data/evil/` to ensure it preserves 100% of the clean sequences and rejects 100% of the evil ones. If a file contains only anomalous sequences, the output file should be empty.

Create the script at `/home/user/sanitize_fasta.sh` and ensure it is executable.