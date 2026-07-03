You are an AI assistant helping a computational biology researcher with a simulation regression pipeline.

The researcher has a set of FASTA files in `/home/user/data/`. They also have a bash-based simulation script located at `/home/user/bin/run_sim.sh`. Recently, the simulation has been failing to converge for certain "near-singular" sequences (specifically those with certain rigid motifs), resulting in exploding energy values.

Your task is to write a reproducible bash script `/home/user/check_convergence.sh` that automates regression testing for this convergence issue.

The script must do the following:
1. Iterate over all `.fasta` files in `/home/user/data/` in alphabetical order.
2. For each file, parse the FIRST protein sequence. A FASTA file has a header line starting with `>` followed by sequence lines. You must extract just the sequence characters (concatenating them if they span multiple lines) and ignore the header.
3. Pass the parsed sequence string as the single argument to the simulation script: `/home/user/bin/run_sim.sh "<sequence_string>"`
4. Parse the output of `run_sim.sh`. The script outputs iterative energy values line-by-line in the format: `Step X: <value>`.
5. Check for convergence divergence. We define divergence as the `<value>` in the *final* Step being greater than `1000`.
6. If the simulation diverges, append the base filename (e.g., `protein_B.fasta`) to a log file located at `/home/user/diverged_sims.log`.

Make sure `/home/user/check_convergence.sh` is executable and run it so that `/home/user/diverged_sims.log` is generated. 

Do not use python, perl, or other scripting languages. Rely strictly on bash, awk, sed, grep, and coreutils. Ensure the output log only contains the filenames of the diverged simulations, one per line.