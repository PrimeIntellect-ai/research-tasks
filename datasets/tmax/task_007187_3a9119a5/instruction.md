You are a data analyst who needs to process some CSV files using C. You have two datasets located in your home directory:
1. `/home/user/users.csv` - Contains user features. Columns: `user_id,f1,f2,f3`
2. `/home/user/weights.csv` - Contains user-specific weights. Columns: `user_id,w1,w2,w3`

Your task is to write a C program that performs the following steps:
1. Reads both CSV files and joins them on `user_id`. (You can assume `user_id` is an integer and there are at most 1000 users. The datasets might not be sorted).
2. For each user present in both files, computes a `score` using the dot product of their feature vector and weight vector: `score = (f1 * w1) + (f2 * w2) + (f3 * w3)`.
3. Filters the users, keeping only those who have a `score >= 50.00`.
4. Writes the result to a new file `/home/user/output.csv` with the header `user_id,score`. The `score` must be formatted to exactly 2 decimal places (e.g., `52.50`).
5. The rows in `output.csv` must be sorted by `user_id` in ascending integer order.

Requirements:
- Write your C code to `/home/user/processor.c`.
- Compile it to an executable named `/home/user/processor` using `gcc`.
- Run the executable so that `/home/user/output.csv` is generated.