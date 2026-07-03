You are a bioinformatics analyst working with targeted DNA sequencing data. You need to build a reproducible pipeline in C to process a FASTA file containing raw sequencing reads, extract specific amplified regions (amplicons) based on known primer sequences, and reshape the extracted data into a summary CSV for downstream statistical analysis.

Your task is to:

1. Write a C program named `/home/user/extractor.c`. 
   - It should take two command-line arguments: an input FASTA file path and an output CSV file path.
   - It must parse the input FASTA file. Sequences may be on a single line after the sequence identifier line (which starts with `>`).
   - For each sequence, search for the Forward Primer: `GACCTACA` and the Reverse Primer: `TGTTGCAG`. 
   - If BOTH primers are found in the sequence (with the forward primer appearing before the reverse primer), extract the nucleotide sequence *strictly between* the end of the forward primer and the start of the reverse primer.
   - For the extracted sequence (the amplicon), calculate its length and its GC content (the proportion of 'G' and 'C' bases out of the total length of the amplicon).
   - Skip any reads where the primers are not found or are in the wrong order.
   - Write the results to the output CSV file with the following exact header: `SeqID,AmpliconLength,GC_Content`.
   - The `SeqID` should omit the leading `>`.
   - `GC_Content` should be a float rounded to exactly two decimal places (e.g., `0.67`).

2. Create a `/home/user/Makefile` that compiles `extractor.c` into an executable named `extractor` using `gcc` with standard warnings enabled (`-Wall -O2`).

3. Create a bash script `/home/user/run_pipeline.sh` that makes the computation reproducible. The script should:
   - Invoke `make` to build the executable.
   - Run the compiled `extractor` program, using `/home/user/reads.fasta` as the input and generating `/home/user/amplicon_data.csv` as the output.
   - Ensure the script has executable permissions.

The raw sequence data is already located at `/home/user/reads.fasta`. Complete these steps so that running `./run_pipeline.sh` successfully produces the correctly formatted `amplicon_data.csv`.