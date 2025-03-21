import mgclient

# Connect to Memgraph
conn = mgclient.connect(host="127.0.0.1", port=7687)
cursor = conn.cursor()

start_word = 'sale'
end_word = 'green'

print("======================SHORTEST PATH=====================")
# Query to find the shortest path between two words, using BFS
query = """
MATCH path=(n:Word {name: $start_word})-[relationships:SYNONYM *BFS]->(m:Word {name: $end_word})
RETURN nodes(path);
"""
cursor.execute(query, {'start_word': start_word, 'end_word': end_word})
r = cursor.fetchall()
print(r)

print("======================SHORTEST PATH UP TO 10=====================")
# Query to find the shortest path between two words, using BFS, constrained to a particular length
query = """
MATCH path=(n:Word {name: $start_word})-[relationships:SYNONYM *BFS ..10]->(m:Word {name: $end_word})
RETURN nodes(path);
"""
cursor.execute(query, {'start_word': start_word, 'end_word': end_word})
r = cursor.fetchall()
print(r)

print("======================DIRECT RELATIONSHIP=====================")
# Query to print the direct relationship between two words, if it exists
query = """
MATCH (b:Word {name: 'sale'})-[r:SYNONYM]->(a:Word {name: 'purchase'})
RETURN b, r, a
"""
cursor.execute(query)
result = cursor.fetchall()
print(result)


print("======================SYNONYMS OF A NODE=====================")
query = """
MATCH (a:Word {name: 'audience'})-[r:SYNONYM]->(b:Word)
RETURN a, r, b
"""
cursor.execute(query)
results = cursor.fetchall()

for row in results:
    print(row)

# Close connection
conn.close()

