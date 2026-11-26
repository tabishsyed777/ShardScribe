# ShardScribe
Reconstruct a short archival excerpt from overlapping, unordered transcriptions. Exact subset search returns a shortest text containing every fragment, the first character offset of each input, and whether another equally short text exists. Ties resolve lexicographically.

## Try it
With Python 3.12 or 3.13, from this directory:
```sh
python3 app.py example.json
python3 -m unittest discover -s tests -v
```
The demo joins dawn, awning and ingot into **dawningot**. Edit the fragments array to try your own case. Offsets are zero-based Unicode character indices. Matching respects spaces and case. The solver accepts up to 12 fragments of 256 characters each because the exact search grows exponentially. Historical accuracy still requires an original source. Typos and missing characters can change the result.

## Verification
Tests include exhaustive permutation comparisons on 40 seeded four-fragment scenarios, ambiguous assemblies, malformed inputs, and a real CLI invocation from another working directory.
