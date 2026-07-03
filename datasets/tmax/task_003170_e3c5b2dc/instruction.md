You are a database administrator working on optimizing a slow NoSQL aggregation query. The current query engine is too slow for our real-time requirements, so we are offloading the result processing and pagination to a specialized, high-performance C executable.

We have an image of the original NoSQL aggregation pipeline rules, which was exported by the data architect. It is located at `/app/pipeline.png`. You will need to extract the pipeline stages (filtering, sorting, and pagination/limits) from this image.

Your task is to write a C program that implements this exact aggregation pipeline and acts as a fast result processor.

Requirements:
1. Write your C source code to `/home/user/pipeline_exec.c` and compile it to `/home/user/pipeline_exec`.
2. The executable must read from standard input (`stdin`).
3. The input format will be:
   - The first line contains a single positive integer `N`, representing the pagination LIMIT.
   - The subsequent lines contain exported query results in CSV format: `id,status,age,score`.
     - `id` is an integer.
     - `status` is a string (up to 20 characters).
     - `age` is an integer.
     - `score` is an integer.
   - The input may contain up to 50,000 CSV rows.
4. Your program must apply the pipeline rules specified in `/app/pipeline.png`.
5. For the records that pass the pipeline and make it to the final result set, output them to standard output (`stdout`) in the following strict JSONL (JSON Lines) format:
   `{"id": <id>, "score": <score>}`
   (Ensure there is exactly one space after the colon, and a newline at the end of each JSON object).

Example of expected output format for a row with id 5 and score 100:
`{"id": 5, "score": 100}`

Compile the C code using GCC. Ensure that your sorting logic is highly efficient and matches the exact ordering rules specified in the image. Your program will be strictly verified against thousands of dynamically generated fuzz inputs to ensure exact behavioral equivalence with our reference processor.