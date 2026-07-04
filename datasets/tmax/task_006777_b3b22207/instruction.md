I am a researcher organizing a dataset of simulated wave propagation signals, but I'm having trouble with my data processing pipeline. I am working on a headless Linux server.

I have a raw dataset at `/home/user/raw_waves.csv` containing columns `time` and `amplitude`. 
There is a skeleton script at `/home/user/process_waves.py`. Currently, it crashes, doesn't clean the data, and its plotting function fails or produces blank images because of a backend misconfiguration on this headless setup.

Please fix my environment and complete the script `/home/user/process_waves.py` to perform the following end-to-end tasks:

1. **ETL Pipeline**: Read `/home/user/raw_waves.csv` using pandas. Drop any rows where `amplitude` is missing (NaN). Save this cleaned dataset to `/home/user/cleaned_waves.csv` (keeping the same header).
2. **Benchmarking**: Measure the time it takes to compute the Fast Fourier Transform (`numpy.fft.fft`) on the cleaned `amplitude` array. Write the elapsed time (in seconds, just the float value) to `/home/user/benchmark.txt`.
3. **Numerical Accuracy Testing**: Verify Parseval's theorem on the cleaned data. The theorem states that the sum of the square of the signal equals the sum of the square of the absolute FFT values divided by the number of samples `N`. Calculate the absolute difference between these two quantities. Save the result to `/home/user/accuracy.json` in the exact format: `{"parseval_diff": <float>, "accurate": <bool>}`, where `accurate` is `true` if the difference is strictly less than `1e-5`.
4. **Visualization**: Generate a plot of the power spectrum (the absolute values of the FFT result against their indices) and save it to `/home/user/spectrum.png`. You must ensure the matplotlib backend is properly configured for a headless environment so the output file is a valid, non-blank PNG image.

You may need to install necessary Python libraries. Ensure your final script runs successfully and generates all four output files:
- `/home/user/cleaned_waves.csv`
- `/home/user/benchmark.txt`
- `/home/user/accuracy.json`
- `/home/user/spectrum.png`