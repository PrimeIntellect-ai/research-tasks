You are a machine learning engineer preparing training data for a product recommendation system. Your ETL pipeline requires a robust filtering step to remove spam reviews from the dataset.

Your task has the following steps:

1. **Extract Configuration:** We have provided an image file at `/app/config_spec.png` containing the specifications for the spam filter. Use an OCR tool (like `tesseract`, which is pre-installed) to read the configuration. The image contains a similarity threshold and a list of known spam template strings.

2. **Implement the Filter:** Write a Python script at `/home/user/spam_filter.py`. The script must take exactly one command-line argument: the path to a text file containing a single review.
   
   The script must determine if the review is spam by doing the following:
   - Read the input text file.
   - Use `sklearn.feature_extraction.text.TfidfVectorizer` with `stop_words='english'` to compute the TF-IDF vectors for the input text and all the spam templates (from the image) together.
   - Compute the Cosine Similarity between the input text and each spam template.
   - Find the maximum similarity score among all templates.
   - If the maximum similarity is strictly greater than or equal to the threshold extracted from the image, print exactly `EVIL` to standard output.
   - Otherwise, print exactly `CLEAN` to standard output.

3. **Verify:** You can test your script against any sample text files you create. An automated verifier will run your script against a hidden adversarial corpus of "evil" spam reviews and "clean" genuine reviews to ensure your filter works flawlessly and exactly matches the logic specified.

**Constraints & Notes:**
- Your output to standard output should be exactly `EVIL` or `CLEAN` followed by a newline, with no other text.
- Make sure to process the text exactly as specified using `scikit-learn`.
- Do not hardcode the path to the input file; read it from `sys.argv[1]`.