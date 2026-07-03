You are a data analyst stepping into a project to fix a machine learning pipeline written in C++. 

We are training a simple Naive Bayes text classifier on a dataset of SMS messages (`/home/user/dataset.csv`) to predict whether a message is spam (1) or ham (0). 

A previous engineer wrote the code in `/home/user/naive_bayes.cpp`. The program tokenizes the text, calculates Bayesian prior probabilities and word conditional probabilities, and then evaluates the model on a hold-out test set (the last 20% of the data).

However, during a code review, we noticed a critical flaw: **Data Leakage**. The program currently builds its vocabulary and calculates word frequencies across the *entire* dataset before splitting it into training and testing sets. This means information from the test set is leaking into the model's tokenization and Bayesian probability estimations.

Your task:
1. Identify and fix the data leak in `/home/user/naive_bayes.cpp`. Refactor the code so that the vocabulary building, tokenization mapping, and probability frequency counting are *only* fitted on the training split. 
2. Ensure that any out-of-vocabulary words encountered in the test set (words that did not appear in the training set) are ignored during the test set probability calculation.
3. Compile the fixed C++ code into an executable named `/home/user/nb_classifier` (use `g++ -std=c++17`).
4. Run the executable and pipe its output to `/home/user/results.txt`.

The C++ program is already set up to print the following output:
```
Vocab Size: <integer>
Test Accuracy: <float>
```
Make sure the format of the output remains exactly as above. When you have generated `/home/user/results.txt` with the fixed model metrics, you are done.