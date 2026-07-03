You are helping a researcher organize their dataset processing and model training workflow. They have a script that joins multi-source data, trains a neural network, and benchmarks inference, but it has several issues:
1. It suffers from a data leakage bug during scaling (the scaler is fitted on the entire dataset before splitting).
2. The model architecture hardcoded in the script is outdated. The correct architecture parameters are saved in an image at `/app/arch.png`.
3. The data joining logic is incomplete. The data is split across three files in `/home/user/data/`: `features_A.csv`, `features_B.csv`, and `labels.csv`. They need to be inner-joined on the `uuid` column.

Your tasks:
1. Inspect the image `/app/arch.png` (using OCR tools like `tesseract`, which you may need to install/configure) to extract the correct `MLPClassifier` hyperparameters.
2. Refactor the researcher's workflow into a single Python script `/home/user/train_and_benchmark.py`.
3. Read and inner-join the three CSV files on `uuid`.
4. Fix the data leakage by constructing a scikit-learn `Pipeline` that chains a `StandardScaler` and the `MLPClassifier`.
5. Initialize the `MLPClassifier` inside the pipeline with the parameters extracted from the image. Set `random_state=42` and `max_iter=500`.
6. Split the joined data into train and test sets (80/20 split, `random_state=42`).
7. Train the `Pipeline` on the training set.
8. Implement an inference performance benchmark in the script: time how long it takes to run `pipeline.predict()` on the test set 100 times in a loop, and print the average inference time in milliseconds.
9. Save the fitted `Pipeline` object to `/home/user/solution_pipeline.joblib` using `joblib`.

Ensure all dependencies are installed. You can run your script to generate the joblib file. Your success will be evaluated based on the accuracy of your saved pipeline on a hidden holdout dataset, which requires the exact model architecture and a leakage-free scaling process.