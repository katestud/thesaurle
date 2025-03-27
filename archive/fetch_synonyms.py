from wordhoard import Synonyms
import csv

CORPUS_FILE = 'data/first20hours-google-10000-english-20k.txt'
NOT_FOUND_FILE = 'data/no_synonyms.txt'
SYNONYMS_FIE = 'data/synonyms.tsv'

def append_to_tsv(filename, data):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(data)

def append_to_file(filename, text):
    with open(filename, mode='a') as file:
        file.write(text + '\n')


def read_first_column(filename):
    first_column = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if row:  # Ensure the row is not empty
                first_column.append(row[0])
    return first_column

def read_file_to_list(filename):
    with open(filename, mode='r') as file:
        lines = file.read().splitlines()
    return lines

def find_and_append_synonym_to_tsv(file_name, word, corpus):
    # sources = ['merriam-webster', 'synonym.com', 'thesaurus.com', 'wordnet', 'collins']
    non_protected_sources = ['merriam-webster', 'synonym.com', 'thesaurus.com']

    synonym = Synonyms(search_string=word,
                   output_format='list',
                   sources = non_protected_sources,
                   max_number_of_requests=200,
                   user_agent=None,
                   proxies=None)
    synonym_results = synonym.find_synonyms()
    if synonym_results == None:
        append_to_file(NOT_FOUND_FILE, word)
        return
    if len(synonym_results) == 0:
        append_to_file(NOT_FOUND_FILE, word)
        return
    filtered = list(set(corpus).intersection(set(synonym_results)))
    append_to_tsv(file_name, [word, ','.join(filtered)])


most_common_words = read_file_to_list(CORPUS_FILE)
no_synonyms = read_file_to_list(NOT_FOUND_FILE)
indexed_words = read_first_column(SYNONYMS_FIE)
print("Indexed Words Count:")
print(len(indexed_words))

words_to_index = list(set(most_common_words) - set(indexed_words) - set(no_synonyms))
print("Remaining words count:")
print(len(words_to_index))

for word in words_to_index:
  print(f"Indexing {word}")
  find_and_append_synonym_to_tsv(SYNONYMS_FIE, word, most_common_words)

