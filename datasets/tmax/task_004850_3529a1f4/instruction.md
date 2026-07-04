You are a performance engineer tasked with profiling a legacy application and creating a precise latency predictor.

You have been provided with two key artifacts:
1. `/app/raw_metrics.log`: A messy, unstructured log file containing recent performance observations.
2. `/app/system_specs.png`: An image of a configuration document containing two critical system constants: `Alpha` and `Beta`.

Your task is to build a robust bash predictor script by completing the following multi-stage workflow:

**Stage 1: Environment Setup & Data Extraction**
* Use OCR (`tesseract` is installed) to extract the values of `Alpha` and `Beta` from `/app/system_specs.png`. 
* Parse `/app/raw_metrics.log` to reshape the observational data. You must extract pairs of `CPU_Load` and `Response_Latency` from lines containing the tag `[METRIC]`. Ignore any lines containing the word `ERROR` or `TIMEOUT`.

**Stage 2: Curve Fitting & Regression**
* Using Bash and shell built-ins/utilities (like `awk` or `bc`), perform a simple linear regression ($Y = mX + c$) on the cleaned data, where $X$ is `CPU_Load` and $Y$ is `Response_Latency`.
* Calculate the slope ($m$) and intercept ($c$). 

**Stage 3: Predictor Implementation & Numerical Stability**
* Create an executable bash script at `/home/user/predictor.sh`.
* The script must take exactly one argument: a `CPU_Load` integer (which can be very large, up to $10^9$).
* To ensure numerical stability and avoid standard bash integer overflow, your script must use `awk` or `bc` internally to compute the final adjusted latency using the formula:
  `Adjusted_Latency = Alpha * (m * CPU_Load + c) + Beta`
* **Formatting Rules for BIT-EXACT Verification:** 
  - When writing your script, hardcode the calculated values of $m$ and $c$ rounded to exactly 2 decimal places (e.g., standard half-up rounding, so 4.855 becomes 4.86).
  - Hardcode `Alpha` and `Beta` exactly as they appear in the image.
  - The script must print *only* the `Adjusted_Latency`, formatted to exactly 3 decimal places (e.g., `124.500`).

Do not use Python, Perl, or any non-Bash languages for the solution; rely entirely on Bash, `awk`, `sed`, `bc`, `grep`, and `tesseract`.