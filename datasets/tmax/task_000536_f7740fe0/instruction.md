You are an data engineer troubleshooting a broken ETL pipeline on a headless Linux server.

There is a Python script located at `/home/user/etl_pipeline.py` that processes numerical data from `/home/user/data.csv`. The script is intended to:
1. Load the data.
2. Perform Principal Component Analysis (PCA) to reduce the data to 2 dimensions.
3. Generate a scatter plot of the two principal components.

However, the pipeline is currently failing for two reasons:
1. The raw dataset contains missing values (`NaN`), which causes the PCA computation to crash.
2. The script is configured to display the plot interactively using `plt.show()`, which crashes in our headless environment due to the lack of an X server.

Your task:
1. Modify `/home/user/etl_pipeline.py` to handle the missing values by imputing them with the **mean of each column** *before* running PCA.
2. Fix the matplotlib configuration in the script so that it operates headlessly (using the `Agg` backend) and successfully saves the plot to `/home/user/pca_plot.png` instead of trying to show it.
3. Add code to the script to save the PCA-transformed data (the 2 principal components) to a CSV file at `/home/user/output.csv`. The CSV must have exactly two columns with the header `PC1,PC2`, and the float values should be rounded to 4 decimal places.
4. Run the fixed script to generate both `/home/user/pca_plot.png` and `/home/user/output.csv`.

Do not change the random states or standard scaling steps already present in the script.