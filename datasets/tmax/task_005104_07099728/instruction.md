You are a machine learning engineer preparing time-series data for a new model. The raw data extraction utility needs to be compiled from source, and the signal processing pipeline needs to be implemented in Rust.

Please complete the following steps:
1. Compile the C source file located at `/home/user/src/extractor.c`. Compile it with `gcc` and place the executable at `/home/user/bin/extractor`. You may need to link the math library (`-lm`).
2. Run the extractor utility to generate exactly 1024 data points: `/home/user/bin/extractor 1024 > /home/user/data/signal.csv`. This file contains one floating-point number per line.
3. Create a new Rust binary project named `processor` in `/home/user/processor`.
4. In this Rust project, write a program that:
   - Reads the 1024 floating-point numbers from `/home/user/data/signal.csv`.
   - Uses the `rustfft` crate to perform a forward Fast Fourier Transform (FFT) on the sequence. Treat the input data as purely real (imaginary part = 0.0).
   - Filters out high-frequency noise by zeroing out specific frequency bins: set the complex values at indices 32 through 992 (inclusive) to exactly `0.0 + 0.0i`.
   - Performs an Inverse Fast Fourier Transform (IFFT) on the filtered frequency domain data.
   - Normalizes the output by dividing each resulting complex number by the sequence length (1024).
   - Writes the real part of the resulting time-series to `/home/user/data/processed.csv`. Format each value to exactly 4 decimal places (e.g., `0.1234`), with one value per line.
5. Run your Rust project to generate the final `/home/user/data/processed.csv` file.

Ensure all directories and paths are respected exactly.