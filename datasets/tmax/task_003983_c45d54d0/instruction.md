You are a data scientist working on a massive telemetry dataset. The data pipeline is clogged with corrupted and maliciously crafted sensor records. We have a proprietary legacy anomaly detector located at `/app/anomaly_oracle` (a stripped binary). This oracle correctly identifies whether a sensor record is "clean" or "evil". 

However, the oracle is incredibly slow, memory-heavy, and cannot handle our large-scale data storage needs. We need a fast, standalone C implementation that perfectly replicates its decision boundary.

Your task:
1. **Model Reconstruction:** Analyze or black-box probe `/app/anomaly_oracle`. It takes a single file path as an argument. The input files are binary files containing exactly 64 single-precision float values (little-endian). The oracle exits with code `0` for clean data and code `1` for anomalous (evil) data. Deduce the statistical model or decision boundary it uses (Hint: it relies on a very simple linear architecture).
2. **Fast Filter Implementation:** Write a C program at `/home/user/fast_filter.c` and compile it to `/home/user/fast_filter`. 
3. **Data Pipeline Integration:** Your C program must accept exactly two arguments: an input directory containing `.bin` files, and an output directory.
   - Invocation: `/home/user/fast_filter <input_dir> <output_dir>`
   - It should process all `.bin` files in the input directory.
   - For each file, if it is "clean", copy it to `<output_dir>/clean/<filename>`.
   - If it is "evil", copy it to `<output_dir>/evil/<filename>`.
   - The program must benchmark its own inference performance: when finished, it must print "Processed X files in Y seconds" to stdout.
4. **Environment Setup:** You are responsible for any scripts needed to generate dummy data to probe the oracle.

The automated testing suite will invoke your `/home/user/fast_filter` on a hidden evaluation dataset containing highly adversarial edge cases. It must perfectly separate the clean and evil data.