You are a data analyst tasked with building a C++ data processing pipeline to score users based on their activity logs using a Naive Bayes model.

You have been provided with two input sources:
1. `/app/priors.png`: An image containing the prior probabilities and conditional likelihoods for our Bayesian model. You will need to extract these parameters (using OCR tools like `tesseract`, which is installed).
2. `/home/user/raw_data.csv`: A log of user actions. The CSV has three columns: `user_id`, `timestamp`, and `feature_type`. The `feature_type` is always either `F1` or `F2`.

Your tasks are to:
1. Extract the Bayesian parameters from `/app/priors.png`. The image lists the prior probabilities for two classes ($C=0$ and $C=1$) and the likelihoods of features $F1$ and $F2$ given each class.
2. Write a C++ program that reads `/home/user/raw_data.csv` and performs an ETL aggregation. For each `user_id`, count the number of times they triggered `F1` and `F2`.
3. In the same C++ program, calculate the posterior probability of class 1 ($C=1$) for each user using the Naive Bayes formula. Use the log-sum-exp trick or direct calculation: 
   $Score_0 = \ln(P(C=0)) + count(F1) \cdot \ln(P(F1|C=0)) + count(F2) \cdot \ln(P(F2|C=0))$
   $Score_1 = \ln(P(C=1)) + count(F1) \cdot \ln(P(F1|C=1)) + count(F2) \cdot \ln(P(F2|C=1))$
   $P(C=1 | F1, F2) = \frac{e^{Score_1}}{e^{Score_0} + e^{Score_1}}$
4. Output the results to `/home/user/results.csv`. The output must have exactly two columns: `user_id` and `prob_1`, sorted by `user_id` in ascending order. `prob_1` should be the probability calculated above, printed to 6 decimal places.

Requirements:
- The core data parsing, aggregation, and mathematical computation MUST be implemented in C++. You may use shell scripts or Python solely for the OCR extraction step to get the parameters if you prefer, but the ETL and modeling must be a compiled C++ program.
- Ensure your output file has a header: `user_id,prob_1`.