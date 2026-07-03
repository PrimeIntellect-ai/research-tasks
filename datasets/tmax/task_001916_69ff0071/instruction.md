You are a machine learning engineer preparing a data preprocessing pipeline for a new 4-class classification model. 

Part of the training data preparation requires normalizing raw input features using a specific weighted log-sum-exp function. The weights for the four features were documented by researchers in a scanned snippet of a spreadsheet, which has been saved to `/app/weights.png`. 

Your task is to write a Go program that reads batches of raw feature vectors, applies the weighted log-sum-exp transformation using the exact weights extracted from the image, and outputs the normalized values.

Because the raw features can be extremely large or small (e.g., in the range of `[-2000, 2000]`), a naive implementation of $y = \log \sum_{i=1}^4 \exp(w_i x_i)$ will result in numerical instability (overflows to `+Inf` or underflows to `-Inf`/`NaN`). You MUST implement the standard "log-sum-exp trick" for numerical stability to pass the tests.

**Requirements:**
1. Extract the four weights ($w_1, w_2, w_3, w_4$) from `/app/weights.png`. You may use OCR tools like `tesseract` which are preinstalled.
2. Write a Go program at `/home/user/normalize.go`.
3. The program must read lines from standard input (`stdin`).
4. Each line will contain exactly 4 comma-separated float64 values: $x_1, x_2, x_3, x_4$.
5. For each line, compute the numerically stable log-sum-exp: $y = \max_i(w_i x_i) + \log \sum_{i=1}^4 \exp(w_i x_i - \max_i(w_i x_i))$.
6. Print the result to standard output (`stdout`), formatted to exactly 6 decimal places (e.g., `fmt.Printf("%.6f\n", result)`).
7. Compile your program to an executable located at `/home/user/normalize`.

An automated fuzzer will stream thousands of random extreme values into your program and compare the outputs bit-for-bit against a reference implementation to ensure numerical stability and correct weight application.