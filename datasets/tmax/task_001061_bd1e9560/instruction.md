You are a bioinformatics analyst working on a sequence processing pipeline. We need to analyze a large dataset of DNA sequences to test a hypothesis about GC content bias in sequences containing a specific motif. 

Your task is to write a complete Go application that performs parallel sequence processing, statistical summary, visualization, and includes regression testing.

Here are the requirements:

1. **Setup Workspace**: 
   - Work in `/home/user/analysis`.
   - Initialize a Go module named `bioanalysis`.
   - The input file is located at `/home/user/data/input.fasta`. It contains thousands of DNA sequences in standard FASTA format.

2. **Parallel FASTA Processing**:
   - Write a Go program (`main.go`) that reads `/home/user/data/input.fasta`.
   - You must parse the FASTA file and calculate the GC content percentage for each sequence: `(count(G) + count(C)) / length(sequence) * 100`.
   - **Requirement**: The GC content calculation must be done concurrently using Go routines and channels or waitgroups to process multiple sequences in parallel.

3. **Statistical Hypothesis Comparison**:
   - Split the sequences into two groups:
     - **Group A**: Sequences that contain the exact motif `ATGCATGC` anywhere in their string.
     - **Group B**: Sequences that DO NOT contain this motif.
   - Calculate the mean GC content for Group A and Group B.
   - Calculate the absolute difference between these two means.
   - We consider the difference "significant" if the absolute difference is strictly greater than `5.0`.
   - Write the results to a JSON file at `/home/user/analysis/results.json` with exactly this structure:
     ```json
     {
       "group_a_mean": 55.421,
       "group_b_mean": 45.123,
       "difference": 10.298,
       "significant": true,
       "num_group_a": 120,
       "num_group_b": 9880
     }
     ```
     *(Round floats to 3 decimal places in the JSON)*

4. **Experimental Data Visualization**:
   - Use the `gonum.org/v1/plot` library (or another Go plotting library of your choice) to generate a simple bar chart comparing the mean GC content of Group A vs Group B.
   - Save the plot as `/home/user/analysis/gc_plot.png`.

5. **Scientific Code Regression Testing**:
   - Create a test file `analyzer_test.go` that tests your GC calculation function.
   - Include at least 3 table-driven test cases (e.g., all Gs, all As, mixed, empty sequence).
   - The tests must pass when `go test` is executed.

Run your application to generate the `results.json` and `gc_plot.png` files, and ensure your tests pass.