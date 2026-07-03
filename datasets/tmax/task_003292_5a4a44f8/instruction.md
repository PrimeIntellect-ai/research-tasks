You are a bioinformatics analyst modeling bacterial population dynamics. We have received an image `/app/lab_notes.png` containing handwritten lab notes with key parameters for our growth model. 

Your task is to:
1. Extract the growth rate (`r`) and carrying capacity (`K`) from the image using OCR (Tesseract is available).
2. Write a Bash script `/home/user/simulate_growth.sh` that simulates the population over time using the logistic growth ODE: `dP/dt = r * P * (1 - P / K)`.
3. Your script must use Euler's method for the numerical integration.
4. The script must accept exactly three command-line arguments in this order:
   - `P0`: Initial population (floating point).
   - `dt`: Time step size for Euler's method (floating point).
   - `N`: Number of steps to simulate (integer).
5. The script should print only the final population after `N` steps, rounded to 4 decimal places.

Ensure your Bash script calculates the steps accurately and handles floating-point arithmetic (e.g., using `awk` or `bc`). We will test your script's correctness by running it with random inputs and comparing its output to a reference binary.