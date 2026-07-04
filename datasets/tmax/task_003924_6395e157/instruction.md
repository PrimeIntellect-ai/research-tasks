You are a machine learning engineer tasked with preparing a baseline model for a resource-constrained embedded system. Because of the target hardware constraints, the baseline model and evaluation pipeline must be written entirely in C from scratch, without using external machine learning libraries.

You have been provided with two datasets in your home directory:
1. `/home/user/features.csv` - Contains sensor readings. Format: `id,f1,f2,f3`
2. `/home/user/labels.csv` - Contains the ground truth labels. Format: `id,label` (Labels are binary: 0 or 1).

Note: The rows in the two files are NOT in the same order.

Your task is to write a C program at `/home/user/evaluate_knn.c` that does the following:
1. **Multi-source Data Joining**: Read both CSV files and join the features and labels based on the `id` field. You can assume there are exactly 100 records and IDs are integers from 1 to 100.
2. **Model Implementation**: Implement a k-Nearest Neighbors (k-NN) classifier using the Euclidean distance metric.
3. **Hyperparameter Tuning & Evaluation**: Implement Leave-One-Out Cross-Validation (LOOCV) to evaluate the accuracy of your k-NN classifier for $k \in \{1, 3, 5, 7\}$. For the prediction, use a simple majority vote among the $k$ nearest neighbors.
4. **Output**: Identify the $k$ value that yields the highest LOOCV accuracy. If there is a tie, prefer the smaller $k$. Write the result to a file named `/home/user/best_model.txt` in the exact following format:
`Best k: [k_value], Accuracy: [accuracy_percentage]%`
(Format the percentage to exactly two decimal places, e.g., `Best k: 3, Accuracy: 95.00%`).

Compile and run your C program to generate the output file. You may use standard C libraries (`stdio.h`, `stdlib.h`, `math.h`, `string.h`). Compile your code with `-lm` to link the math library.