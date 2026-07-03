You are an MLOps engineer tasked with recovering lost experiment tracking metadata. A previous engineer trained several models but forgot to log their evaluation metrics. The model artifacts are saved in the `/home/user/models/` directory as `.pkl` files.

You have been provided with the evaluation dataset:
- Features: `/home/user/X.npy`
- Target outputs: `/home/user/y_target.npy`

Your task is to:
1. Write a Python script to load each scikit-learn model from the `/home/user/models/` directory.
2. Run inference using each model on the features in `X.npy`.
3. Evaluate the predictions by calculating the Mean Squared Error (MSE) between the model's predictions and `y_target.npy`.
4. Identify the model that produces the lowest MSE.
5. Write the exact filename of the best performing model (e.g., `model_something.pkl`) to a file named `/home/user/best_model.txt`.

Ensure your evaluation is accurate and outputs only the filename of the best model to the specified text file.