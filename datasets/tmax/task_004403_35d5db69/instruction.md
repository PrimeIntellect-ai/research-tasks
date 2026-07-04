You are a data scientist tasked with cleaning and linking two distinct user datasets to generate content recommendations. The company has an e-commerce platform and a community forum, but the user databases are separate and don't share IDs. 

Your task is to perform entity resolution using text similarity to join the datasets, and then generate recommendations.

**Input Data:**
You have two datasets located in `/home/user/data/`:
1. `/home/user/data/ecommerce.csv`: Contains columns `id`, `name`, `about`, `purchases`.
2. `/home/user/data/forum.csv`: Contains columns `fid`, `username`, `signature`, `topics`.

**Instructions:**
1. Install necessary Python libraries in your environment (e.g., `pandas`, `scikit-learn`).
2. Write a Python script to join the datasets based on profile similarity. 
3. For the similarity search:
   - Construct a profile document for e-commerce users by concatenating `name` and `about` with a single space (e.g., `name + " " + about`).
   - Construct a profile document for forum users by concatenating `username` and `signature` with a single space.
   - Use `sklearn.feature_extraction.text.TfidfVectorizer` (with default parameters) to vectorize the combined corpus of both e-commerce and forum profile documents.
   - Compute the cosine similarity between the e-commerce profiles and the forum profiles.
4. Link each e-commerce user to the forum user with the **highest** cosine similarity score. 
5. **Threshold:** Only keep the match if the cosine similarity score is strictly greater than `0.45`. If an e-commerce user has no match above this threshold, skip them.
6. Generate recommendations: For each matched e-commerce user, recommend the topics from their matched forum profile. The `topics` column contains a semicolon-separated string of topics (e.g., `sports;news`). Split this string into a Python list of strings.
7. Save the final recommendations to `/home/user/output/recommendations.json`. The JSON file should contain a single dictionary where the keys are the e-commerce `id`s (as strings) and the values are the lists of recommended topics (as lists of strings).

Create the `/home/user/output/` directory if it does not exist. Ensure your script is executed and the JSON file is created exactly at the specified path.