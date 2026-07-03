You are helping a data researcher organize their laboratory datasets. 

The researcher has two CSV files located in `/home/user/data/`:
1. `notes.csv` - Contains the text notes for various experimental samples.
2. `metrics.csv` - Contains a binary `quality_label` (0 or 1) for the samples.

The researcher wrote a script at `/home/user/clean_pipeline.py` to merge these files:
```python
import pandas as pd

notes = pd.read_csv('/home/user/data/notes.csv')
metrics = pd.read_csv('/home/user/data/metrics.csv')

df = notes.merge(metrics, on='id', how='left')
df.to_csv('/home/user/data/cleaned_data.csv', index=False)
```

**The Problem:**
Because some samples in `notes.csv` do not have corresponding entries in `metrics.csv`, the left join introduces `NaN` values into the `quality_label` column. This silently causes pandas to cast the entire `quality_label` column from integers to floats (e.g., `1` becomes `1.0`). 

**Your Task:**
1. **Fix the Pipeline**: Modify `/home/user/clean_pipeline.py` to prevent this silent type casting. You must use pandas' nullable integer data type (`Int64`) for the `quality_label` column so that the valid labels remain integers (not floats) and the missing values remain standard pandas missing values. Run the script to generate `/home/user/data/cleaned_data.csv`.
2. **Setup Dependencies**: Install `scikit-learn` and `pandas` if you haven't already.
3. **Train and Predict**: Write a new script at `/home/user/predict.py` that does the following:
   - Reads `/home/user/data/cleaned_data.csv`.
   - Separates the data into a training set (rows where `quality_label` is not null) and a prediction set (rows where `quality_label` is null).
   - Uses `sklearn.feature_extraction.text.TfidfVectorizer` (with default parameters) to compute text embeddings of the `text` column.
   - Trains an `sklearn.linear_model.LogisticRegression` model (with `random_state=42` and default parameters) on the training set to predict `quality_label` from the text embeddings.
   - Predicts the `quality_label` for the missing row(s) in the prediction set.
4. **Output**: Save the predicted integer value(s) for the missing row(s) to a plain text file at `/home/user/data/prediction.txt`, with one integer per line.

Ensure your scripts execute successfully and the final files `/home/user/data/cleaned_data.csv` and `/home/user/data/prediction.txt` are created.