You are a performance engineer tasked with optimizing a critical data processing step in our computational fluid dynamics (CFD) pipeline. 

We have a massive simulation mesh stored in HDF5 format (`/home/user/mesh_data.h5`). The mesh needs to be partitioned into sub-domains for parallel processing. Currently, we have a black-box legacy tool, `/app/legacy_partitioner`, which correctly reads the HDF5 mesh, performs a spatial domain decomposition (using a recursive coordinate bisection method), and outputs an HDF5 file with the partition IDs for each element. 

However, `/app/legacy_partitioner` is extremely slow. 

Your task is to write a highly optimized C program from scratch that replicates the functionality of `/app/legacy_partitioner`. 
Your program must:
1. Read the input HDF5 mesh (`/home/user/mesh_data.h5`), which contains a dataset `/coordinates` of shape `(N, 3)` (double precision floats).
2. Perform recursive coordinate bisection to partition the elements into 16 sub-domains. The bisection always splits along the axis with the largest spread (max - min) at the median value of that axis.
3. Write the resulting partition IDs (0 to 15) to an output HDF5 file `/home/user/optimized_partitions.h5` as an integer dataset named `/partition_ids` of shape `(N,)`.
4. Produce *exactly* the same partition assignments as `/app/legacy_partitioner`. You can use the legacy tool as an oracle to test your correctness. 

Your C code must be compiled to an executable at `/home/user/fast_partitioner`.

Your solution will be evaluated on a much larger hidden dataset. To pass, your implementation must produce the exact same HDF5 output as the legacy binary AND achieve a **runtime speedup of at least 3.0x** over `/app/legacy_partitioner` on the test machine.

Constraints & Notes:
- You must write the solution in C.
- You will need to install the HDF5 C library and development headers (e.g., `libhdf5-dev`).
- Make sure to compile with `-O3`.
- The execution time of `/home/user/fast_partitioner` will be timed and compared against `/app/legacy_partitioner`.