You are a data analyst working for an e-commerce company. Due to a system glitch, our latest batch of product reviews contains duplicate entries. We need you to clean this data, calculate summary statistics, and generate a final markdown report.

You have been provided with two files:
1. `/home/user/reviews.csv`: A CSV file containing the raw reviews. 
   The columns are: `ReviewID`, `Timestamp`, `UserID`, `ProductID`, `Rating`, `ReviewText`.
2. `/home/user/template.md`: A markdown template for reporting.

Your tasks are:

**1. Hash-based Deduplication**
Parse `/home/user/reviews.csv` and remove duplicate entries. A review is considered a duplicate if it has the exact same `UserID`, `ProductID`, and `ReviewText` as another row. 
* To perform this deduplication, you must compute a SHA-256 hash of the string formed by concatenating these three fields separated by a pipe character: `UserID|ProductID|ReviewText`.
* If multiple rows produce the same hash, keep only the row with the **earliest** `Timestamp` (chronologically) and discard the others. 

**2. Summary Statistics**
Using the deduplicated data, calculate the following metrics for each unique `ProductID`:
* `TotalReviews`: The total number of valid (deduplicated) reviews for the product.
* `AverageRating`: The mean `Rating` of the valid reviews for the product, rounded to exactly two decimal places (e.g., "4.50").

**3. Template-based Text Generation**
Using `/home/user/template.md`, generate a final report named `/home/user/summary_report.md`.
The template file contains:
```markdown
## Product: {{ProductID}}
- Total Reviews: {{TotalReviews}}
- Average Rating: {{AverageRating}}
```

Your final `/home/user/summary_report.md` must start with exactly this header:
```markdown
# Product Review Summary
```
Followed by a blank line, and then the populated template for each product. 
* The products must be sorted alphabetically by `ProductID`.
* Separate each product's section with a single blank line.

You may use any programming language (e.g., Python, Bash, AWK) available on the system to complete this task. Write your code, execute it, and ensure `/home/user/summary_report.md` is perfectly formatted according to the instructions.