You are a machine learning engineer preparing training data from bioinformatics signals. You need to write a feature extraction tool that computes a simulated spectroscopy signal from DNA sequences.

1. There is an image file located at `/app/amplitude.png` that contains a single handwritten integer. This integer represents the `Amplitude` of our signal. Extract this number.
2. Write a Go program at `/home/user/encoder.go` and compile it to an executable at `/home/user/encoder`.
3. The executable must read standard input until EOF. The input will resemble a simplified FASTA format mixed with noise.
4. Your program must process the input as follows:
   - Process the input line by line.
   - Strictly ignore any line where the very first character is `>` (these are headers).
   - For all other lines, analyze the sequence to find valid DNA bases. A valid base is defined as the characters `A`, `C`, `G`, or `T` (case-insensitive). Ignore any other characters (including spaces, punctuation, or other letters like `N`).
   - Keep a running count of the total number of valid DNA bases, and the number of strong bases (`G` and `C`, case-insensitive).
5. After reading all input, calculate the GC-ratio: `(count of G + count of C) / (total valid bases)`.
6. Calculate the simulated signal intensity using the formula: `Amplitude * sin(GC_ratio * Pi)`. (Use standard library `math.Pi`).
7. Print this single floating-point result to standard output, formatted to exactly 6 decimal places (e.g., `123.456789`), followed by a newline.
8. If the total number of valid bases across the entire input is 0, the program should output exactly `0.000000` followed by a newline.

Ensure your program is compiled to `/home/user/encoder` before you finish, as it will be tested automatically against many random inputs.