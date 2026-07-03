You are assisting a data scientist who needs to fit a series of linear models on highly collinear data. We have 5 different experimental datasets. 

The input features are stored in a 3-dimensional numpy array at `/home/user/X_data.npy` with shape `(5, 50, 10)` representing `(datasets, samples, features)`.
The corresponding target values are stored at `/home/user/y_data.npy` with shape `(5, 50)`.

Your task is to:
1. Create a Jupyter Notebook named `/home/user/fit_models.ipynb`.
2. Inside the notebook, write Python code to load the arrays.
3. For each of the 5 datasets, compute the linear regression weights $w$ that minimize $||Xw - y||_2$. Because the features are highly collinear, you must use Singular Value Decomposition (SVD) to construct the Moore-Penrose pseudoinverse. 
4. Crucially, to regularize the solution, you must implement a truncated SVD: any singular value strictly less than `1e-4` must be treated as zero when computing the pseudoinverse.
5. Collect the computed weights into a single numpy array of shape `(5, 10)`.
6. Save this final weights array to `/home/user/weights.npy`.
7. Execute the notebook from the command line (e.g., using `jupyter nbconvert` or `papermill`) so that the notebook runs headlessly and produces the output file.

Ensure your notebook is fully self-contained and runs without errors when executed top-to-bottom.