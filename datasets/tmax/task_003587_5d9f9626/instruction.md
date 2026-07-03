You are an AI assistant helping a bioinformatics analyst process DNA sequences. 

We have a collection of DNA sequences in FASTA format. Some of these sequences are "clean" (normal) and some are "evil" (anomalous, perhaps artifacts of sequencing errors or specific genomic islands). 

Your task is to build a high-performance filter in Rust that classifies these sequences. 

1. **Extract Parameters**: We have a scanned image of lab notes at `/app/lab_notes.png`. Use OCR (e.g., `tesseract`) to read the text in this image. It contains a critical parameter: `GC_MAX_THRESHOLD`.
2. **Build the Classifier**: Create a Rust project at `/home/user/seq_filter`. The tool should compile to an executable.
   - It must take a single argument: the path to a FASTA file.
   - It should calculate the exact GC content (number of 'G' and 'C' bases divided by the total number of 'A', 'C', 'G', 'T' bases, ignoring case and whitespace/newlines).
   - If the GC content is strictly greater than the `GC_MAX_THRESHOLD` extracted from the image, the sequence is considered "evil".
   - The program must exit with status code `0` if the sequence is "clean" (GC content <= threshold) and exit with status code `1` if it is "evil" (GC content > threshold).
3. **Parallel Processing**: Ensure your Rust code uses the `rayon` crate to process chunks of the sequence in parallel if it's long, although simple counting is acceptable as long as it correctly classifies the files.
4. **Validation**: We have provided two directories for you to test your tool locally (though the automated test will use its own hidden datasets):
   - `/home/user/sample_clean/`: Contains examples of clean FASTA files.
   - `/home/user/sample_evil/`: Contains examples of evil FASTA files.

Please build the Rust tool and ensure it can be run via:
`cargo run --release -- <path_to_fasta>`
or by directly calling the binary in `target/release/seq_filter`.

Your solution will be tested against a hidden "clean" corpus and a hidden "evil" corpus. It must perfectly separate them based on the rules above.