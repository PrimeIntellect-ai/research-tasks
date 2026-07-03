You are an AI assistant helping a researcher organize their dataset of short scientific notes. They need a fast, custom C++ utility to perform simple text classification using a Naive Bayes model.

Your task is to write a C++ program that trains a Naive Bayes classifier from a labeled training set and predicts the labels of a test set.

**Dataset Files:**
*   `/home/user/train.tsv`: The training data. It is a tab-separated file where each line has a label (`0` or `1`) followed by a tab and then a short text.
*   `/home/user/test.txt`: The test data. Each line contains a short text to be classified.

**Requirements for the C++ Program (`/home/user/classifier.cpp`):**
1.  **Tokenization:** For every line of text (in both train and test), convert all letters to lowercase. Replace any non-alphanumeric character with a space character. Split the resulting string by whitespace to extract tokens.
2.  **Training (Bayesian Inference):**
    *   Identify the vocabulary $V$ as the set of all unique tokens present in the training data.
    *   Calculate the prior probability for each class based on the number of training examples.
    *   Calculate the likelihood of each word given each class using Laplace smoothing with $\alpha = 1$. The formula is:
        $P(w|c) = \frac{\text{count}(w, c) + 1}{\text{total\_words}(c) + |V|}$
        where $\text{count}(w, c)$ is the number of times token $w$ appears in texts of class $c$, $\text{total\_words}(c)$ is the total number of tokens across all texts in class $c$, and $|V|$ is the total number of unique tokens in the entire training dataset.
3.  **Prediction:**
    *   For each text in `/home/user/test.txt`, calculate the log-probability of each class given the tokens in the text:
        $\text{Score}(c) = \log(P(c)) + \sum_{w \in \text{text}} \log(P(w|c))$
        *(Note: If a token in the test text does not exist in the training vocabulary $V$, completely ignore it).*
    *   Predict the class (`0` or `1`) that yields the higher score. In case of a tie, predict `1`.
4.  **Output:**
    *   The program should write the predicted label (`0` or `1`) for each line of `/home/user/test.txt` to `/home/user/predictions.txt`, one label per line.

**Execution:**
Once you write `/home/user/classifier.cpp`, compile it using `g++ -O3 /home/user/classifier.cpp -o /home/user/classifier` and run it to produce `/home/user/predictions.txt`. Do not leave behind any other unnecessary files.