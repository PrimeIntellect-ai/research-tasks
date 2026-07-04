You are a Machine Learning Engineer preparing a specialized genomic dataset for a new generative model. Before creating the final training tensors, you need to extract specific DNA regions from a raw dataset and analyze their statistical properties to ensure they don't exhibit severe distributional shifts.

You have been provided with a FASTA file containing raw DNA sequences at `/home/user/raw_sequences.fasta`.

Write a Go program at `/home/user/prepare_data.go` that performs the following steps using only the Go standard library:

1. **Sequence Extraction (Primer Alignment simulation)**
   Parse `/home/user/raw_sequences.fasta`. For each sequence, search for the first occurrence of the forward motif `GACCAT` and the first occurrence of the reverse motif `TGTCGA` that appears *after* the forward motif. 
   Extract the subsequence strictly *between* these two motifs. If a sequence does not contain both motifs in the correct order, or if the extracted subsequence has a length of 0, ignore it.

2. **GC Content Calculation**
   For each successfully extracted subsequence, calculate its GC content. The GC content is defined as the number of 'G' and 'C' bases divided by the total number of bases in the extracted subsequence.

3. **Bootstrap Confidence Interval**
   To estimate the population mean GC content for our ML priors, compute a 95% bootstrap confidence interval for the mean GC content of the extracted subsequences.
   - Use exactly `B = 10000` bootstrap resamples.
   - To ensure reproducibility, initialize your random number generator exactly like this: `rng := rand.New(rand.NewSource(42))` (using `math/rand`). 
   - Sample with replacement from your calculated GC contents.
   - Use the percentile method to find the 95% CI (find the 2.5th percentile and the 97.5th percentile of the bootstrap means). For calculating percentiles, simply sort the bootstrap means and pick the indices `int(0.025 * B)` and `int(0.975 * B)`.

4. **Output**
   Calculate the sample mean of the GC contents, and output the statistics as a JSON file at `/home/user/ml_data_stats.json` with the following exact structure:
   ```json
   {
     "extracted_count": <integer>,
     "mean_gc": <float>,
     "ci_lower": <float>,
     "ci_upper": <float>
   }
   ```
   (Format floats to 4 decimal places if you wish, but standard float serialization is fine as long as it's accurate).

Run your Go program to produce the JSON file.