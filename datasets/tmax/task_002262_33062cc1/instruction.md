You are a data engineer maintaining an ETL pipeline. As part of a data drift diagnostic step, a Python script `/home/user/etl_diagnostic.py` is executed to perform dimensionality reduction (PCA) on a bootstrap sample of the incoming data, plot the explained variance, and log the optimal hyperparameters. 

However, the script is currently broken:
1. It attempts to display a plot interactively, which fails or produces a blank output in our headless Linux environment. It needs to save the plot to `/home/user/pca_plot.png`.
2. It fails to take a bootstrap sample. It should sample exactly 1000 rows with replacement using a random seed of `42`.
3. It hardcodes the PCA `n_components` to 2. It needs to dynamically find the minimum number of components required to explain strictly greater than or equal to `85%` (0.85) of the variance.
4. It does not log the experiment. It must output a JSON file at `/home/user/tracking.json` containing the optimal components and the exact cumulative variance they explain.

Here is the current broken `/home/user/etl_diagnostic.py`:
```python
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import json

def run_diagnostics():
    # 1. Load data
    df = pd.read_parquet('/home/user/data.parquet')
    
    # 2. Bootstrap sampling (Currently missing!)
    # TODO: Take a bootstrap sample of 1000 rows with replacement (random_state=42)
    sample_df = df 
    
    # 3. Dimensionality Reduction
    # TODO: Find minimum n_components that explains >= 85% of variance
    pca = PCA(n_components=2)
    pca.fit(sample_df)
    
    # 4. Plotting (Failing in headless environment!)
    plt.figure()
    plt.plot(pca.explained_variance_ratio_.cumsum(), marker='o')
    plt.title('PCA Explained Variance')
    plt.show() 
    
    # 5. Tracking (Currently missing!)
    # TODO: Save the optimal n_components and its cumulative variance to /home/user/tracking.json
    # Format: {"n_components": int, "variance_explained": float}

if __name__ == "__main__":
    run_diagnostics()
```

Your task: Fix `/home/user/etl_diagnostic.py` and run it so that it correctly generates `/home/user/pca_plot.png` (a valid, non-empty image file) and `/home/user/tracking.json` according to the exact specifications above. Do not modify the data file `/home/user/data.parquet`.