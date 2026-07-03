You are an ML engineer preparing a specialized dataset for a new language model. You have been given a raw JSONL dataset and need to orchestrate a data processing pipeline using Bash and Python. 

Your tasks are to:
1. **Environment Setup**: Create a Python virtual environment at `/home/user/venv` and install `tokenizers` and `numpy`.
2. **Tokenizer Training**: Write a Python script to train a Byte-Pair Encoding (BPE) tokenizer from scratch using the Hugging Face `tokenizers` library on the text from `/home/user/raw_data.jsonl`. 
    - Use the `Whitespace` pre-tokenizer.
    - Set the vocabulary size to 500.
    - Save the trained tokenizer to `/home/user/bpe_tokenizer.json`.
3. **Dataset Preparation & Statistical Filtering**: Write another script (or extend the same one) to encode all texts in the dataset using your newly trained tokenizer.
    - Extract the sequence of token IDs for each text.
    - Calculate the token sequence length for each text.
    - Use `numpy` to calculate the exact 85th percentile of token lengths across the entire dataset.
    - Filter the dataset to keep ONLY the records where the token length is strictly LESS THAN the 85th percentile threshold.
4. **Reporting**: Output the filtered results to a CSV file at `/home/user/filtered_dataset.csv`.
    - The CSV must have exactly two columns: `id` and `token_length`.
    - Include a header row.
    - The rows must be sorted in ascending order by `id`.

The raw data is located at `/home/user/raw_data.jsonl` and each line is a JSON object with the format: `{"id": <int>, "text": "<string>"}`.