You are a bioinformatics analyst working on a highly reproducible computation pipeline for identifying viable sequence targets for an upcoming genetic study. Your system contains a set of candidate DNA sequences, some of which are valid ("clean") and some of which contain adversarial artifacts or fail thermodynamic/structural requirements ("evil"). 

Your first task is to extract the sequence design parameters from an old laboratory note that was scanned and saved as an image. The image is located at `/app/lab_specs.png`. You will need to use an OCR tool (like `tesseract`, which is preinstalled) to read the constraints. The image contains three critical pieces of information:
1. A required DNA motif that must be present in all valid sequences.
2. A MIN_GC percentage.
3. A MAX_GC percentage.

Once you have extracted these parameters, you must write a Bash script acting as a sequence classifier at `/home/user/analyze_primer.sh`. 

This script must be executable and follow these exact specifications:
- It must accept a single argument: the path to a FASTA format file.
- It must read the sequence from the FASTA file (ignoring the header line starting with `>`).
- It must calculate the GC content (percentage of G and C nucleotides out of the total A, T, G, C nucleotides).
- It must check if the required DNA motif (extracted from the image) is present anywhere in the sequence.
- **Exit Code 0 (Clean):** The script must exit with 0 if the sequence CONTAINS the required motif AND its GC content falls STRICTLY INCLUSIVELY within the [MIN_GC, MAX_GC] range.
- **Exit Code 1 (Evil/Reject):** The script must exit with 1 if the sequence is missing the motif OR its GC content is strictly less than MIN_GC OR strictly greater than MAX_GC.

You have been provided with two directories of `.fasta` files to test your script:
- `/app/corpus/clean/` : Contains sequences that perfectly adhere to the rules. Your script must exit 0 for all of these.
- `/app/corpus/evil/` : Contains sequences that violate at least one of the rules. Your script must exit 1 for all of these.

You may use standard Linux utilities (e.g., `grep`, `awk`, `bc`, `sed`) within your Bash script. Make sure your script is robust against multi-line FASTA sequences (you should concatenate sequence lines before analyzing them).

Once your script perfectly separates the clean corpus from the evil corpus, your task is complete. The automated test will invoke your script against a held-out set of clean and evil sequences using the exact same parameters from the image.