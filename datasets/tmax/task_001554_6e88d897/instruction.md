You are acting as a bioinformatics analyst. We are studying the spectral properties of nucleotide sequences using a custom numerical filter, but our lab only has the filter configuration stored as an image from an old presentation.

Your task consists of the following steps:
1.  **Setup Environment**: Install `tesseract-ocr` to extract text from images.
2.  **Extract Parameters**: Read the image located at `/app/motif_spec.png`. This image contains the specific integer mapping for each nucleotide (A, C, G, T) and a 1D convolution kernel (a sliding window array of weights).
3.  **Implement the Filter**: Write a Bash script at `/home/user/process_seq.sh`.
    *   The script must accept a single DNA sequence string as its first command-line argument (e.g., `bash /home/user/process_seq.sh ATCGGATC`).
    *   It should convert the sequence into a 1D array of integers based on the nucleotide mapping extracted from the image. Any unrecognized character (like 'N') should be mapped to the value `0`.
    *   It must then apply the convolution kernel (from left to right) over the numeric array. For a sequence of length $L$ and a kernel of length $K$, you will compute $L - K + 1$ values.
    *   The convolution operation for a window starting at index $i$ is: $\sum_{j=0}^{K-1} (\text{value}[i+j] \times \text{kernel}[j])$.
    *   The script must output the resulting filtered integers as a single space-separated line to standard output.

Make sure your script is robust and strictly uses Bash. Do not use external scripting languages like Python or Perl for the final `process_seq.sh` script, though standard Unix utilities (like `awk`, `sed`, `grep` if needed, though pure Bash arrays are recommended) are allowed. Make the script executable.