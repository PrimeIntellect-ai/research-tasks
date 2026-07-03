As an artifact manager for our organization's binary repository, you need to write a classifier script to filter incoming artifacts. We have been receiving gzipped ELF binaries where some have been injected with malicious payloads within a custom `.note.artifact` section.

Write a Python script at `/home/user/sanitizer.py` that takes a single command-line argument: the path to a gzipped ELF file (`.elf.gz`).

Your script must:
1. Decompress the gzipped stream in memory or to a temporary file.
2. Extract the raw binary contents of the `.note.artifact` section from the ELF.
3. Determine if the artifact is clean or evil. To do this, you have access to a stripped binary oracle at `/app/validator_oracle`. You must figure out how to interact with this oracle to classify the extracted section (the oracle accepts the raw section data via standard input).
4. Exit with code `0` if the artifact is clean.
5. Exit with code `1` if the artifact is evil (malicious).

We have provided a small sample of files in `/home/user/sample_corpus/clean/` and `/home/user/sample_corpus/evil/` for you to test your logic. The final automated test will use a hidden adversarial corpus to grade your script. 

Ensure your script is robust and executable via `python3 /home/user/sanitizer.py <file.gz>`.