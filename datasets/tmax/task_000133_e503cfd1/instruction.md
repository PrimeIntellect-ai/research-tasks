You are acting as a performance engineer and bioinformatics developer. We have an audio transmission containing a target DNA sequence, and we need to rapidly filter a massive library of candidate primers to find suitable matches using Go.

Your objectives:
1. **Extract the Target Sequence**: The file `/app/audio/target.wav` contains a target DNA sequence encoded in standard International Morse Code (audio tones). Decode this audio to recover the string of 'A', 'C', 'G', and 'T' characters. This is your `<target_sequence>`.
2. **Build a Primer Classifier in Go**: Create a Go program at `/home/user/classifier.go` and compile it to `/home/user/classifier`. 
   The CLI invocation must be:
   `/home/user/classifier <target_sequence> <input_directory> <output_directory>`
   
   For every `.txt` file in `<input_directory>` (each containing a single primer string), your Go program must evaluate it and copy the file to `<output_directory>` ONLY IF it passes ALL the following tests:
   - **Alignment**: The primer must exist as an exact contiguous substring within the `<target_sequence>`.
   - **GC Content**: The primer must have a GC content between 40% and 60% inclusive.
   - **Numerical Stability & Distribution**: Calculate the Kullback-Leibler (KL) divergence of the dinucleotide (2-mer) frequencies of the primer relative to the `<target_sequence>`. 
     - You must implement Laplace smoothing (add 1 to all counts before calculating probabilities) to ensure numerical stability and prevent NaNs from zero counts.
     - The smoothed KL divergence $D_{KL}(P_{primer} || P_{target})$ must be less than 0.5.
   - **Parallelism**: The program must process the files concurrently using goroutines to ensure high performance profiling.

Write the code, compile it, and ensure it correctly filters the corpora.