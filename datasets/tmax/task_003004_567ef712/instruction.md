You are acting as a data analyst working with an audio engineering team. The team extracts waveform data from audio files into CSV format to analyze signal anomalies. We have been receiving "poisoned" audio samples that contain severe high-variance noise spikes. 

We have provided a reference audio file at `/app/reference.wav` which you can inspect if needed, but your primary task is to write a classification tool to automatically filter out poisoned data.

Your goal is to build a C-based command-line classifier that reads a waveform CSV file and determines if it is "clean" or "poisoned".

Requirements:
1. Write a C program at `/home/user/classifier.c`.
2. The program must parse a CSV file provided as its first command-line argument. The CSV files contain two columns with a header row: `time,amplitude` (both are floating-point numbers).
3. You must configure and use the GNU Scientific Library (GSL) to compute the sample standard deviation of the `amplitude` column. (You will need to install the necessary packages on the system to use GSL).
4. If the sample standard deviation of the amplitude is strictly greater than `10.5`, the program must reject the file by exiting with status code `1` (indicating a "poisoned" or evil file).
5. If the standard deviation is less than or equal to `10.5`, the program must accept the file by exiting with status code `0` (indicating a "clean" file).
6. Compile your program to the executable `/home/user/classifier`.

Your tool will be tested against two hidden corpora of CSV files: a clean set and a poisoned set. Your program must correctly accept all clean files and reject all poisoned ones.