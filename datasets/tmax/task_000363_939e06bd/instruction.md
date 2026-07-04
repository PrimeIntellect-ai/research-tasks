As a data scientist, you are debugging a bioinformatics MCMC pipeline that processes FASTA sequences to estimate posterior probabilities of certain statistical hypotheses.

Part 1: Pipeline Configuration
The pipeline consists of a Redis instance, a FASTA data producer, and an MCMC statistical consumer. They are managed by the script `/app/services/start.sh`. Currently, the pipeline fails to run because the producer and consumer are configured with incorrect Redis ports. 
- The configuration file is located at `/app/services/config.json`.
- Redis is bound to port 6379.
- Edit `/app/services/config.json` to configure both the producer and consumer to use port 6379.
- You can test the pipeline by running `/app/services/start.sh` and ensuring it completes successfully and writes its results to `/home/user/pipeline_success.log`.

Part 2: High-Performance FASTA Posterior Evaluator
The Python consumer is too slow, so we are replacing the core evaluation loop with a C program.
Write a C program at `/home/user/fasta_parser.c` and compile it to `/home/user/fasta_parser` (using `gcc -O3`).
This program must read a modified FASTA stream from `stdin` and print the evaluated posterior probabilities to `stdout`.

Input Format:
- Header lines start with `>` followed by a sequence ID (up to 50 characters, no spaces), a space, and `prior=` followed by a floating-point number.
  Example: `>sequence_A prior=0.65`
- Sequence lines follow the header and consist of characters. You should only count 'A', 'C', 'G', and 'T' (case-sensitive). Ignore any other characters, including spaces and newlines.
- A sequence ends when a new header line (starting with `>`) is encountered or at the end of the file.

Computation:
- For each sequence, compute the GC ratio: `(count of G + count of C) / (total valid characters A, C, G, T)`.
- If there are no valid characters, the GC ratio is `0.0`.
- Compute the posterior: `posterior = GC ratio * prior`.

Output Format:
For each sequence, print exactly one line to `stdout`:
`[sequence ID] posterior=[posterior formatted to 4 decimal places]`
Example:
`sequence_A posterior=0.3250`

Ensure your C program robustly handles varying line lengths and multiple sequences. Do not crash on missing sequence lines or zero-length sequences.