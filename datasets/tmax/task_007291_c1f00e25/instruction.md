You are a bioinformatics analyst building a reproducible computation pipeline. I have a dataset of raw, uncleaned DNA sequences in `/home/user/data/reads.csv`. 

I need you to create a Rust project to reshape this observational data, estimate the density/distribution of its GC content (Guanine-Cytosine fraction), and output the results.

Please do the following:
1. Create a new Rust project (using Cargo) named `gc_estimator` in `/home/user/`.
2. Write a Rust program in this project that reads `/home/user/data/reads.csv`. The CSV has two columns: `id` and `sequence`.
3. The program must filter out any sequences that contain invalid characters. A sequence is ONLY valid if it contains exclusively the characters `A`, `C`, `G`, and `T` (case-insensitive).
4. For each valid sequence, calculate its GC fraction (the total count of `G` and `C` characters divided by the sequence length).
5. Compute the population mean and the population standard deviation of the GC fractions across all valid sequences.
6. Compile and run your Rust program so that it writes a JSON file to `/home/user/gc_distribution.json` with the exact following format:
`{"mean": <float>, "std_dev": <float>}`

Make sure to build and run the pipeline successfully. Do not round the float outputs; leave them at the default f64 precision.