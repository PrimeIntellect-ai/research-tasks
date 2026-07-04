You are an ML Engineer tasked with fixing a flawed machine learning pipeline and optimizing its performance.

We have a script located at `/app/model_pipeline.py` that trains a classification model on a large dataset stored at `/app/data/dataset.parquet`. Currently, the script has a critical methodological flaw: data leaks between the train and test sets during preprocessing. 

Additionally, we have received hyperparameters and tuning instructions as an image from the research team, located at `/app/data/instructions.png`.

Your tasks:
1. **Extract Instructions**: Use OCR (e.g., `tesseract`) to read `/app/data/instructions.png` and find the specific tuning grid, cross-validation strategy, and random states required.
2. **Fix Data Leakage**: Modify `/app/model_pipeline.py` to ensure absolutely no data leaks between the train and test splits. Use a proper scikit-learn `Pipeline` to encapsulate preprocessing and modeling. Apply the `train_test_split` with the `random_state` specified in the image and a `test_size` of 0.2.
3. **Hyperparameter Tuning**: Implement the tuning strategy specified in the image to find the best model. Optimize for ROC AUC.
4. **Hypothesis Testing / Confidence Intervals**: Evaluate the best model on your test split. Then, compute the 95% confidence interval for the ROC AUC score on this test split using 1000 bootstrap iterations. Save the interval to `/app/ci.txt` in the format `lower_bound,upper_bound` (e.g., `0.812,0.855`).
5. **Serialization**: Save your fitted, tuned `Pipeline` (the best model from your search) to `/app/best_model.pkl` using `joblib`.

A holdout verification script will later load `/app/best_model.pkl` and evaluate its ROC AUC on a hidden dataset to ensure it meets our quality thresholds and correctly processes raw, unscaled inputs. Ensure your saved model expects raw features and scales them internally.