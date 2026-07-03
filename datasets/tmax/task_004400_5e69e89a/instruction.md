You are helping a researcher organize and analyze their datasets. They have two CSV files containing text fragments that need to be merged and analyzed for similarity. 

The files are located at:
1. `/home/user/primary.csv` - Contains columns `record_id` (integer), `description` (text), and `link_code` (string).
2. `/home/user/secondary.csv` - Contains columns `link_code` (string) and `extra_notes` (text). Not all `link_code`s from the primary dataset exist in the secondary dataset.

Your task:
1. Perform a left join of `primary.csv` with `secondary.csv` using `link_code`.
2. Construct a combined `document` string for each row by joining the `record_id`, `description`, and `extra_notes` with a single space. 
   * **Crucial requirement:** Due to the left join, some rows will have missing `extra_notes`. In pandas, this often causes related integer columns to silently cast to floats if you aren't careful, or it introduces literal "nan" strings. Ensure that the `record_id` is represented strictly as an integer string (e.g., "1001", NEVER "1001.0") and treat missing `extra_notes` as empty strings. 
   * Example correct document format: `"1001 Data science is great Needs more data"` or `"1002 Machine learning models are cool "` (trailing space is fine).
3. Compute TF-IDF embeddings for the resulting `document` column using `sklearn.feature_extraction.text.TfidfVectorizer` with all default parameters.
4. Compute the pairwise cosine similarity matrix for all documents.
5. Identify the pair of *distinct* records that have the highest cosine similarity.
6. Write the integer `record_id`s of this pair, in ascending numerical order separated by a comma, to `/home/user/closest_pair.txt` (e.g., `1042,1089`).

Use Python to accomplish this task. You can create and run scripts in the `/home/user` directory.