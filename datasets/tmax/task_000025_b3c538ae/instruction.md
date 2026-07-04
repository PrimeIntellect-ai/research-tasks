You are a mobile build engineer migrating our legacy build pipeline tools. We have a legacy Ruby script that calculates the deterministic build order of mobile modules based on their dependencies (using a topological sort with alphabetical tie-breaking). We are moving this logic to a Python-based gRPC microservice architecture.

Your task is to translate the dependency resolution logic into Python, integrate it with Protobuf, and prove its correctness using property-based testing.

Here is what you need to do:

1. **Install Dependencies**: Install `grpcio-tools`, `protobuf`, `pytest`, and `hypothesis` using pip.
2. **Compile Protobuf**: We have a protobuf file at `/home/user/build_graph.proto`. Compile it to generate the Python data classes in `/home/user/`.
3. **Translate Logic**: Look at the legacy Ruby script at `/home/user/legacy_solver.rb`. It computes a deterministic build order (if A depends on B, B must be built first. Ties are broken alphabetically). Implement this exact logic in Python in `/home/user/solver.py`.
   - Your python file must expose a function: `def resolve_build_order(graph_pb)`.
   - `graph_pb` is an instance of the `BuildGraph` protobuf message.
   - The function must return a `BuildOrder` protobuf message.
   - If a cycle is detected, raise a `ValueError("Cycle detected")`.
4. **Property-Based Testing**: Create `/home/user/test_solver.py`. Use the `hypothesis` library to generate arbitrary valid build graphs (without cycles) and test your Python function. 
   - Your test must verify the core property: For any module in the generated `BuildGraph`, all of its dependencies MUST appear *before* it in the resulting `BuildOrder.ordered_modules` list.
   - Also test that the number of modules in the output matches the input.
5. **Run Tests**: Execute your tests using `pytest /home/user/test_solver.py` and pipe the output to `/home/user/test_report.txt`.

The `/home/user/build_graph.proto` file contains:
```proto
syntax = "proto3";

message Module {
  string name = 1;
  repeated string depends_on = 2;
}

message BuildGraph {
  repeated Module modules = 1;
}

message BuildOrder {
  repeated string ordered_modules = 1;
}
```

The `/home/user/legacy_solver.rb` file contains:
```ruby
def resolve(modules)
  in_degree = Hash.new(0)
  adj = Hash.new { |h, k| h[k] = [] }
  
  modules.each do |mod|
    in_degree[mod[:name]] ||= 0
    mod[:depends_on].each do |dep|
      adj[dep] << mod[:name]
      in_degree[mod[:name]] += 1
      in_degree[dep] ||= 0
    end
  end

  queue = in_degree.select { |_, v| v == 0 }.keys.sort
  result = []

  while !queue.empty?
    # pop first alphabetically
    u = queue.shift
    result << u
    
    adj[u].each do |v|
      in_degree[v] -= 1
      if in_degree[v] == 0
        queue << v
        queue.sort!
      end
    end
  end

  raise "Cycle detected" if result.size != in_degree.size
  result
end
```