You are acting as a data scientist for a bioinformatics lab. We have a pipeline that predicts organism growth rates based on their genomic GC content. However, our current naive implementation fails or produces `NaN` values due to some corrupted reads in our latest sequencing run (which act as near-singular or invalid inputs for our curve fitting).

Your task is to write a robust, concurrent Go program that parses a FASTA file, calculates the GC content for each valid sequence, matches it to a CSV of growth rates, and performs an Ordinary Least Squares (OLS) linear regression.

Here are the specific requirements:
1. **Inputs:** 
   - A FASTA file located at `/home/user/data/sequences.fasta`.
   - A CSV file located at `/home/user/data/growth_rates.csv` (Format: `SequenceID,GrowthRate`).
2. **Data Processing (Concurrent & Robust):**
   - Write a Go program at `/home/user/fit_model.go`.
   - Parse the FASTA file. The sequence ID is the string immediately following `>` up to the first space or newline.
   - Concurrently calculate the GC ratio ($GC\_ratio = \frac{count(G) + count(C)}{count(A, C, G, T)}$) for each sequence.
   - **Crucial:** Some sequences in the FASTA are corrupted (e.g., containing only 'N's or zero valid nucleotides). These will cause division-by-zero or destabilize the variance. You must strictly ignore any sequence that has a total `A+C+G+T` count of 0.
3. **Curve Fitting:**
   - For the valid sequences that have a corresponding entry in the CSV, fit a simple linear regression model: $GrowthRate = \beta_0 + \beta_1 \times GC\_ratio$.
   - Use the standard analytical OLS formulas:
     $\beta_1 = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2}$
     $\beta_0 = \bar{y} - \beta_1 \bar{x}$
4. **Output:**
   - Calculate $\beta_0$ and $\beta_1$ and write them to a JSON file at `/home/user/model_results.json`.
   - The JSON must have exactly this structure, with values rounded to 4 decimal places:
     ```json
     {
       "beta_0": 1.2345,
       "beta_1": 0.9876
     }
     ```

Please write and execute the Go program to generate the `/home/user/model_results.json` file.