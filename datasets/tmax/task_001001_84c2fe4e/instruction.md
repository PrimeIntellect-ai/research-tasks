You are a data analyst tasked with building a custom K-Nearest Neighbors (KNN) classifier in C++ to process some tabular CSV files. 

We have a vendored copy of the `rapidcsv` C++ library located at `/app/rapidcsv/`. However, our previous engineer mentioned that something is currently wrong with how it parses standard comma-separated files out of the box. You will need to identify and fix the issue in the vendored library before you can use it.

Your objective is to:
1. Fix the vendored `rapidcsv` package.
2. Write a C++ program (e.g., `classifier.cpp`) that reads `/home/user/features.csv` and `/home/user/labels.csv`. Both files have a `user_id` column. You must join the features and labels on this `user_id`.
3. Implement a simple K-Nearest Neighbors algorithm (using Euclidean distance) in your C++ code. The features are all continuous numeric values, and the label is a binary integer (0 or 1).
4. Perform 5-fold cross-validation in your C++ program to find the optimal hyperparameter `k` (search `k` in the range `[1, 15]`, considering odd numbers only). 
5. Once the best `k` is found, train on the full joined dataset and generate predictions for the test dataset at `/home/user/test_features.csv`.
6. Output the predictions to `/home/user/predictions.csv` with exactly two columns: `user_id,prediction`. 

Notes:
- You may use standard C++ libraries (`<vector>`, `<cmath>`, `<algorithm>`, etc.).
- Compile your code using `g++ -std=c++17 -I /app/rapidcsv/src classifier.cpp -o classifier`.
- The evaluation will compare your `/home/user/predictions.csv` against a hidden ground-truth file using Accuracy as the metric. Your accuracy must be strictly greater than 0.85.