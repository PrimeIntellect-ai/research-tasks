You are a database administrator tasked with extracting dependency analytics from a company's microservice architecture graph. 

We store our architecture metadata as an RDF graph in a Turtle (`.ttl`) file located at `/home/user/architecture.ttl`. The graph uses the namespace `http://example.org/` and the predicate `http://example.org/dependsOn` to represent dependencies (e.g., ServiceA `dependsOn` ServiceB means ServiceA calls ServiceB).

Your task:
1. Formulate a SPARQL query to calculate the "in-degree centrality" of all services. Specifically, count how many unique services depend on each target service.
2. Identify the top 3 most critical services (the ones with the highest in-degree count). If there is a tie, sort them alphabetically by the service name (URI) in descending order.
3. Export these top 3 services and their in-degree counts to a JSON file at `/home/user/critical_services.json`.
4. Ensure your output strictly validates against the JSON schema provided at `/home/user/schema.json`.

The final JSON should look structurally like this (but with the actual computed values):
```json
{
  "top_services": [
    {
      "service_name": "http://example.org/ServiceX",
      "in_degree": 10
    }
  ]
}
```

You may use Python and install any necessary libraries (like `rdflib` and `jsonschema`) using `pip` to write a script that processes the data, executes the SPARQL query, and writes the output.