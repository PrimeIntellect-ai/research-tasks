You are acting as a bioinformatics analyst. We need to build a high-performance sequence analysis pipeline to find the best alignment score of a specific DNA motif within a large target genome sequence.

Your task consists of the following steps:

1. **Extract the Motif (Image processing):** 
   There is an image file located at `/app/motif_reference.png` containing the reference motif sequence we need to search for. Use OCR (e.g., `tesseract`) to extract the text. The image contains a string in the format `MOTIF: <SEQUENCE>`. Extract just the `<SEQUENCE>` (which consists of A, C, G, T characters).

2. **Develop the Scoring Engine (C & Parallel Computing):**
   A long target DNA sequence is located at `/home/user/target.txt`. 
   Write a C program at `/home/user/motif_scorer.c` that computes the alignment score of the extracted motif against every possible starting position in the target sequence.
   - **Scoring rule:** For a motif of length $L$, compare it to a substring of length $L$ in the target. Award +1 for each matching character and -1 for each mismatching character. 
   - **Domain Decomposition & Parallelism:** You must use OpenMP to parallelize the search. Divide the target sequence into chunks (domain decomposition) so multiple threads can evaluate different sliding windows concurrently.
   - The program should output the maximum score achieved and the 0-based index in the target sequence where this maximum score occurs (if there is a tie, output the lowest index).

3. **Serve the Results (Network Service):**
   Deploy a network service listening on `127.0.0.1:8080`. 
   When this service receives an HTTP GET request to `/score`, it must execute your C program (or use its pre-computed output) and respond with a `200 OK` HTTP status and a JSON body containing the results:
   `{"max_score": <int>, "index": <int>}`
   You can implement the server directly in C, or use tools like `nc`, `socat`, or a bash script to serve the HTTP response. The service must stay running in the background.

Constraints:
- You must write the core computation in C (`/home/user/motif_scorer.c`).
- You must compile the C program with OpenMP enabled (`-fopenmp`).
- The network service must run on `127.0.0.1:8080`.