import mgclient
import sys
import os
import time

# WTF is this shit, how do python imports work!?
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dictionary import build_dictionary

# Connect to Memgraph
conn = mgclient.connect(host="127.0.0.1", port=7687)
cursor = conn.cursor()

# Wipe the database by deleting all nodes and relationships
cursor.execute("MATCH (n) DETACH DELETE n")
conn.commit()

synonyms = build_dictionary()

# Prepare data for bulk insert
nodes = [{"name": word} for word in synonyms.keys()]
relationships = [{"word": word, "syn": syn} for word, syns in synonyms.items() for syn in syns]

# Bulk insert nodes
# Takes roughly ~30 seconds
print("Inserting Nodes")
start_time = time.time()
cursor.execute("""
UNWIND $nodes AS node
MERGE (n:Word {name: node.name})
""", {"nodes": nodes})
end_time = time.time()
print(f"Time taken to insert nodes: {end_time - start_time} seconds")

# Bulk insert relationships
# Takes roughly ~7 minutes
print("Inserting Relationships")
start_time = time.time()
cursor.execute("""
UNWIND $relationships AS rel
MATCH (a:Word {name: rel.word})
MATCH (b:Word {name: rel.syn})
MERGE (a)-[:SYNONYM]->(b)
""", {"relationships": relationships})
end_time = time.time()
print(f"Time taken to insert relationships: {end_time - start_time} seconds")

conn.commit()

# Close connection
conn.close()
