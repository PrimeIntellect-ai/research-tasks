You are an MLOps engineer tasked with reviving a legacy predictive pipeline. We need to predict customer Lifetime Value (LTV) using a proprietary, undocumented feature extractor left behind by a former team member. 

Here is what you have:
1. Raw transactional data: `/home/user/data/transactions.csv` containing columns `tx_id`, `user_id`, `amount`, `timestamp`.
2. Target labels: `/home/user/data/targets.csv` containing columns `user_id`, `ltv`.
3. A legacy feature extractor: An undocumented, stripped binary located at `/app/feat_encode`.

Your objective:
1. **Tabular Aggregation**: Process `transactions.csv` to create user-level features. You must compute the `total_amount`, `tx_count`, and `avg_amount` per `user_id`. Save this aggregated dataset as a CSV (with headers `user_id,total_amount,tx_count,avg_amount` sorted by `user_id`).
2. **Embedding Computation**: Figure out how to run the `/app/feat_encode` binary on your aggregated CSV to generate customer embeddings. You may need to inspect the binary (e.g., using `strings` or `objdump`) to determine its expected command-line arguments. 
3. **Cross-Validation & Hyperparameter Tuning**: Using the generated embeddings as your feature matrix and the LTV values as your targets, train a scikit-learn regression model (e.g., Ridge Regression or Random Forest). You must use cross-validation (e.g., GridSearchCV or RandomizedSearchCV) to tune the hyperparameters of your chosen model.
4. **Serialization**: Save your best fitted model to exactly `/home/user/model.joblib` using the `joblib` library. The model should be ready to accept a 2D numpy array of embeddings and predict the `ltv` values.

An automated test suite will load your saved model and evaluate its performance against a held-out test set. Your model must achieve an MSE (Mean Squared Error) of less than 2.5 on this hidden dataset.