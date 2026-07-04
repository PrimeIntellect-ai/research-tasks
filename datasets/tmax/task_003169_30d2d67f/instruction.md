You are an AI assistant helping a data science researcher organize and classify a small text dataset. 

The researcher has a dataset of short messages split into "spam" and "ham" (normal messages). They want to build a reproducible pipeline in Go to tokenize the text, train a simple Naive Bayes classifier from scratch, and evaluate it.

The dataset is located at:
`/home/user/dataset/train/spam/`
`/home/user/dataset/train/ham/`
`/home/user/dataset/test/spam/`
`/home/user/dataset/test/ham/`

Your task is to write a Go program at `/home/user/classifier.go` that does the following:

1. **Tokenization and Dataset Preparation**:
   - Read all text files from the train and test directories.
   - For each file, convert the text to lowercase.
   - Replace any character that is not a lowercase letter (a-z) or digit (0-9) with a space.
   - Split the resulting string by whitespace to get a slice of tokens. Ignore empty tokens.

2. **Model Training (Naive Bayes)**:
   - Compute the global vocabulary size $|V|$ (the number of unique tokens across the entire training set, both spam and ham).
   - Calculate the prior probabilities for each class $c \in \{\text{spam}, \text{ham}\}$:
     $P(c) = \frac{\text{Number of training documents in class } c}{\text{Total number of training documents}}$
   - Calculate the conditional probabilities for each token $w$ given class $c$ using Laplace smoothing (+1):
     $P(w|c) = \frac{\text{Count of token } w \text{ in class } c + 1}{\text{Total tokens in class } c + |V|}$
   *Note: "Total tokens in class c" is the sum of occurrences of all tokens in that class's training documents. "Count of token w in class c" is how many times w appears in documents of class c.*

3. **Inference and Evaluation**:
   - For each document in the test set, calculate the log-probability score for each class:
     $\text{Score}(c) = \ln(P(c)) + \sum_{w \in \text{document}} \ln(P(w|c))$
     *(Only include tokens in the test document that exist in the training vocabulary. Ignore out-of-vocabulary tokens).*
   - Predict the class with the highest score. If the scores are exactly equal, predict "ham".
   - Compute the accuracy on the test set (number of correct predictions divided by total test documents).

4. **Output**:
   - The program should output a JSON file to `/home/user/results.json` with exactly this structure:
     ```json
     {
       "vocab_size": 123,
       "test_accuracy": 0.85
     }
     ```
   *(Use the actual calculated vocabulary size and accuracy as a float).*

Write the code, compile it, and run it to produce `/home/user/results.json`.