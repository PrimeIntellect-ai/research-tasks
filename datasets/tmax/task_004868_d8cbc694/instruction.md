I need you to act as a data analyst processing some raw data exports. I have three large CSV files representing tables from a relational database, but I don't remember the exact foreign key relationships. Fortunately, I have a screenshot of the schema diagram. 

Your task is to write a highly efficient C++ program that reads these CSV files, joins them according to the relationships shown in the schema image, and exports the data into a nested JSON document format.

Here are the requirements:
1. Examine the image at `/app/schema_diagram.png` (using OCR or vision tools) to determine how the three CSV files (`/app/users.csv`, `/app/orders.csv`, and `/app/items.csv`) relate to each other.
2. Write a C++ program at `/home/user/join_to_json.cpp` that reads these three CSV files.
3. The program must perform the necessary joins and construct a single JSON array of user objects. Each user object should contain their details and an array of their `orders`. Each order object should contain its details and an array of its `items`.
4. Skip users with no orders, and skip orders with no items.
5. Write the resulting JSON to `/home/user/result.json`.
6. Compile your program as `/home/user/join_to_json` using `g++ -O3 -std=c++17 /home/user/join_to_json.cpp -o /home/user/join_to_json`.

The CSV files contain hundreds of thousands of rows. A naive nested-loop join will be far too slow. You must design an efficient in-memory indexing strategy (e.g., using hash maps) to ensure the program processes the data and outputs the JSON very quickly.

Output JSON structure example:
```json
[
  {
    "user_id": "1",
    "user_name": "Alice",
    "orders": [
      {
        "order_id": "101",
        "order_date": "2023-01-01",
        "items": [
          {
            "item_id": "1001",
            "item_name": "Widget",
            "price": "10.50"
          }
        ]
      }
    ]
  }
]
```

We will run a verification script that measures the execution time of `/home/user/join_to_json`. It must run in under 1.5 seconds.