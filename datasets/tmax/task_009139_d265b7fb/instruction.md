You are an observational data scientist working on an atmospheric tracking project. We have a set of raw sensor readings from various planetary probes that needs to be reshaped, averaged, and fitted to a linear regression model ($y = mx + c$) to determine temperature trends over time. 

Because we are working on a highly constrained legacy terminal server, you must use **only standard Bash tools** (e.g., `awk`, `sed`, `grep`, `xargs`, coreutils). Python, R, and other high-level languages are strictly prohibited and uninstalled.

Here is your objective:
1. You will find the raw data inside `/home/user/raw_data/`. There are multiple files, one for each planet (e.g., `Mars.txt`, `Venus.txt`, etc.).
2. The data in these files is structured in a custom format: `PlanetName|Timestamp|Sensor1,Sensor2,Sensor3`
3. You need to reshape this data by calculating the average of the three sensors for each row. Let this average be $Y$, and the Timestamp be $X$.
4. Calculate the Ordinary Least Squares linear regression coefficients (Slope $m$ and Intercept $c$) for $Y$ against $X$ for each planet. 
   *(Hint for awk: $m = \frac{n(\sum xy) - (\sum x)(\sum y)}{n(\sum x^2) - (\sum x)^2}$, and $c = \frac{\sum y - m(\sum x)}{n}$)*
5. To simulate a parallel computing setup to process these files as fast as possible, write a master script at `/home/user/fit_models.sh` that processes all `.txt` files in the `raw_data` directory **in parallel** (using `xargs -P` or backgrounding with `&` and `wait`).
6. Your script must output the final results into a single CSV file at `/home/user/regression_results.csv`.
7. The output CSV must be sorted alphabetically by PlanetName and strictly follow this format: `PlanetName,Slope,Intercept` (with Slope and Intercept formatted to exactly two decimal places, e.g., `Mars,10.00,0.00`).

Ensure your script `/home/user/fit_models.sh` is executable and run it to generate the final `regression_results.csv` file. Do not include a header in the CSV.