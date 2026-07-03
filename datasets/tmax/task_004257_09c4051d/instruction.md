I need you to process a large dataset of sales transactions, but the specific filtering and aggregation constraints were left for me in an audio voice memo. 

First, listen to the audio file located at `/app/data_request.mp3` and transcribe the constraints.
Next, process the large CSV file at `/home/user/transactions.csv`. You must write a Python script that loads this data (you may use SQLite in-memory or a local database file to leverage indexes and optimize the query plan), applies the exact filtering constraints mentioned in the audio, and performs a cross-query aggregation to summarize the total sales amount by product category.

Output the final aggregated data as a JSON file at `/home/user/summary.json` with the following schema:
```json
{
  "categories": [
    {
      "category_name": "string",
      "total_sales": float
    }
  ]
}
```

Make sure your Python script is optimized, as the dataset is large. You will be evaluated on the accuracy of your numeric aggregation.