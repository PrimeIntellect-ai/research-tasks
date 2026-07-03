I am a machine learning researcher trying to organize a large-scale text corpus for training a custom neural network. I have raw text data and a vocabulary, but I need you to build a reproducible data processing and testing pipeline.

You need to perform the following tasks entirely in `/home/user/`:

1. **Tokenization & Large-scale Storage**: 
   - Read the raw text corpus located at `/home/user/corpus.txt` and the vocabulary dictionary at `/home/user/vocab.json`.
   - Tokenize the text by splitting on single spaces. Map each word to its integer ID using `vocab.json`. If a word is not in the vocabulary, map it to the ID of the `<unk>` token (which is also defined in the vocabulary).
   - Save the resulting integer sequence to a memory-mapped numpy array (`numpy.memmap`) located at `/home/user/dataset.bin`. 
   - The memmap must use the `int32` data type (`np.int32`), mode `w+`, and its shape should be a 1D array equal to the total number of tokens in the corpus.

2. **Model Architecture Reconstruction**:
   - Write a Python script to define a specific PyTorch model.
   - The model must be a subclass of `torch.nn.Module` with three layers executed in this exact sequence:
     1. An `Embedding` layer with `num_embeddings` equal to the total number of keys in `vocab.json` (including `<unk>`) and an `embedding_dim` of 16.
     2. A `Linear` layer with `in_features=16` and `out_features=8`.
     3. A `ReLU` activation function.
   
3. **Numerical Accuracy Testing & Inference**:
   - In your script, before initializing the model, you **must** set the PyTorch manual seed to 42 exactly: `torch.manual_seed(42)`.
   - Load the first 100 tokens from your `dataset.bin` memmap array.
   - Convert these 100 tokens into a PyTorch long tensor (`torch.long`).
   - Pass this tensor through your initialized model to get an output tensor.
   - Calculate the mean and standard deviation (unbiased, which is PyTorch's default) of this entire output tensor.

4. **Reporting**:
   - Create a JSON file at `/home/user/metrics.json` containing exactly these keys:
     - `"total_tokens"`: the integer count of the total tokens processed and stored in the memmap.
     - `"output_mean"`: the float value of the output tensor's mean.
     - `"output_std"`: the float value of the output tensor's standard deviation.

Ensure your code is modular and handles dependencies correctly. If `torch` or `numpy` are not installed, you will need to install them using `pip`. Do not modify `corpus.txt` or `vocab.json`.