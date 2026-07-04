You are an MLOps engineer tasked with reviving a legacy feature engineering pipeline for a machine learning experiment.

A previous engineer left a raw dataset at `/home/user/raw_data.csv` (containing 1000 samples and 50 raw features, some of which contain missing values or are highly correlated). They also left a compiled, stripped legacy evaluation binary at `/app/score_features`. 

Your objective is to create a fully reproducible Python script at `/home/user/pipeline.py` that processes the raw dataset and extracts a dense, highly informative representation.

Requirements for `/home/user/pipeline.py`:
1. It must read `/home/user/raw_data.csv`.
2. It must handle missing values appropriately and perform necessary feature scaling/engineering.
3. It must perform dimensionality reduction to reduce the dataset to exactly **10** features.
4. It must output the transformed data to `/home/user/final_features.csv` (comma-separated, no headers, no index, exactly 1000 rows and 10 numeric columns).
5. Ensure any necessary Python packages (like `pandas` and `scikit-learn`) are installed in your environment.

The legacy binary `/app/score_features` acts as an oracle. When you run `/app/score_features /home/user/final_features.csv`, it will evaluate your reduced features against hidden labels and output an accuracy score. 

You must optimize your `pipeline.py` so that the feature representation achieves an accuracy score of **at least 0.85** when evaluated by the binary.