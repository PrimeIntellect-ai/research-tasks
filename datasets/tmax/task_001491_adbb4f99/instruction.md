You are assisting a researcher who is organizing datasets in a highly constrained remote server environment. The server lacks Python, R, and other high-level mathematical tools. You must use only standard Bash tools (shell built-ins, coreutils, `awk`, `bc`, etc.) to perform an end-to-end mathematical analysis and modeling task.

You are provided with a dataset at `/home/user/dataset.csv`. The CSV has a header row and comma-separated values. The columns are: `id`, `sensor_A`, `sensor_B`, `sensor_C`, and `target`.

Your objective is to complete the following phases entirely using Bash scripts and CLI tools:

1. **Correlation Analysis & Feature Selection**
   Analyze the dataset to find which of the three features (`sensor_A`, `sensor_B`, or `sensor_C`) has the highest absolute Pearson correlation coefficient with the `target` column. 
   
2. **Model Training (Simple Linear Regression)**
   Using the single most correlated feature identified in step 1, calculate the ordinary least squares (OLS) linear regression parameters: Slope ($m$) and Intercept ($b$). 
   *Formulas:* 
   $m = \frac{n(\sum xy) - (\sum x)(\sum y)}{n(\sum x^2) - (\sum x)^2}$
   $b = \frac{\sum y - m(\sum x)}{n}$
   Round the final Slope and Intercept to exactly 2 decimal places.

3. **Evaluation (Mean Squared Error)**
   Calculate the Mean Squared Error (MSE) of your linear model over the entire dataset. Round the MSE to exactly 2 decimal places.
   $MSE = \frac{1}{n} \sum (y_i - (m \cdot x_i + b))^2$

4. **Inference Benchmarking**
   Create an executable bash script at `/home/user/predict.sh` that takes a single numerical argument (the selected sensor's value) and outputs the predicted target value (rounded to 2 decimal places). 

5. **Reporting**
   Create a report file at `/home/user/report.txt` exactly matching this format:
   ```
   Best Feature: [Feature Name]
   Slope: [m]
   Intercept: [b]
   MSE: [mse]
   ```

**Constraints:**
* Do not install any additional packages (no Python, no R, no Perl). Use `awk`, `bc`, `sed`, `bash`, etc.
* Your scripts and the `predict.sh` file must have execution permissions.
* For floating point math in Bash, you will likely need to rely heavily on `awk` or `bc -l`.