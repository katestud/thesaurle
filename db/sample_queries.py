import mgclient
import csv

conn = mgclient.connect(host="127.0.0.1", port=7687)
cursor = conn.cursor()

def fetch_all_nodes():
    query = "MATCH (n:Word) RETURN n.name"
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]

def fetch_shortest_path_length(start, end):
    query = """
    MATCH path=(n:Word {name: $start_word})-[relationships:SYNONYM *BFS]->(m:Word {name: $end_word})
    RETURN length(path) AS path_length;
    """
    cursor.execute(query, {'start_word': start, 'end_word': end})
    result = cursor.fetchone()
    return result[0] if result else float('inf')

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
  ('en', 'sn'),
  ('spec', 'coke'),
  ('merchant', 'carrot'),
  ('merchant', 'wonderland')
]

for start, end in random_associations:
  print(f"======================{start} TO {end}=====================")
  path = fetch_shortest_path(start, end)
  print_path(path)


def fetch_all_nodes():
    query = "MATCH (n:Word) RETURN n.name"
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]

def fetch_words_within_hops(start, min_hops, max_hops, limit):
    query = f"""
    MATCH path=(n:Word {{name: $start_word}})-[relationships:SYNONYM *BFS {min_hops}..{max_hops}]->(m:Word)
    RETURN m.name, length(path) AS path_length LIMIT {limit}
    """
    cursor.execute(query, {'start_word': start})
    return cursor.fetchall()

# all_nodes = fetch_all_nodes()

# with open('results.csv', 'a', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     for node in all_nodes:
#         words_within_hops = fetch_words_within_hops(node, 5, 9, 20)
#         for word, distance in words_within_hops:
#             csvwriter.writerow([node, word, distance])

# Close connection
conn.close()

