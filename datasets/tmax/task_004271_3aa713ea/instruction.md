You are an ML Engineer preparing and debugging a data pipeline. A legacy feature-extraction simulator generates a dataset of features ($x_1$, $x_2$) and labels ($y$). However, due to non-deterministic parallel floating-point reduction orders in the legacy C++ code, the outputs ($y$) contain noise and lack exact reproducibility.

We know the underlying model is exactly a linear relationship: 
$y = w_1 x_1 + w_2 x_2 + b + \text{noise}$

Your task is to write a purely Bash-based optimization script to estimate the true underlying weights ($w_1$, $w_2$) and the bias ($b$), effectively bypassing the noise through analytical/optimization means. 

Requirements:
1. Generate the training data by running the existing script: `python3 /home/user/generate_data.py`. This will create `/home/user/training_data.csv` (header: `x1,x2,y`).
2. Write a Bash script `/home/user/optimize.sh`. This script MUST implement Gradient Descent (or exactly solve the normal equations) to find $w_1, w_2, b$ that minimize the Mean Squared Error.
3. **CRITICAL CONSTRAINT:** You may NOT write or execute any Python, R, Perl, Ruby, or Node.js scripts to perform the optimization. Your `optimize.sh` must rely strictly on standard Unix text processing utilities (e.g., `awk`, `bc`, `sed`, `grep`, `bash`). Using `awk` for the mathematical operations and optimization loop is highly recommended.
4. Your script must output the final estimated weights into a file named `/home/user/weights.csv` in the exact format: `w1,w2,b` (e.g., `1.23,-0.45,0.01`).
5. The estimates must be within $\pm 0.1$ of the true analytical weights used by the generator. 

Run your script, ensure it completes successfully, and verify that `/home/user/weights.csv` is created with the correct format.