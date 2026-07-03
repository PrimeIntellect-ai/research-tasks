As a Machine Learning Engineer, you are tasked with preparing a raw dataset for training and generating a feature plot on a headless Linux server. You must set up your environment, write a script to process the data, and output the clean data and a visualization.

Here are the requirements:

1. **Environment Setup**: Install any necessary tools or libraries (e.g., pandas, matplotlib) in the provided environment.
2. **Read Data**: Load the dataset located at `/home/user/raw_data.csv`.
3. **Data Schema Enforcement**: The final dataset must contain exactly three columns: `A`, `B`, and `C`. Ensure they are all cast to `float64`. Drop any other columns present in the raw data.
4. **Missing Value Handling**: 
   - Drop any rows where column `A` contains missing (`NaN`) values.
   - For column `B`, fill any missing values with the mean of the remaining valid values in column `B` (calculated *after* dropping rows missing `A`).
5. **Outlier Handling**: Clip the values of column `C` to its 5th and 95th percentiles (calculated *after* the previous missing value handling steps). Values below the 5th percentile should be replaced by the 5th percentile, and values above the 95th should be replaced by the 95th percentile.
6. **Plotting**: Generate a scatter plot with column `B` on the x-axis and column `C` on the y-axis. Save the plot to `/home/user/scatter.png`. *Note: You are operating on a headless Linux server. Ensure your plotting library backend is configured properly to output an actual image file instead of crashing or producing a blank plot.*
7. **Save Data**: Export the processed dataset to `/home/user/cleaned_data.csv` as a comma-separated values file without the row indices.

Complete these steps using a language and scripts of your choice. Ensure `/home/user/cleaned_data.csv` and `/home/user/scatter.png` exist and are correct upon completion.