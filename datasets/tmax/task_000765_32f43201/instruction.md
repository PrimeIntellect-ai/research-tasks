You are a data analyst troubleshooting a pipeline. A nightly job dumped a corrupted CSV file containing daily sales totals into `/home/user/sales.csv`. 

The file has two columns: `Date` (YYYY-MM-DD) and `Sales`. However, the rows are out of order, and several days are completely missing their `Sales` values.

Using only Bash built-ins and standard coreutils (like `awk`, `sed`, `sort`, `head`), process this file to find the 3 days with the highest 3-day rolling average of sales. 

Perform the following operations in your pipeline:
1. **Sorting**: Ignore the CSV header and sort the data chronologically by `Date`.
2. **Imputation**: Forward-fill any empty `Sales` values (if a day has no sales value, use the most recent available sales value from the sorted data). The first chronological day will always have a valid value.
3. **Rolling Statistics**: Compute a 3-day rolling average for the imputed sales. The rolling average for day $N$ is the integer floor of the mean of the sales on day $N$, day $N-1$, and day $N-2$. For the first two days, compute the integer floor mean of the available days up to that point. (e.g., day 1 is just day 1's sales; day 2 is the floor average of day 1 and 2).
4. **Ranking**: Sort the days by this rolling average in descending order. If there is a tie in the rolling average, break the tie by sorting the `Date` in ascending (earliest first) order.

Save the top 3 rows into `/home/user/top_rolling.csv` in the exact format:
`YYYY-MM-DD,RollingAvg`
(Do not include a header in the output file).