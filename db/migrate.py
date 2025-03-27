import mgclient
import time
import csv

DICTIONARY_FILE = "data/synonyms.tsv"

def read_dictionary_tsv(filename):
    synonym_dict = dict()
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
           if len(row) > 1:
            key = row[0]
            synonym_dict[key] = row[1].split(',')
    return synonym_dict

synonyms = read_dictionary_tsv(DICTIONARY_FILE)

# Connect to Memgraph
conn = mgclient.connect(host="127.0.0.1", port=7687)
cursor = conn.cursor()

# Wipe the database by deleting all nodes and relationships
cursor.execute("MATCH (n) DETACH DELETE n")
conn.commit()


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
