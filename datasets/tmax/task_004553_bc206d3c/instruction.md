You are an AI assistant helping a bioinformatics analyst debug a data pipeline.

Recently, our Monte Carlo sequence simulator experienced a "step-size divergence" bug during integration, leading to the generation of corrupted biological sequences. We need to filter our generated sequence datasets to remove these corrupted artifacts before they are used to build molecular graph models.

A colleague left a scanned note from their lab book explaining exactly how to identify the diverged sequences, but it was saved as an image file. The image is located at `/app/divergence_note.png`. 

Your task is to:
1. Extract the rejection criteria from the scanned note (you have `tesseract` installed for OCR). The note specifies a specific k-mer (a 4-letter sequence) and the maximum allowed occurrences of that k-mer in a single sequence before it is considered "diverged" (evil).
2. Write a Bash script located at `/home/user/detector.sh` that will act as a classifier for our sequences.
3. The script must take exactly one argument: the absolute path to a FASTA file.
4. The script must parse the sequence from the FASTA file (ignoring the header lines starting with `>`), evaluate it against the criteria extracted from the image, and output an exit code:
   - `exit 0` if the sequence is valid (clean) and should be preserved.
   - `exit 1` if the sequence is diverged (evil) based on the image's rule and should be rejected.

Make sure your script only relies on standard Bash tools (like `grep`, `awk`, `sed`, `tr`, etc.) and handles multi-line FASTA sequences correctly by concatenating sequence lines before counting.

Ensure your script is executable (`chmod +x /home/user/detector.sh`). You do not need to process entire directories yourself; our testing framework will call your script individually on thousands of reference datasets.