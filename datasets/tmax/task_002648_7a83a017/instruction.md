You are a bioinformatics analyst working on a new genomic sequence analysis tool. Your Principal Investigator (PI) left you an audio memo at `/app/memo.wav` detailing the parameters for a new algorithm.

Your task is to transcribe the audio memo to retrieve two parameters: the number of domains ($D$) and the number of bootstrap iterations ($B$). Then, write a C program that implements the algorithm.

Write your C code in `/home/user/analyze_seq.c` and compile it to an executable at `/home/user/analyze_seq`.

### Algorithm Specification
The program `/home/user/analyze_seq` must accept exactly one command-line argument: a DNA sequence string (containing only 'A', 'C', 'G', 'T').
It must perform the following:

1. **Domain Decomposition:** Divide the input sequence into $D$ equal-length contiguous sub-sequences (domains). If the length of the sequence $N$ is not perfectly divisible by $D$, the first $D-1$ domains should have length $\lfloor N/D \rfloor$, and the final domain should contain all the remaining characters.
2. **Bootstrap Resampling:** For each domain (processed in order from $0$ to $D-1$), perform $B$ bootstrap iterations (from $0$ to $B-1$). 
   - In each iteration, generate a resampled domain of the same length $L$ by sampling characters from the original domain *with replacement*.
   - To ensure reproducible results, you MUST use the following specific Linear Congruential Generator (LCG) for all random sampling:
     ```c
     uint32_t state = 1337; // Initial seed
     uint32_t next_rand() {
         state = (state * 1103515245 + 12345) & 0x7FFFFFFF;
         return state;
     }
     ```
   - For each character position (from $0$ to $L-1$) in the resampled sequence, pick the character from the original domain at index `next_rand() % L`. Do NOT reset the seed between domains or iterations; the LCG state should evolve continuously throughout the entire program execution.
3. **Confidence Intervals:** For each bootstrap iteration, calculate the GC-count (the total number of 'G' and 'C' characters in the resampled domain). Sort the $B$ GC-counts for each domain in ascending order. Calculate the 95% Bootstrap Confidence Interval by taking the 2.5th and 97.5th percentiles. 
   - Calculate indices as: `lower_idx = (int)(0.025 * B)` and `upper_idx = (int)(0.975 * B)`.
4. **Statistical Hypothesis Comparison & Mesh Refinement Flagging:** Calculate the width of the confidence interval for each domain (`count[upper_idx] - count[lower_idx]`).
   - Find the domain with the widest confidence interval, indicating the highest variance region that requires "mesh refinement".
   - If there is a tie, select the domain with the lowest index.
5. **Output:** Print the 0-based integer index of the domain that requires refinement to `stdout`, followed by a newline.

Install any audio processing or transcription tools you need to decode the PI's memo. The automated verifier will strictly test your compiled binary against thousands of random DNA sequences to ensure bit-exact logical equivalence with the reference implementation.