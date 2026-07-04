You are acting as a bioinformatics analyst. We are currently developing a pipeline to filter out artifactual DNA sequence reads from our sequencer. Some reads contain artificial periodic noise (a specific synthetic adapter or motor artifact) that manifests as strong abnormal frequency peaks in the spectral domain.

Your task is to write a standalone C++ command-line tool, `seq_filter`, that reads a genomic sequence (consisting of A, C, G, T) and determines whether it is "clean" or "artifactual" using Fourier analysis. 

First, look at the image provided at `/app/filter_specs.png`. This image contains a handwritten note from the lead scientist detailing the exact spectral analysis method to use (e.g., how to numerically encode the DNA string, which frequency ranges to inspect, and the threshold ratio for the artifact peak). You must extract these parameters.

Once you have the specifications, implement the `seq_filter` tool in C++. The tool must accept a single string of DNA as a command-line argument or from standard input, and output exactly one word to standard output: either `ACCEPT` or `REJECT`.

We have two directories of test sequences:
- `/app/reads/clean/`: Contains hundreds of raw `.txt` files, each with a valid, biological DNA sequence.
- `/app/reads/artifact/`: Contains hundreds of `.txt` files, each corrupted by the periodic sequencer artifact.

You must compile your program to `/home/user/seq_filter`. Your program must be able to classify the sequences. Our automated verifier will run your compiled executable against the unseen evaluation directories (structured identically to the provided test directories) and expects `ACCEPT` for all clean sequences and `REJECT` for all artifactual sequences. 

Write the C++ code, compile it using standard `g++` (you may use standard libraries, or include basic mathematical implementations as needed), and verify it against the provided datasets.