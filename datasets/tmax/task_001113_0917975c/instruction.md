You are a data analyst tasked with cleaning, transforming, and merging employee survey data. 

You have been provided with regional survey results in wide-format CSV files located in `/home/user/survey_data/`. There are three files: `survey_NA.csv`, `survey_EU.csv`, and `survey_APAC.csv`. 

Each survey file has the following header:
`emp_id,q1_satisfaction,q2_workload,q3_culture,q4_management`

You also have a metadata file located at `/home/user/metadata.csv` with the header:
`emp_id,hire_year,office_city`

Your goal is to write a script (in a language of your choice) to process these files and generate a single, cleaned, long-format CSV file at `/home/user/clean_long_survey.csv`. 

**Requirements:**
1. **Parallel Processing:** You must read and process the three regional survey files in parallel (e.g., using Python's `multiprocessing` or `concurrent.futures`, or GNU `parallel` in bash).
2. **Data Validation (Constraints):** 
   - `emp_id` MUST be exactly 8 characters long, starting with "EMP" followed by exactly 5 digits (e.g., `EMP01234`).
   - All question scores (`q1_satisfaction`, `q2_workload`, `q3_culture`, `q4_management`) MUST be integers between 1 and 10 (inclusive).
   - If any row in the survey data violates these constraints (invalid ID, missing score, or out-of-bounds score), you must **drop** the entire row.
3. **Reshaping:** Convert the valid survey data from wide format to long format. The new format should have three columns: `emp_id`, `question`, and `score`. The `question` column should contain the column names (e.g., `q1_satisfaction`).
4. **Joining:** Merge the reshaped survey data with the `metadata.csv` file using `emp_id` as the key. Keep only the records that exist in both the valid survey data and the metadata (Inner Join).
5. **Output Formatting:**
   - The final output must be saved to `/home/user/clean_long_survey.csv`.
   - The header must be exactly: `emp_id,hire_year,office_city,question,score`
   - The rows must be sorted alphabetically by `emp_id` (ascending), and then alphabetically by `question` (ascending).

Write and execute the necessary code to produce `/home/user/clean_long_survey.csv`.