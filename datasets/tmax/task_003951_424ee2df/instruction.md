You are an ML engineer preparing a training dataset of biological sequences and their numerical stability scores for a sequence generation model.

Your task is to implement a high-performance C++ data preparation pipeline that processes target DNA sequences, extracts candidate primers, and scores them based on a custom numerical stability metric. The parameters for this metric were provided by the bio-informatics team in an image snippet.

**Step 1: Extract Scoring Parameters**
You have been given an image containing the scoring coefficients at `/app/scoring_params.png`. Use an OCR tool (like `tesseract`, which you may need to install or use via CLI/Python) to extract the three coefficients: `alpha`, `beta`, and `gamma`.

**Step 2: Process FASTA and Compute Scores in C++**
Write a C++ program (e.g., `prepare_data.cpp`) to do the following:
1. Parse the FASTA file located at `/home/user/data/targets.fasta`.
2. For each sequence, extract the first 20 bases. This is the "candidate primer".
3. Calculate the following for the 20-bp candidate primer:
   - `GC_content`: The fraction of G and C bases (between 0.0 and 1.0).
   - `Tm` (Melting Temperature): Calculated as `4 * (G + C count) + 2 * (A + T count)`.
   - `Homopolymer_Penalty`: The length of the longest contiguous stretch of identical bases in the 20-bp sequence.
4. Calculate the Numerical Stability Score using `double` precision:
   `Score = (alpha * GC_content) + (beta * (Tm / 100.0)) - (gamma * Homopolymer_Penalty)`
   *(Use the coefficients you extracted from the image).*

**Step 3: Output**
Your C++ program must output a CSV file to `/home/user/output/primer_scores.csv`. 
The CSV must have the following header and format:
`SequenceID,Primer20,Score`
(e.g., `seq1,ATGCATGCATGCATGCATGC,1.234567`)
Ensure the score is printed to 6 decimal places.

Compile and run your C++ code to generate the final output file.