You are a bioinformatics analyst working on a reproducible computation pipeline. We are attempting to recreate a legacy sequence stability scoring algorithm. 

Unfortunately, the original source code is lost, and the only documentation we have is an old lab voice memo located at `/app/lab_notes.wav`. This audio file describes the exact algorithm and the specific numerical weights assigned to each nucleotide (A, C, G, T) for calculating the sequence stability score.

Your task is to:
1. Listen to or transcribe the audio file `/app/lab_notes.wav` to extract the nucleotide weights and the scoring formula.
2. Write a C program named `bio_scorer.c` in `/home/user/` that implements this scoring algorithm.
3. Compile it to an executable named `/home/user/bio_scorer`.

The executable must take exactly one command-line argument: a string representing the DNA sequence (containing only the characters A, C, G, T). It should output the calculated integer stability score to standard output, followed by a newline.

Your implementation must be bit-exact equivalent to the legacy binary. We will verify your program by testing it against a hidden reference implementation with a large number of randomly generated DNA sequences. Ensure your code handles strings up to 1024 characters long and avoids integer overflow by adhering strictly to the modulo operations described in the audio.