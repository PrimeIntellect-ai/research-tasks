I am an ML engineer preparing training data for a new model. I wrote a C++ data preparation pipeline located at `/home/user/pipeline.cpp`. The pipeline is supposed to:
1. Read user demographic features from `/home/user/features.csv`.
2. Read pre-computed embeddings from `/home/user/embeddings.csv`.
3. Perform an inner join on the `id` column (which is the first column in both files).
4. Perform bootstrap sampling to draw exactly 50 samples from the joined dataset.
5. Write the sampled results to `/home/user/sampled_data.csv`.

However, the pipeline is currently broken and non-reproducible:
- **Empty Output Bug**: The output file is empty because the join logic is failing. The code incorrectly attempts to parse `embeddings.csv` using space delimiters, but the file is actually comma-separated. 
- **Reproducibility Issue**: The bootstrap sampler uses a non-deterministic random seed (`std::random_device`).

Please fix the C++ code to resolve these issues:
1. Fix the delimiter parsing so it correctly reads `embeddings.csv` and successfully joins the datasets.
2. Make the sampling strictly reproducible. Replace `std::random_device` with a fixed seed of `42`.
3. **Crucial:** Because `std::uniform_int_distribution` can vary between compiler standard libraries, compute the random index strictly using the raw engine output modulo the size: `size_t index = gen() % joined_data.size();` (do not use `std::uniform_int_distribution`).

Once you have fixed the code, compile it using `g++ -O3 -std=c++11 /home/user/pipeline.cpp -o /home/user/pipeline` and run it to generate the `/home/user/sampled_data.csv` file. 

The output CSV must contain the joined data (ID, features, then embeddings) in a comma-separated format.