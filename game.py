import random
import csv

def read_file_to_list(filename):
    with open(filename, mode='r') as file:
        lines = file.read().splitlines()
    return lines

def read_dictionary_tsv(filename):
    synonym_dict = dict()
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
           if len(row) > 1:
            key = row[0]
            synonym_dict[key] = row[1].split(',')
    return synonym_dict

SYNONYMS = read_dictionary_tsv("data/synonyms.tsv")

def get_synonyms(word):
  if word in SYNONYMS:
    return SYNONYMS[word]
  return []

def game_setup(current, length):
  path = [current]

  for i in range(length):
    # Blow up if the start word is terrible
    synonyms = get_synonyms(current)
    while len(synonyms) == 0:
      path = path[:-1]
      current = path[-1]
      synonyms = get_synonyms(current)

    current = random.choice(synonyms)
    path.append(current)

  return path


def play_the_game(start_word, target_word, num_turns):

  print(f"You can get from {start_word} to {target_word} in {num_turns} steps")
  guess_options = get_synonyms(start_word)

  turns_taken = 0
  game_won = False

  while not game_won and turns_taken < num_turns:
    turns_taken = turns_taken + 1
    print(guess_options)
    guess = input("enter your guess:")
    if not (guess in guess_options): 
      print("not a valid guess")
    else: 
      if guess == target_word:
        game_won = True 
      else: 
        guess_options = get_synonyms(guess)

  if(game_won):
    print("🎉🎉🎉 Hooray 🎉🎉🎉!")


num_turns = 5

starting_word = random.choice(list(SYNONYMS.keys()))

print("Initializing game play!")
path = game_setup(starting_word, num_turns)
print("Secret path")
print(path)
end_word = path[-1]

play_the_game(starting_word, end_word, num_turns)





# put game logic in a function 
# cycles in the synonums 
# history-aware BFS
# number of turns 
# better relationship bw numturns and path length 




