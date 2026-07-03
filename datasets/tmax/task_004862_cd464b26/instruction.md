You are a data analyst tasked with building a robust data processing pipeline tool. 

We receive streams of CSV data containing text snippets and probability metrics. You need to write a standalone CLI program located at `/home/user/processor`. This program must be executable directly (e.g., if you write it in Python, include a `#!/usr/bin/env python3` shebang and run `chmod +x /home/user/processor`, or compile a binary to that exact path). 

Your program will be rigorously tested against a stream of automated inputs.

Here are the requirements for `/home/user/processor`:

1. **Information Extraction**:
   There is an image file located at `/app/priors.png` containing the text `BAYES_PRIOR=0.XX` (where `0.XX` is a float). Use OCR (e.g., Tesseract) to extract this prior probability value. Your program should use this extracted value internally as `P(H)`.

2. **Data Ingestion & Tokenization**:
   The program must read a headerless CSV from `standard input` (`stdin`). Each line follows the format: `Text_Data,Float_X,Float_Y`.
   For each row, tokenize `Text_Data` by splitting it strictly on whitespace. Count the number of resulting tokens.

3. **Covariance & Bayesian Analysis**:
   After reading all rows from `stdin`, calculate:
   - The **population covariance** between `Float_X` and `Float_Y`.
   - The **Bayesian Posterior Probability** $P(H | Data)$. 
     - Prior $P(H)$ is the value extracted from the image.
     - Likelihood $P(Data | H)$ is the product of all `Float_X` values in the dataset.
     - Likelihood $P(Data | \neg H)$ is the product of all `Float_Y` values in the dataset.
     - Calculate the posterior using Bayes' theorem. If the denominator is exactly 0, the posterior should evaluate to `0.0000`.

4. **Output Format**:
   Your program must print strictly to `stdout` in the following format (all floats must be rounded to exactly 4 decimal places):
   
   First, reproduce the dataset substituting the text with the token count:
   ```
   [TokenCount_1],[Float_X_1],[Float_Y_1]
   [TokenCount_2],[Float_X_2],[Float_Y_2]
   ...
   ```
   Then, print an empty line.
   Finally, print the computed metrics:
   ```
   COVARIANCE: [Value]
   POSTERIOR: [Value]
   ```

Do not include any other output, debugging logs, or prompts on `stdout`.