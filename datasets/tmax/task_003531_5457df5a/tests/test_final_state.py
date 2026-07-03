# test_final_state.py
import tarfile
import re
import os

def test_final_docs_tarball_exists():
    path = "/home/user/final_docs.tar.gz"
    assert os.path.exists(path), f"Final docs tarball {path} does not exist. Did you create the final archive?"
    assert os.path.isfile(path), f"{path} is not a file."

def test_link_conversion_accuracy_and_api_doc():
    path = "/home/user/final_docs.tar.gz"
    assert os.path.exists(path), f"Final docs tarball {path} does not exist."

    correct_conversions = 0
    leftover_wiki_links = 0
    has_api_doc = False

    try:
        with tarfile.open(path, 'r:gz') as tar:
            for member in tar.getmembers():
                # Check for the generated API doc
                if member.name.endswith('deploy_api.md'):
                    has_api_doc = True

                # Process all markdown files for link checking
                if member.name.endswith('.md') and member.isfile():
                    f = tar.extractfile(member)
                    if f is not None:
                        content = f.read().decode('utf-8', errors='replace')

                        # Count leftover wiki links: [[Some Text]]
                        leftovers = len(re.findall(r'\[\[.*?\]\]', content))
                        leftover_wiki_links += leftovers

                        # Count correct new format links: [Some Text](Some_Text.md)
                        # We use the heuristic from the verifier to match the expected format
                        corrects = len(re.findall(r'\[(.*?)\]\(\1\.md\)', content.replace(' ', '_')))
                        correct_conversions += corrects
    except Exception as e:
        assert False, f"Failed to read or parse the tarball {path}: {e}"

    assert has_api_doc, "deploy_api.md is missing from the final archive. Did you generate the documentation using shdoc?"

    total = correct_conversions + leftover_wiki_links
    if total == 0:
        accuracy = 1.0
    else:
        accuracy = correct_conversions / total

    assert accuracy >= 0.95, f"Link conversion accuracy {accuracy:.2f} is below threshold 0.95. Correct: {correct_conversions}, Leftover: {leftover_wiki_links}."