You are assisting a researcher who is running simulations of a biological oscillator. The researcher has extracted a noisy time-series fluorescence signal from the simulation but needs to automatically extract its core periodic properties. 

Your task is to write a Python script that analyzes this data using signal processing and curve fitting.

1. There is a data file located at `/home/user/signal.csv` with two columns: `t` (time in seconds) and `y` (fluorescence intensity). The sampling rate is uniform.
2. Write a Python script at `/home/user/analyze.py` that does the following:
   - Reads `/home/user/signal.csv`.
   - Uses a Fast Fourier Transform (FFT) to determine the dominant frequency ($f_{dom}$) of the signal in Hz. You must ignore the DC component (0 Hz) when finding the peak.
   - Fits the data to the model $y(t) = A \sin(2\pi f_{dom} t + \phi) + C$ using non-linear least squares (`scipy.optimize.curve_fit` is recommended). 
   - Constrain or adjust your final output such that the Amplitude ($A$) is positive, and the phase ($\phi$) is within $[-\pi, \pi]$.
3. The script must write the extracted parameters to a text file at `/home/user/output.txt` exactly in the following format (round all numerical values to exactly 2 decimal places):

```
Frequency: <f_dom>
Amplitude: <A>
Phase: <phi>
Offset: <C>
```

4. Run your script to generate the output file. You can use standard libraries like `numpy`, `scipy`, and `pandas`.