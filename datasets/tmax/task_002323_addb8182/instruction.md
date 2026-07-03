You are tasked with building a robust, Bash-only ETL pipeline to generate user product recommendations. 

You have been provided with raw data in `/home/user/data/`:
1. `users.csv` (`user_id,age,region`)
2. `transactions.csv` (`tx_id,user_id,product_id,amount`)
3. `products.csv` (`product_id,category`)

**The Challenges:**
1. **Tooling Setup:** Your pipeline needs to perform fast grouping and aggregations. GNU `datamash` is perfect for this, but the system doesn't have it installed. The source code for `datamash-1.8` is pre-vendored at `/app/datamash-1.8`. However, the `configure` script was accidentally corrupted during a previous migration and fails immediately. You must find the deliberate syntax error in the `configure` script, fix it, compile the binary (you do not have root access, so use the compiled binary directly from the source tree), and use it in your pipeline.
2. **Silent Type Corruption (Missing Values):** The `transactions.csv` file has missing `amount` values (represented as empty fields, e.g., `101,1,55,`). If processed naively in Bash/awk, these evaluate to 0 or cause downstream type corruptions. You must impute any missing `amount` with the *integer average (floor)* of all valid transaction amounts for that specific `user_id`. If a user has no valid transactions, default to `0`.
3. **Multi-Source Join & Recommendation:** Join the imputed transactions with `products.csv` to map `product_id` to `category`. Then, calculate the total amount spent by each user per `category`. 
4. **Final Output:** For each `user_id`, output their top recommended category (the category where they spent the most in total). If there is a tie, select the category that comes first alphabetically.

**Requirements:**
- Write your entire pipeline in a script at `/home/user/pipeline.sh`.
- You may only use standard Bash utilities, `awk`, `sed`, `join`, `sort`, and your locally compiled `datamash`. No Python/Perl/Ruby.
- Your script must output the final recommendations to `/home/user/recommendations.csv` with the format `user_id,top_category` (sorted numerically by `user_id`). No header in the output.

Ensure your pipeline accurately processes the missing values and generates the correct recommendations. Your final `recommendations.csv` will be scored automatically against a hidden reference set.