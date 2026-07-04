You are a bioinformatics analyst processing raw nanopore sequencing current signals. We have discovered a severe issue in our legacy analysis pipeline: certain raw signal files cause our main sequence aligner to produce non-reproducible results. After debugging, we found this happens because the aligner uses a parallelized reduction to normalize signals, and some maliciously malformed or corrupted signal files suffer from severe floating-point reduction order dependencies (catastrophic cancellation), causing different threads to compute vastly different total signal intensities depending on chunking.

Your task is to create a robust C-based filter to sanitize our datasets. 

1. **Investigate the Oracle:**
   There is a stripped, heavily optimized binary at `/app/signal_aligner`. This is our legacy processor. We cannot modify it. You can observe its behavior on signal files, but your main goal is to build a pre-filter.

2. **Develop the Filter:**
   Write a C program at `/home/user/filter_signal.c` and compile it to `/home/user/filter_signal`.
   - The program must take a single command-line argument: the path to a signal file.
   - A signal file is a raw binary file containing an array of 32-bit single-precision floats (IEEE 754, little-endian).
   - Your program must read the entire file.
   - It must compute the total sum of the signal intensities in two ways:
     a) Left-to-right (index 0 to N-1). Let this be `Sum_LR`.
     b) Right-to-left (index N-1 down to 0). Let this be `Sum_RL`.
   - Compute the absolute difference: `Diff = |Sum_LR - Sum_RL|`.
   - If `Diff > 0.01`, the file is deemed unstable/corrupt. Your program must print `EVIL` to stdout and exit with code `1`.
   - If `Diff <= 0.01`, the file is valid. Your program must print `CLEAN` to stdout and exit with code `0`.
   - Also reject the file (exit 1) if it contains any NaN or Infinity values.

3. **Validation Corpora:**
   To test your implementation, we have provided two sets of reference datasets:
   - `/app/corpus/clean/`: Contains typical, valid nanopore signal files.
   - `/app/corpus/evil/`: Contains malformed files designed to trigger the floating-point instability.
   
Your compiled binary `/home/user/filter_signal` must correctly classify 100% of the files in both directories.