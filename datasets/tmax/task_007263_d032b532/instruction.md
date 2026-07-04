We are in the process of migrating a legacy Python 2 text analysis system to a modern, high-performance polyglot architecture (Python 3, C++, and Rust). As part of this migration, the core data aggregation component is being rewritten. 

We need you to design a gRPC/Protobuf interface, implement the core custom data structure in C++, and fix a bug in our new Rust client.

**Step 1: Protobuf Design**
Create a file at `/home/user/aggregator.proto` with `syntax = "proto3";` and package `migration`.
Define a service `Aggregator` with two RPCs:
1. `Record(RecordRequest) returns (RecordResponse);`
2. `GetTop(TopRequest) returns (TopResponse);`

Define the messages:
- `RecordRequest`: contains a single string field `item` (tag 1).
- `RecordResponse`: contains a boolean `success` (tag 1).
- `TopRequest`: contains an integer `limit` (tag 1).
- `TopResponse`: contains a repeated string `items` (tag 1).

**Step 2: Custom Data Structure in C++**
We are replacing the Python 2 `collections.Counter` logic with a specialized C++ class. 
Create `/home/user/FrequencyStore.h` and `/home/user/FrequencyStore.cpp`. 
Implement a class `FrequencyStore` with the following public methods:
- `void record(const std::string& item);`
- `std::vector<std::string> get_top(int limit);`

The `FrequencyStore` must keep track of the count of each `item`. When `get_top(limit)` is called, it should return the top `limit` items sorted by frequency in descending order. If frequencies are tied, sort them lexicographically (alphabetically) in ascending order. (e.g., if "apple" and "banana" both have count 2, "apple" comes first).

**Step 3: Fix the Rust Client**
We have a Rust client located in `/home/user/rust_client`. It parses a log file and is supposed to send the items to our service (the network code is mocked out for this test). 
Currently, the Rust client fails to compile due to a borrow checker/ownership error in `/home/user/rust_client/src/main.rs`.
Fix the compilation error without changing the structure of the mocked network call or the log parsing logic. 

**Step 4: Verification**
Once you have created the protobuf file, implemented the C++ data structure, and fixed the Rust client, compile and run the Rust client by executing:
```bash
cd /home/user/rust_client
cargo run > /home/user/rust_output.log
```
Ensure `/home/user/rust_output.log` is generated successfully.