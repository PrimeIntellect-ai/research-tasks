You are a Machine Learning Engineer tasked with preparing a clean training dataset by filtering out noisy documents, and then tuning a baseline model on the cleaned data. You must implement the following pipeline in Python.

Your task has three phases. Write and execute a script (or scripts) to accomplish this end-to-end workflow:

**Phase 1: Environment and Data Loading**
1. Install `scikit-learn`, `numpy`, and `pandas`.
2. Using `sklearn.datasets.fetch_20newsgroups`, load the training subset for the categories `['comp.graphics', 'sci.space']`. 
   * Ensure you use `subset='train'` and `remove=('headers', 'footers', 'quotes'), random_state=42`.

**Phase 2: Embedding Computation and Outlier Removal (Linear Algebra)**
1. Compute TF-IDF embeddings for the documents using `TfidfVectorizer(max_features=1000, stop_words='english')`.
2. Apply dimensionality reduction using `TruncatedSVD(n_components=50, random_state=42)` to generate dense 50-dimensional embeddings.
3. For each of the two classes (categories), calculate the class centroid (the mean vector of the 50-dimensional embeddings for all documents belonging to that class).
4. Compute the Cosine Similarity between each document's 50-dimensional vector and its corresponding class centroid.
5. Filter the dataset by discarding the 10% of documents in *each class* that have the lowest cosine similarity to their class centroid. (Calculate the drop count for a class as `int(class_size * 0.10)` and drop that many documents. Keep the rest.)

**Phase 3: Cross-validation and Hyperparameter Tuning**
1. Using the remaining "cleaned" dataset and their 50-dimensional SVD embeddings, perform hyperparameter tuning using `GridSearchCV`.
2. The model to tune is `RidgeClassifier(random_state=42)`.
3. Search over the `alpha` values: `[0.1, 1.0, 10.0]`.
4. Use standard 5-fold cross-validation (`cv=5`).

**Output Requirements**
Once the pipeline is complete, generate a JSON file at `/home/user/ml_prep_results.json` with exactly the following keys:
* `"original_size"`: (integer) The total number of documents before filtering.
* `"clean_size"`: (integer) The total number of documents after filtering.
* `"best_alpha"`: (float) The optimal `alpha` value found by GridSearchCV.
* `"best_cv_score"`: (float) The best mean cross-validated score found by GridSearchCV, rounded to exactly 4 decimal places.

Your work will be verified by checking the contents of `/home/user/ml_prep_results.json`.