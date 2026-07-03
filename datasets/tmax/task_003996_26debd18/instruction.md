You are acting as a bioinformatics pipeline engineer. We have received a new batch of nanopore sequencing data, but the metadata for the run was recorded as a voice memo by the lab technician.

You need to process this data using a multi-language approach. Here are the steps:

1. **Extract Parameters from Audio**
   There is an audio file at `/app/lab_memo.wav`. It contains the lab technician's spoken notes. You need to transcribe or listen to this audio (you can install tools like `pocketsphinx` via pip, or analyze it however you see fit) to extract two crucial pieces of information:
   - The three initial mean values for the signal states.
   - The convergence tolerance for the EM algorithm.

2. **Signal Data Processing & Density Estimation**
   The raw nanopore current signal trace is located at `/app/nanopore_signal.txt` (one float per line). 
   You must implement a Gaussian Mixture Model (GMM) Expectation-Maximization (EM) algorithm from scratch in Python or R. **Do not use pre-built GMM fitters like `sklearn.mixture.GaussianMixture` or `mclust`.** You must write the EM loop yourself to properly handle our custom convergence testing.

3. **Convergence Testing**
   Initialize your three Gaussian components with the means extracted from the audio. Initialize the weights uniformly (1/3 each) and the variances to 1.0. 
   Iterate the EM algorithm until the absolute change in the log-likelihood of the dataset between consecutive iterations is strictly less than the convergence tolerance extracted from the audio.

4. **Integration and Output**
   Once the model converges, extract the final estimated means of the three components.
   Sort these three means in ascending order.
   Save them to exactly `/home/user/estimated_means.txt`, formatted with one floating-point number per line (e.g., `1.2345`).

Your final output will be verified quantitatively against the true hidden state parameters of the nanopore signal. A high-quality fit (low Mean Squared Error) is required.