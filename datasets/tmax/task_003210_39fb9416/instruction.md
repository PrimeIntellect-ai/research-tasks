You are a Machine Learning Engineer preparing a data pipeline for a statistical primer sequence alignment model. As part of your workflow, you need to extract ground truth data from an annotated image, run regression tests via a Jupyter Notebook, and deploy a Bash-based optimization service for primer selection.

Perform the following steps:

1. **Information Extraction**:
   There is an annotated electrophoresis gel image at `/app/reference_gel.png`. Use optical character recognition (OCR) to extract the target reference sequence from the image. The image contains a line of text in the format `TARGET_SEQ: <sequence>`. Extract just the sequence (e.g., `ATGC...`) and save it into a file named `/app/target_sequence.txt`.

2. **Regression Testing**:
   There is a scientific regression test suite inside `/app/regression.ipynb` that verifies the statistical distribution of the dataset based on your extracted sequence. Execute this notebook headlessly in-place (e.g., using `jupyter nbconvert --execute --inplace`). The notebook will read `/app/target_sequence.txt`. Make sure the execution succeeds. You may need to install `jupyter` and any required dependencies.

3. **Bash Optimization Service**:
   Write a lightweight HTTP server entirely in Bash (you may use tools like `socat` or `nc`) that listens on `127.0.0.1:8080`.
   - The service must accept `GET` requests to the endpoint `/optimize?min_len=<N> HTTP/1.1`.
   - When a request is received, the server must parse the `min_len` parameter (an integer).
   - It should then read `/app/candidates.csv` (which contains lines formatted as `PrimerID,Sequence`).
   - The optimization task: Filter the candidates to keep only those where the length of the `Sequence` is strictly greater than or equal to `min_len`. Among these valid candidates, find the one that has the highest alignment score with the target sequence (from `/app/target_sequence.txt`).
   - *Alignment score definition*: The number of matching characters at the exact same index position between the target sequence and the candidate sequence (Hamming-style similarity, up to the length of the shorter sequence). In case of a tie in the highest score, pick the candidate that appears first in the CSV.
   - The server must respond with a valid HTTP 200 response:
     ```
     HTTP/1.1 200 OK
     Content-Type: text/plain
     Content-Length: <length>
     
     <PrimerID>
     ```

Leave your Bash HTTP server running in the background. The verification suite will send several HTTP requests to `127.0.0.1:8080` with different `min_len` values and verify the returned `PrimerID`.