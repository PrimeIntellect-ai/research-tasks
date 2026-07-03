I am a researcher organizing a text dataset from multiple sources, and I'm running into some issues on my headless Linux server. I need you to complete the data processing pipeline and fix a broken plotting script.

Here is what you need to do:

1. **Data Joining and Tokenization:**
   I have two dataset files:
   - `/home/user/articles.jsonl` (contains `article_id` and `text`)
   - `/home/user/metadata.jsonl` (contains `article_id` and `source`)
   
   Write a Python script at `/home/user/prepare_dataset.py` that reads both files, performs an inner join on `article_id`, and creates a new column called `tokens`. 
   To generate the `tokens`, lowercase the `text` field and extract all alphanumeric sequences using the regular expression `[a-z0-9]+`.
   Add another column called `token_count` which is the integer length of the `tokens` list.
   Save the joined and processed DataFrame as a Parquet file at `/home/user/processed_corpus.parquet`. 

2. **Fix the Plotting Script:**
   I wrote a script at `/home/user/plot_distribution.py` to plot the distribution of token counts from the Parquet file. However, it crashes or hangs because it tries to open a graphical window, and this server doesn't have a display/X11 configured.
   Modify `/home/user/plot_distribution.py` so that it uses a headless matplotlib backend, does not attempt to open a GUI window, and successfully saves the plot to `/home/user/token_distribution.png`.

3. **Execution:**
   Run your data processing script to generate the Parquet file, and then run the fixed plotting script to generate the PNG file.

Ensure that `/home/user/processed_corpus.parquet` and `/home/user/token_distribution.png` exist and are correctly formatted when you are finished. You can install any standard Python packages (like `pandas`, `pyarrow`, `matplotlib`) using `pip` if they are not already installed.