You are a machine learning engineer preparing training data for a genomic foundational model. You need to write a C program to calculate statistical features from a set of DNA sequences and reference weights stored in a scientific data format.

Your task:
1. Ensure the necessary C libraries for HDF5 development are installed on the system (e.g., `libhdf5-dev`).
2. Write a C program at `/home/user/process.c` that does the following:
   - Parses the FASTA file located at `/home/user/data.fasta` to determine the length (number of characters, excluding newlines and header lines) of each sequence.
   - Reads the HDF5 file located at `/home/user/ref.h5`. This file contains a 1D dataset named `weights` of type double (`H5T_NATIVE_DOUBLE`). The number of weights matches the number of sequences in the FASTA file.
   - Computes the "weighted length" for each sequence: `sequence_length * weight`.
   - Computes the mean and population variance of these weighted lengths.
   - Computes the discrete numerical derivative (forward differences) of the weighted lengths, i.e., `diff[i] = weighted_length[i+1] - weighted_length[i]`, and finds the maximum absolute difference (`Max_Abs_Diff`).
3. Compile and run your program. It must write the final statistics to `/home/user/stats.txt` in exactly the following format (values rounded to 2 decimal places):
```
Mean: <value>
Variance: <value>
Max_Abs_Diff: <value>
```

Constraints:
- Use C as your programming language.
- You may use the standard C library and the HDF5 C API. 
- You may need to specify the correct include paths and linker flags when compiling (e.g., `-I/usr/include/hdf5/serial -L/usr/lib/x86_64-linux-gnu/hdf5/serial -lhdf5`).