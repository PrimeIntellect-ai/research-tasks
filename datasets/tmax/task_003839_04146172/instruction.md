You are a bioinformatics analyst responsible for building an automated quality-control pipeline for primer sequences. We have received a new batch of candidate primers, but they contain a mix of valid sequences and contaminated or poorly designed ones.

Your task is to write a C++ classifier that filters out the bad primers based on specific lab constraints. The lead scientist left a voice memo detailing the exact design constraints for this assay, which has been saved at `/app/lab_notes.wav`.

**Step 1: Recover the Experimental Constraints**
Transcribe or listen to `/app/lab_notes.wav`. The audio contains critical parameters regarding:
1. The acceptable range for the melting temperature ($T_m$). Use the standard Wallace rule for calculation: $T_m = 2(A+T) + 4(G+C)$.
2. The maximum allowed length of a homopolymer run (consecutive identical nucleotides).

**Step 2: Build the Classifier (Adversarial Corpus Filter)**
Write a C++ program at `/home/user/primer_filter.cpp` and compile it to `/home/user/primer_filter`.
- The program must take a single command-line argument: the path to a FASTA file containing a single primer sequence.
- It must read the sequence (ignoring the `>header` line and any whitespace/newlines).
- It must calculate the Wallace $T_m$, check the homopolymer lengths, and ensure the GC-content is between 40% and 60% (inclusive).
- **Output:** The program must exit with status code `0` if the sequence satisfies ALL constraints (accept). It must exit with status code `1` if the sequence fails ANY constraint (reject).

You must test your classifier against the corpora located at:
- `/app/corpus/clean/`: Contains FASTA files of correctly designed primers.
- `/app/corpus/evil/`: Contains FASTA files of primers that violate one or more constraints (wrong $T_m$, long homopolymers, or extreme GC distributions).
Your tool must accept 100% of the files in the `clean` directory and reject 100% of the files in the `evil` directory.

**Step 3: Density Estimation Visualization**
Once your filter is working, run it over the `clean` corpus. Collect the precise GC content percentages of all the accepted sequences.
Write a script (or extend your C++ program) to generate an SVG histogram at `/home/user/gc_density.svg` visualizing the GC density distribution of the clean corpus. The plot does not need axes or labels, but must visually represent the binning of GC percentages.