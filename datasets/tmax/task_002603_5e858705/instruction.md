You are a data analyst tasked with processing data from two systems to calculate a final mathematical metric for our users. 

You have two files located in `/home/user`:
1. `/home/user/users.csv`: A standard UTF-8 encoded CSV containing user metadata.
   Columns: `user_id,username,multiplier`
2. `/home/user/scores.csv`: A UTF-16LE encoded CSV containing raw user scores.
   Columns: `user_id,score1,score2,score3`

Your objective is to write a Rust program (save it as `/home/user/process.rs`) that:
1. Reads and appropriately decodes both files.
2. Joins the data on `user_id`.
3. Calculates a `final_score` for each user. The mathematical formula for the final score is the Euclidean norm of the three scores, multiplied by the user's multiplier:
   `final_score = sqrt(score1^2 + score2^2 + score3^2) * multiplier`
4. Sorts the users in descending order based on their `final_score`.
5. Writes the result to `/home/user/result.csv` in UTF-8 format.

The output file `/home/user/result.csv` must have exactly the following format (including the header):
```csv
username,final_score
```
The `final_score` must be rounded to exactly two decimal places (e.g., `56.12`, `20.00`). 

To complete the task:
- Write the Rust source code to `/home/user/process.rs`.
- Compile it using `rustc /home/user/process.rs`.
- Execute the compiled binary to generate `/home/user/result.csv`.
- You may use standard Unix commands (like `iconv`) to preprocess the files if you prefer not to handle the UTF-16LE decoding directly in Rust, but the joining, math, and sorting must be handled by your Rust code.