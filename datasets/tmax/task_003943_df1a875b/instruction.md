You are a Machine Learning Engineer preparing a text dataset for a new NLP model. Before proceeding with model training, you need to evaluate two different tokenization strategies to understand how they affect sequence lengths. 

You have been provided with a raw dataset of text snippets at `/home/user/raw_texts.csv`. The file has a header and two columns: `id` and `text`.

Your task is to write a Python script at `/home/user/evaluate_tokenizers.py` that does the following:
1. Reads the dataset.
2. Applies two tokenization strategies to each text:
   - **Strategy A (Whitespace):** Split the text by exactly one space character (i.e., using `text.split(' ')`).
   - **Strategy B (Alphanumeric words):** Extract all contiguous alphanumeric sequences using the regex `r'\w+'`.
3. Counts the number of tokens produced by each strategy for every text.
4. Performs statistical analysis on the sequence lengths:
   - Calculates the **Pearson correlation coefficient** between the token counts of Strategy A and Strategy B.
   - Conducts a **paired Student's t-test** comparing the token counts of Strategy A and Strategy B to check for a statistically significant difference in sequence lengths.
5. Saves the experiment metrics to a JSON file at `/home/user/experiment_results.json` with the following structure:
```json
{
  "correlation": <float>,
  "t_statistic": <float>,
  "p_value": <float>,
  "mean_length_A": <float>,
  "mean_length_B": <float>
}
```

Constraints:
- Use only Python standard libraries (e.g., `csv`, `re`, `json`, `math`, `statistics`) or `scipy`/`numpy` if already available in the standard Python data science environment. You are highly encouraged to use `scipy.stats.pearsonr` and `scipy.stats.ttest_rel` for the statistics.
- The output JSON values must be numbers (floats) rounded to exactly 4 decimal places.
- Do not modify the original data file.

Once you have written the script, execute it to generate the `/home/user/experiment_results.json` file.