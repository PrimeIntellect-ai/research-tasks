You are a performance engineer working on a structural bioinformatics project. Your team needs a fast, optimized C program to process large Protein Data Bank (PDB) files, extract specific atomic signals, process them, and perform statistical modeling.

Your task is to write a C program that does the following:
1. Reads a PDB file located at `/home/user/data/input.pdb`.
2. Parses the `ATOM` records and extracts only the alpha-carbon (`CA`) atoms (identified by `" CA "` in columns 13-16).
3. Extracts the residue sequence number (columns 23-26, integer) as the X variable, and the temperature factor (B-factor, columns 61-66, float) as the raw Y variable.
4. Applies a Simple Moving Average (SMA) filter to the B-factor signal to smooth it out. Use a window size of 5 (i.e., for an element at index `i`, average the available elements from `i-2` to `i+2`, properly handling the boundaries where fewer than 5 elements are available).
5. Performs a linear regression ($Y = mX + c$) on the smoothed B-factors ($Y$) against the residue sequence numbers ($X$) to find the global trend of protein flexibility.
6. The C program must output the final slope and intercept to `/home/user/regression_results.txt` in exactly this format:
   ```
   Slope: [value]
   Intercept: [value]
   ```
   (Format the values to 4 decimal places).

Additionally, as part of your performance profiling:
1. Compile your C program with `-O3` optimization.
2. Run your application and profile its execution.
3. Write a brief report to `/home/user/profile.txt` containing the word `COMPLETED` and the path to the executable you profiled.

All work should be done in `/home/user`. Do not use external libraries other than the standard C library (`stdio.h`, `stdlib.h`, `string.h`, `math.h`, etc.).