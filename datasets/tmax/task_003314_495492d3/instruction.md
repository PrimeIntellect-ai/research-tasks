You are a machine learning engineer preparing a dataset of spectral readings for a neural network. The raw data from the spectrometer is noisy. Your task is to implement a fast data preprocessing pipeline in C to smooth the data, followed by a bash script to extract features (peaks) and visualize the output as an ASCII plot.

The raw data is located at `/home/user/raw_spectra.txt`. It contains two space-separated columns: `Wavelength` (integer) and `Intensity` (float). 

Please perform the following steps:

1. **Write and compile a C program:**
   - Create a C program at `/home/user/filter.c` and compile it to `/home/user/filter.bin`.
   - The program must read `/home/user/raw_spectra.txt`.
   - Apply a Simple Moving Average (SMA) filter with a window size of 5 to the `Intensity` values. 
   - For a given index $i$, the filtered intensity is the average of the raw intensities at indices $i-2, i-1, i, i+1, i+2$.
   - For the boundary cases (the first two and last two data points), simply copy the raw `Intensity` without modification.
   - Output the results to `/home/user/filtered_spectra.txt` with two space-separated columns: `Wavelength` and `Filtered_Intensity`. Format the `Filtered_Intensity` to exactly two decimal places (e.g., `5.40`).

2. **Write a peak-finding and visualization Bash script:**
   - Create a bash script at `/home/user/process_spectra.sh` and make it executable.
   - The script should read `/home/user/filtered_spectra.txt` and find all local maxima (peaks). A point is a local maximum if its `Filtered_Intensity` is strictly greater than both its immediate preceding and succeeding points.
   - Append the `Wavelength` and `Filtered_Intensity` of these peaks to `/home/user/peaks.log` (space-separated).
   - The script must also generate an ASCII bar chart of the filtered spectra in `/home/user/plot.txt`. For each line in `filtered_spectra.txt`, output `Wavelength | ` followed by a number of `*` characters.
   - The number of `*` characters should be calculated as `floor((Filtered_Intensity / Max_Filtered_Intensity) * 20)`. If the value is 0 or negative, print 0 stars. 

Run your C program and your bash script to produce the final outputs `/home/user/filtered_spectra.txt`, `/home/user/peaks.log`, and `/home/user/plot.txt`.