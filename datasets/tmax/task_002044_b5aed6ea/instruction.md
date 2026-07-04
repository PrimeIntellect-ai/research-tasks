You are an assistant helping a researcher process a dataset of environmental audio recordings. The researcher wants to find similar acoustic events using a custom pipeline.

Your task is to build an ETL pipeline to process an audio dataset, perform feature extraction, apply dimensionality reduction, and execute a similarity search.

The audio file is located at: `/app/research_audio.wav`

Perform the following steps exactly as described:
1. **ETL / Chunking:** Read the audio file (it has a sample rate of 16000 Hz and is exactly 60 seconds long). Split the audio array into 60 consecutive 1-second chunks (16000 samples each). Chunk 0 is the first second, Chunk 1 is the second, etc.
2. **Feature Extraction:** For each chunk, compute the magnitude of the Real Fast Fourier Transform (using `numpy.fft.rfft` and `numpy.abs`). This will yield 8001 frequency components.
3. **Binning:** Reduce the 8001 components into 32 equal-sized buckets. Use `numpy.array_split(spectrum, 32)` and compute the mean of each bucket to get a 32-dimensional feature vector per chunk.
4. **Dimensionality Reduction:** Create a feature matrix of shape `(60, 32)`. Center the data by subtracting the mean of each column. Apply Principal Component Analysis (PCA) to reduce the dimensionality to exactly 4 components. You may use `sklearn.decomposition.PCA(n_components=4)`.
5. **Similarity Search:** Calculate the cosine similarity between the 4-dimensional representation of **Chunk 0** and all other chunks (Chunks 1 through 59). 
6. **Recommendation:** Find the top 5 chunks most similar to Chunk 0. 

Create a CSV file at `/home/user/top5.csv` with exactly two columns: `chunk_id` and `similarity`. 
The file should contain a header and the 5 rows of your top recommendations, sorted in descending order of similarity.

Note: You can install any standard Python data science libraries (like `numpy`, `scipy`, `scikit-learn`) using `pip`.