import csv

def read_dictionary_tsv(filename):
    synonym_dict = dict()
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
           if len(row) > 1:
            key = row[0]
            synonym_dict[key] = row[1].split(',')
    return synonym_dict
