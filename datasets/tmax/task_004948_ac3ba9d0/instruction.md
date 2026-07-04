You are acting as a data scientist analyzing spectral data. We have extracted power spectral density (PSD) data from a time-series signal, and we need to fit a simple threshold model by computing the total energy in the spectrum and comparing it to a reference dataset.

You have been provided with a partial C++ program `/home/user/analyze_spectra.cpp`. This program reads a CSV file containing frequency and PSD values, and it reads a reference energy threshold from a text file.

Your task is to:
1. Complete the `computeTotalEnergy` function in `/home/user/analyze_spectra.cpp`. You must implement the **Trapezoidal Rule** for numerical integration to calculate the total energy (the integral of PSD with respect to frequency).
2. Compile the C++ program into an executable named `analyze_spectra` in the `/home/user` directory. You may use standard `g++`.
3. Run the executable using the provided data files:
   `/home/user/analyze_spectra /home/user/data.csv /home/user/reference.txt`
4. Ensure the program creates a file at `/home/user/result.txt` with the following exact format:
   ```
   Total Energy: <calculated_value>
   Exceeds Reference: <Yes/No>
   ```
   (Print the calculated value to 2 decimal places. The reference value is simply a floating point number inside `reference.txt`.)

Do not use any external libraries other than the C++ Standard Library.