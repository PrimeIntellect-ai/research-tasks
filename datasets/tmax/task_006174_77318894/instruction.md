You are a data analyst working entirely in the Linux terminal. You need to process a raw medical dataset using Bash, command-line utilities, and an external tool.

The raw data is located at `/home/user/data/patients.csv` and contains three columns: `ID,Age,BloodPressure`.

Your task is to write a Bash pipeline or script to do the following:

1. **Package Installation:** Install `csvkit` locally using `pip install --user csvkit`. Ensure `~/.local/bin` is in your PATH so you can use tools like `csvgrep`.
2. **Data Schema Enforcement:** The dataset is dirty. Use `csvgrep` to filter out any rows where `Age` or `BloodPressure` contain non-numeric characters or are empty. Both columns must consist entirely of digits (0-9).
3. **Classification:** For the valid rows, calculate a risk score using the following linear regression-based formula:
   `Score = (0.05 * Age) + (0.02 * BloodPressure) - 5.0`
   If the `Score` is greater than `0`, classify the risk as `1` (High Risk). Otherwise, classify the risk as `0` (Low Risk). You must implement this math using pure Bash, `awk`, or `bc`.
4. **Output Generation:** Write the final classified data to `/home/user/risk_output.csv`. The file must be a valid CSV containing exactly two columns: `ID` and `Risk`. The first line must be the header `ID,Risk`.

You can do this directly in the terminal or write a script to execute it. The final evaluation will simply check the contents of `/home/user/risk_output.csv`.