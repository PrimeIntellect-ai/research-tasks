You are assisting a bioinformatics researcher working on an anomaly detection system for synthetic DNA sequences. 

The researcher has left a voice memo detailing the exact parameters for an ODE-based anomaly detection model, located at `/app/lab_dictation.wav`. 

Your task is to:
1. Extract the audio transcript to retrieve the specific target primer sequence and the ODE decay constant. You may use standard tools (e.g., `ffmpeg` or Python speech recognition libraries) to retrieve this.
2. Write a C program named `detector.c` (and compile it to `/home/user/detector`) that takes a single file path as a command-line argument.
3. The program must parse the FASTA file at the given path.
4. For the DNA sequence in the FASTA file, simulate the following spatial ODE along the sequence index $x$ (from $x=0$ to $L-1$, where $L$ is sequence length).
   - Let $P(x)$ be the concentration of a synthetic protein, with $P(0) = 0.0$.
   - At each nucleotide index $x$, check if a perfect match of the **target primer sequence** (retrieved from the audio) STARTS at $x$. 
   - If a match starts at $x$, the local production rate $S(x) = 1.0$. Otherwise, $S(x) = 0.0$.
   - The ODE is: $dP/dx = S(x) - k \cdot P(x)$, where $k$ is the **decay constant** (retrieved from the audio).
   - Integrate this step-by-step using the Euler method with a step size of $\Delta x = 1$. (i.e., $P(x+1) = P(x) + S(x) - k \cdot P(x)$).
5. If at any point $P(x) > 1.5$, the sequence is classified as "anomalous" (evil). Otherwise, it is "safe" (clean).
6. The `detector` executable MUST return exit code `1` (reject) if the sequence is anomalous, and exit code `0` (accept) if it is safe.

Two directories of FASTA files are provided for you to test against:
- `/app/corpora/clean/` (contains only safe sequences)
- `/app/corpora/evil/` (contains synthetic sequences that trigger the anomaly threshold)

You must ensure that your `/home/user/detector` successfully accepts 100% of the clean corpus and rejects 100% of the evil corpus.