I have a set of simulated DNA spectroscopy readings, but my data pipeline is producing non-reproducible spectral centroids due to floating-point reduction order issues when accumulating sums from unordered mappings. 

I need you to process the data to find a specific sample and calculate its spectral centroid deterministically.

Here is what you need to do:
1. Search the FASTA file at `/home/user/sequences.fasta` to find the sequence ID that contains the exact primer motif: `GGTACCTAG`.
2. Find the corresponding spectral data for that sequence ID in `/home/user/spectra.txt`. The format of this file is `SequenceID|freq1:intensity1,freq2:intensity2,...` where the frequency-intensity pairs are unordered.
3. Reshape and process this data to calculate the spectral centroid: $\frac{\sum (frequency_i \cdot intensity_i)}{\sum intensity_i}$.
4. **Critical**: To guarantee deterministic floating-point results, your code (which can be Python, R, or Bash/Awk) MUST sort the frequency-intensity pairs by frequency (from lowest to highest) *before* accumulating the running sums for the numerator and denominator.
5. Output the result to `/home/user/result.txt` in the exact format: `SequenceID,CentroidValue` (round the centroid to exactly 6 decimal places).

Write and execute the necessary scripts/commands to accomplish this.