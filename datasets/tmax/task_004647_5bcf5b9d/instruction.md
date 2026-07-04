You are a Machine Learning Engineer responsible for preparing training data for a new anomaly detection model. 

We have a legacy data cleaning tool located at `/app/oracle_processor`. It is an old, stripped, and undocumented binary. It reads raw sensor data from an HDF5 file, applies a proprietary denoising and normalization algorithm, and writes the processed features to a new HDF5 file. 
Usage: `/app/oracle_processor <input.h5> <output.h5>`
It expects an input HDF5 file containing a dataset named `raw_features` (shape: N x 50 float64) and produces an output HDF5 file with a dataset named `clean_features` (shape: N x 5 float64).

The problem is that `/app/oracle_processor` is incredibly slow and cannot scale to the petabytes of data we need to process. 

Your task is to write a fast Python replacement script at `/home/user/fast_prepare.py`.
Usage: `python3 /home/user/fast_prepare.py <input.h5> <output.h5>`

**Investigation Hints:**
We suspect the binary performs the following mathematical operations:
1. A linear dimensionality reduction via matrix decomposition (likely PCA / Truncated SVD) to reduce the 50 dimensions down to 5.
2. An independent density estimation/distribution fitting step on each of the 5 resulting latent dimensions, mapping their empirical distributions to a uniform [0, 1] range (i.e., empirical CDF mapping or Quantile Transformation).

**Your Workflow:**
1. Generate some dummy raw data in HDF5 format to probe the binary.
2. Run `/app/oracle_processor` on your dummy data to observe the input-output relationship.
3. Write `/home/user/fast_prepare.py` using `numpy`, `scipy`, or `scikit-learn` to approximate the binary's transformation. You are highly encouraged to fit a pipeline (e.g., PCA + QuantileTransformer) on a large sample and save the fitted parameters (e.g., using `joblib` or `pickle`) so your script can quickly apply the transformation to new files.
4. Ensure your script reads `raw_features` and writes `clean_features` to the specified HDF5 output file.

**Evaluation:**
We will test your script against a held-out raw HDF5 file (`/tmp/test_raw.h5`) by running:
`python3 /home/user/fast_prepare.py /tmp/test_raw.h5 /home/user/test_processed.h5`
We will then calculate the Mean Squared Error (MSE) between your script's output and the oracle's output. Your script must achieve an MSE of less than 0.005.

Note: You have full access to install packages via `pip`.