You are helping a researcher organize and prepare a dataset for a text classification task. The researcher has written a Go program to tokenize text messages into integer IDs, but they suspect there is a "data leakage" bug in their pipeline. 

Currently, the script `/home/user/prepare_data.go` reads `/home/user/dataset/messages.csv`, builds a vocabulary from *all* the messages, and then splits the data into an 80% training set and a 20% test set (sequentially). Because the vocabulary includes words that only appear in the test set, information from the test set is leaking into the training pipeline.

Your task:
1. Fix the bug in `/home/user/prepare_data.go`. You must modify the logic so that the vocabulary is built **only** using the first 80% of the dataset (the training set). 
2. Ensure that any words in the test set that were not seen in the training set are assigned the ID `0` (which represents `<UNK>`).
3. Have the script output the tokenized test set to `/home/user/test_features.csv`. Each line should be a comma-separated list of integer IDs representing the tokenized text.
4. Create a benchmarking file `/home/user/prepare_data_test.go` containing a standard Go benchmark named `BenchmarkTokenize` that benchmarks the `Tokenize(text string, vocab map[string]int) []int` function using a sample string "hello world this is a test" and a dummy vocabulary.

Requirements for `test_features.csv`:
- Only contain the tokenized arrays of the test set (the last 20% of the messages).
- Format: plain text, one row per message, comma-separated integers (e.g., `4,0,12,0`). No brackets or labels.
- Do not change the existing basic whitespace-splitting logic in `prepare_data.go`, only fix the leakage and output format.

Once you have fixed the script, run it to generate `/home/user/test_features.csv` and ensure your benchmark runs successfully via `go test -bench .`.