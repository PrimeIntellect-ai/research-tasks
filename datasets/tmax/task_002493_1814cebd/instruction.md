You are an automation specialist creating a data processing workflow. We receive a high volume of chat messages in a continuous stream, and we need to detect spam/bot behavior by finding messages that are highly similar to recently sent messages, even if they use Unicode tricks or different languages. 

Your task is to write a Python script `/home/user/detect_spam.py` that processes a large JSONL file line-by-line and flags messages that meet a specific similarity threshold within a rolling time window.

### Instructions

1. **Input File**: You will process `/home/user/chat_stream.jsonl`. Each line is a JSON object with the following schema:
   `{"id": "string", "timestamp": integer, "text": "string"}`
   *Note: You must stream this file line-by-line. Do not load all records into memory at once, as the real file can be larger than available RAM.*

2. **Text Normalization**: Before comparing messages, normalize the `text` field:
   - Convert the string to lowercase.
   - Normalize the string using the `NFKD` Unicode normalization form.
   - Remove all characters EXCEPT basic ASCII alphanumeric characters (`a-z` and `0-9`).

3. **Feature Extraction**: Convert the normalized string into a set of character bigrams (overlapping sequences of 2 characters). For example, "hello" becomes `{"he", "el", "ll", "lo"}`. If the normalized text has fewer than 2 characters, it has no bigrams (an empty set).

4. **Rolling Window Aggregation**: 
   Maintain a rolling window of recent messages. A message is considered "recent" for a new message if:
   `current_message.timestamp - 60 < previous_message.timestamp < current_message.timestamp`
   *(The window is exactly 60 seconds, exclusive of the lower bound, exclusive of the upper bound since timestamps monotonically increase).*

5. **Similarity Computation**:
   For each new message, compute the Jaccard similarity between its bigram set and the bigram sets of all valid messages currently in the rolling window.
   - $Jaccard(A, B) = \frac{|A \cap B|}{|A \cup B|}$
   - If both sets are empty, the similarity is `0.0`.
   - The threshold for flagging a message is a Jaccard similarity $\ge 0.75$.

6. **Output Generation**:
   Create a CSV file at `/home/user/flagged_messages.csv` with the following headers:
   `id,matched_id,similarity_score`
   - If a message exceeds the threshold with *multiple* messages in the window, select the one with the highest similarity score.
   - If there is a tie in similarity scores, select the oldest message (the one with the smallest timestamp).
   - Format the `similarity_score` to exactly 3 decimal places (e.g., `0.769`, `1.000`).
   - Only include flagged messages in the CSV.

Run your script to produce `/home/user/flagged_messages.csv`.