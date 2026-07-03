You are a bioinformatics analyst working with a newly recovered deep-sea dataset. We have received a batch of FASTA files containing genetic sequences, but we suspect our transmission system corrupted some of them, introducing anomalies that cause our downstream Monte Carlo simulation and numerical stability tests (which are run via a Jupyter notebook pipeline) to crash or produce invalid floating-point operations.

We have a set of reference sequences in `/app/corpus/clean/` (which are known to be perfectly valid and stable) and a set of corrupted, unstable sequences in `/app/corpus/evil/`. 

To understand the exact classification criteria for what constitutes a "clean" versus an "evil" sequence, you need to listen to the dictation left by the lead scientist. The audio recording of their instructions is located at `/app/instructions.wav`. You will need to transcribe or listen to this audio file to understand the specific rules.

Your task is to write a Bash shell script located at `/home/user/filter.sh` that acts as a classifier. 
It must:
1. Accept a single argument: the path to a FASTA file.
2. Read the FASTA file and evaluate it against the rules dictated in the audio file.
3. Exit with status code `0` if the sequence is "clean".
4. Exit with status code `1` if the sequence is "evil".

You may use any standard Linux text processing tools (like `awk`, `grep`, `sed`, `python3`) inside your Bash script to implement the logic, but the main entry point must be the `filter.sh` Bash script.

Requirements:
- Your script must have executable permissions (`chmod +x /home/user/filter.sh`).
- Do not modify the files in the corpus.
- Ensure your script correctly handles standard FASTA formats (header starting with `>`, followed by sequence lines).