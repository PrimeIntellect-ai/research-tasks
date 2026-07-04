You are a bioinformatics analyst tasked with designing an optimal primer sequence for a novel target region.

We have a proprietary scoring tool, provided as a stripped binary at `/app/binding_scorer`. It takes a 20-bp DNA sequence (consisting only of A, C, G, T) as a single command-line argument and prints a binding affinity score (a floating-point number). 

We also have a genomic data file in HDF5 format at `/app/genomic_landscape.h5`. It contains a single dataset named `nucleotide_probs` of shape `(4, 10000)`, representing the probabilities of A, C, G, and T (in that exact order) at each position along a 10,000-bp contig.

Your objective is to write a Rust project in `/home/user/primer_opt` that performs the following multi-stage pipeline:

1. **Environment Setup**: Ensure your environment has the necessary system libraries (e.g., `libhdf5-dev`) to compile Rust scientific I/O crates.
2. **Data Ingestion & Array Manipulation**: Read the `nucleotide_probs` dataset from `/app/genomic_landscape.h5`. Compute the "consensus sequence" by taking the nucleotide with the highest probability at each of the 10,000 positions.
3. **Density Estimation**: Find the 500-bp window within this consensus sequence that has the highest GC-content density. Implement a moving average or kernel density estimator over the consensus sequence to locate the start index of this optimal 500-bp region.
4. **Primer Optimization**: Within that specific 500-bp window, evaluate all possible contiguous 20-bp candidate primers. For each candidate, invoke the black-box oracle `/app/binding_scorer` to get its binding affinity score. 
5. **Output**: Identify the 20-bp primer with the highest score. Write your final answer to `/home/user/solution.txt` containing exactly one line in the format: `SEQUENCE,SCORE`.

Ensure your Rust program compiles successfully from source and runs efficiently. You may use external Rust crates like `ndarray` and `hdf5`. Do not hardcode offsets; your Rust code must perform the array manipulation, argmax, and density estimation dynamically.