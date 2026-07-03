You are a data processing analyst tasked with building a high-performance analytics microservice in C. 

We have a dataset located at `/app/data.csv` (which has 4 columns: `f1`, `f2`, `f3`, `target`, all floats, with no header row). 
We also have an image containing our configuration parameters for the current modeling sprint located at `/app/config.png`.

Your objectives are:
1. **Extract Parameters:** Read `/app/config.png` (using OCR) to extract the cross-validation configuration. It contains text like `K_FOLDS=X` and `LAMBDA_VALS=A,B,C`.
2. **C Analytics Engine:** Write a C program (`/home/user/engine.c`) that links against the GNU Scientific Library (GSL). It should:
   - Read a CSV file passed as an argument.
   - Compute the Pearson correlation matrix for the 4 columns.
   - Perform a basic cross-validation grid search (using the `K_FOLDS` value and testing the `LAMBDA_VALS` extracted from the image) for a mock regularized model. For simplicity, the "MSE" for a given $\lambda$ in fold $k$ is calculated as a dummy function: $MSE = ( \lambda - \text{average\_correlation\_of\_fold} )^2$. Find the $\lambda$ that minimizes the average MSE across all folds.
3. **Microservice Configuration:** Create a web service listening on `127.0.0.1:8080`. You may write the web server in C (e.g., using `libmicrohttpd`) or use a Python wrapper script (e.g., Flask/FastAPI) that executes your compiled C binary. 
   - `GET /correlation`: Returns a JSON array of arrays representing the $4 \times 4$ correlation matrix.
   - `GET /tune`: Returns a JSON object `{"best_lambda": <float>, "k_folds": <int>}` based on the bounds extracted from the image and the C program's evaluation.

Ensure your service is running in the background and bound to port 8080 before you finish. Do not hardcode the parameters; they must be dynamically read or compiled based on the image contents.