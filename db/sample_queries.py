import mgclient

conn = mgclient.connect(host="127.0.0.1", port=7687)
cursor = conn.cursor()

start_word = 'sale'
end_word = 'green'

def fetch_shortest_path(start, end, max_hops=None):
    if max_hops:
      query = f"""
      MATCH path=(n:Word {{name: $start_word}})-[relationships:SYNONYM *BFS ..{max_hops}]->(m:Word {{name: $end_word}})
      RETURN nodes(path);
      """
    else:
      query = """
      MATCH path=(n:Word {name: $start_word})-[relationships:SYNONYM *BFS]->(m:Word {name: $end_word})
      RETURN nodes(path);
      """
    cursor.execute(query, {'start_word': start, 'end_word': end})
    return cursor.fetchall()

# Given a tuple result of nodes from a `fetchall` query, print the nodes names
def print_path(path):
    for row in path:
        for item in row[0]:
            print(item.properties['name'])

print("======================SHORTEST PATH=====================")
print(fetch_shortest_path(start_word, end_word))

print("======================SHORTEST PATH UP TO 10=====================")
print(fetch_shortest_path(start_word, end_word, 10))

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

random_associations = [
  ('faithful', 'cheat'),
  ('subway', 'lattice'),
  ('carver', 'chill'),
  ('sale', 'green'),
  ('audience', 'crowd'),
  ('purchase', 'sale'),
  ('outreach', 'boulder'),
  ('en', 'sn')
]

for start, end in random_associations:
  print(f"======================{start} TO {end}=====================")
  path = fetch_shortest_path(start, end)
  print_path(path)


# Close connection
conn.close()

