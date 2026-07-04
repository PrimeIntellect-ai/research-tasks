You are assisting a data scientist who is cleaning a large mathematical dataset of vector embeddings, but they are running into several technical roadblocks. 

Here are your objectives:

1. **Fix the Visualization Script:**
   The data scientist wrote a script at `/app/plot_correlations.py` to generate covariance/correlation heatmaps of the datasets. However, due to a backend misconfiguration (likely an issue with running in a headless Linux environment), it is generating completely blank or empty image files. Fix the script so it correctly renders and saves a non-blank heatmap to `/home/user/correlation.png`. 

2. **Extract the Correlation Threshold:**
   We need to filter out datasets that contain highly redundant features. The exact threshold for this is documented in a legacy plot image located at `/app/threshold_image.png`. You must use OCR (Tesseract is preinstalled) to read the text in this image and find the mathematical threshold value (it will be in the format `THRESHOLD=X.XX`).

3. **Build the Dataset Filter (Adversarial Corpus Task):**
   Write a Python CLI tool at `/home/user/filter_datasets.py` that filters datasets based on feature correlation and similarity.
   * **CLI Signature:** `python3 /home/user/filter_datasets.py <input_dir> <output_dir>`
   * **Logic:** The script should iterate over all `.npy` files (2D numpy arrays where rows are samples and columns are features) in `<input_dir>`. For each dataset, calculate the Pearson correlation matrix between all features (columns). If the maximum absolute correlation between *any two distinct features* is greater than or equal to the threshold you extracted via OCR, the dataset is considered "corrupted/redundant" and must be rejected. 
   * **Action:** Only copy the files that pass the check (i.e., are "clean") into `<output_dir>`. 

4. **Inference Performance Benchmarking:**
   The filtering script must benchmark its own performance. After processing the input directory, it must write the average time taken to process a single file (in seconds) to `/home/user/benchmark.txt` (just the float value on a single line).

Ensure that all scripts are executable and that you have installed any necessary Python libraries (like `pytesseract`, `Pillow`, `numpy`, `matplotlib`, etc.).