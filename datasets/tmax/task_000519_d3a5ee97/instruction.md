I am a materials science researcher running high-throughput spectroscopy simulations. My simulation pipeline generates thousands of spectral absorption curves, but due to numerical instabilities and unphysical parameters in my Monte Carlo generator, some of the generated data is "corrupted" (unphysical noise, wrong peak locations, or excessively broad peaks). 

I need you to create a high-performance data sanitization filter in Rust. 

Here is what you need to do:
1. **Extract Calibration Parameters**: I left a scanned note with the expected absorption parameters at `/app/calibration_specs.png`. Please extract the text from this image (you can use standard OCR tools available on Linux). It contains the `EXPECTED_PEAK_CENTER` (in nm) and the `MAX_FWHM` (Maximum Full-Width at Half-Maximum, in nm).
2. **Understand the Data**: The spectra are provided as CSV files with two columns: `wavelength,intensity`. A valid (clean) spectrum has a baseline intensity of approximately 1.0, with a single absorption dip (minimum intensity < 0.8). 
3. **Write the Filter**: Create a Rust project at `/home/user/spectro_filter`. Write a CLI program that accepts a single argument: the absolute path to a CSV file.
   - The program must parse the CSV.
   - It must find the wavelength of the minimum intensity point ($\lambda_{min}$).
   - It must calculate the FWHM (Full-Width at Half-Maximum). You can assume the baseline is exactly 1.0. The half-depth intensity is $I_{half} = 1.0 - (1.0 - I_{min})/2$. The FWHM is the difference between the largest wavelength and smallest wavelength where the intensity drops below $I_{half}$.
   - The spectrum is **VALID (clean)** if:
     - $|\lambda_{min} - EXPECTED\_PEAK\_CENTER| \le 5.0$ nm.
     - The calculated FWHM $\le MAX\_FWHM$.
   - The spectrum is **INVALID (evil)** if it fails the above conditions, or if it is excessively noisy (e.g., multiple deep dips).
4. **Program Behavior**: 
   - If the CSV is VALID, the program must exit with status code `0`.
   - If the CSV is INVALID, the program must exit with status code `1` (or any non-zero code).
5. **Compile**: Ensure your binary is built in release mode, resulting in an executable at `/home/user/spectro_filter/target/release/spectro_filter`.

I have a test corpus of simulations. Your tool will be evaluated by a rigorous automated test script against a hidden set of clean and corrupted data. Accuracy must be 100%. Use your scientific computing skills to ensure the peak finding and FWHM logic is robust against minor discretization artifacts!