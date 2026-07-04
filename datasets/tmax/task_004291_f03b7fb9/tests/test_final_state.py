# test_final_state.py

import os
import stat

def test_files_exist():
    """Ensure all required files exist."""
    assert os.path.isfile("/home/user/sparql_gen.cpp"), "Source file /home/user/sparql_gen.cpp is missing."
    assert os.path.isfile("/home/user/sparql_gen"), "Executable /home/user/sparql_gen is missing."
    assert os.path.isfile("/home/user/generate.sh"), "Script /home/user/generate.sh is missing."
    assert os.path.isfile("/home/user/queries.sparql"), "Output file /home/user/queries.sparql is missing."

def test_executables():
    """Ensure the compiled binary and bash script are executable."""
    gen_stat = os.stat("/home/user/sparql_gen")
    assert gen_stat.st_mode & stat.S_IXUSR, "/home/user/sparql_gen is not executable."

    sh_stat = os.stat("/home/user/generate.sh")
    assert sh_stat.st_mode & stat.S_IXUSR, "/home/user/generate.sh is not executable."

def test_queries_sparql_content():
    """Check that the generated SPARQL queries match the expected output exactly."""
    expected_content = """PREFIX ex: <http://example.org/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?paper ?title ?year ?citations
WHERE {
  ?paper ex:hasSubject <ex:MachineLearning> .
  ?paper foaf:title ?title .
  ?paper ex:year ?year .
  ?paper ex:citations ?citations .
  FILTER(?year >= 2018)
}
ORDER BY DESC(?citations) ASC(?paper)
LIMIT 50
OFFSET 0

PREFIX ex: <http://example.org/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?paper ?title ?year ?citations
WHERE {
  ?paper ex:hasSubject <ex:Bioinformatics> .
  ?paper foaf:title ?title .
  ?paper ex:year ?year .
  ?paper ex:citations ?citations .
  FILTER(?year >= 2020)
}
ORDER BY DESC(?year) ASC(?paper)
LIMIT 10
OFFSET 20

PREFIX ex: <http://example.org/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?paper ?title ?year ?citations
WHERE {
  ?paper ex:hasSubject <ex:QuantumComputing> .
  ?paper foaf:title ?title .
  ?paper ex:year ?year .
  ?paper ex:citations ?citations .
  FILTER(?year >= 2015)
}
ORDER BY DESC(?citations) ASC(?paper)
LIMIT 100
OFFSET 50
"""

    with open("/home/user/queries.sparql", "r") as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), "The contents of /home/user/queries.sparql do not match the expected output."