I am a researcher running spectral simulations on large time-series datasets. I wrote a Python script located at `/home/user/analyze_signal.py` that generates a 10-million-point synthetic signal (using `float32` to save memory) and verifies Parseval's theorem: the total energy of the signal in the time domain should equal the total energy in the frequency domain.

However, I am getting non-reproducible and highly inaccurate results. The absolute difference between the time-domain energy and the frequency-domain energy is massive. I suspect this is due to floating-point reduction order issues and numerical instability when performing standard summations (`np.sum`) over 10 million single-precision floats. 

Your task is to:
1. Modify `/home/user/analyze_signal.py` to fix the numerical stability issues in the energy summation. You must retain the `float32` datatype for the signal and FFT arrays to simulate my memory constraints, but you are permitted to accumulate the sum using `float64` or a stable summation algorithm (like Kahan summation or `math.fsum`).
2. The script currently writes the absolute difference between the time-domain energy and frequency-domain energy to `/home/user/energy_diff.txt`. Once you fix the summation, run the script so it outputs the newly corrected difference. The difference must be less than `1.0`.
3. Analyze the frequency spectrum of the signal to find the dominant frequency (the frequency with the highest power, ignoring the DC component/0 Hz). Write this dominant frequency as an integer to `/home/user/dominant_freq.txt`.

Ensure your final modifications are saved in `/home/user/analyze_signal.py` and that all output files are generated correctly. You may install any standard Python scientific libraries you need.