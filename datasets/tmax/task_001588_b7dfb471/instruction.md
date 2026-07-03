You are a bioinformatics analyst tasked with finding periodicities in a large uncharacterized synthetic genomic sequence. You need to map the DNA sequence to numerical values, decompose the genome into smaller chunks (windows), compute the power spectrum for each chunk using Fast Fourier Transforms (FFT), and average them. To speed up the process, you should implement parallel computing (e.g., using Python's `multiprocessing` or `mpi4py`).

Here is what you need to do:
1. **Extract Parameters:** You have been provided an image at `/app/note.png`. This image contains a handwritten note specifying the numerical mapping for the nucleotides (A, C, G, T) and the `Window` size (an integer) to be used for domain decomposition. Read these parameters (you can use `tesseract` or any OCR tool).
2. **Process the Genome:** Read the DNA sequence from `/app/genome.txt` (a single long string of characters).
3. **Domain Decomposition:** Split the genome into sequential, non-overlapping windows of the size specified in the image. Discard any remaining nucleotides at the end that do not form a complete window.
4. **Numerical Mapping:** Convert the sequence in each window into an array of floats using the mapping rules extracted from the image.
5. **Spectral Analysis:** For each numerical window, compute the power spectrum. The power spectrum is defined here as the squared magnitude of the 1D Discrete Fourier Transform (i.e., `|FFT(window)|^2`). Do not normalize the FFT.
6. **Parallelize:** Distribute the window processing across multiple parallel workers.
7. **Average and Save:** Calculate the element-wise average of the power spectra across all valid windows. Save the resulting 1D NumPy array (which should have a length equal to the window size) to `/home/user/avg_spectrum.npy`.

Ensure your Python environment is set up correctly (e.g., installing `numpy`, `pytesseract`) to perform this analysis.