import wordfreq
import random
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_synonyms_api_ninjas(word):
  url = "https://api.api-ninjas.com/v1/thesaurus?word={}".format(word)
  response = requests.get(url, headers={'X-Api-Key': os.getenv('API_NINJAS_KEY')})
  if response.status_code == requests.codes.ok:
    return response.json()["synonyms"]
  else:
    return None

def get_synonyms_subset(word, corpus):
  results = get_synonyms_api_ninjas(word)
  return list(set(corpus).intersection(set(results)))

def choose_synonym(list):
  return random.choice(list)

def game_setup(current, length, corpus):
  path = [current]

  for i in range(length):
    # Blow up if the start word is terrible
    synonyms = get_synonyms_subset(current, corpus)
    while len(synonyms) == 0:
      path = path[:-1]
      current = path[-1]
      synonyms = get_synonyms_subset(current, corpus)

    current = choose_synonym(synonyms)
    path.append(current)

  return path

def take_turn(target_word, guess_options, corpus):
    synonyms = []
    while len(synonyms) == 0:
        guess = input("Enter your guess: ")
        if not (guess in guess_options):
            print("Not a valid guess")
            continue
        if guess == target_word:
            print("You won")
            return []
        synonyms = get_synonyms_subset(guess, corpus)
        if len(synonyms) == 0:
            print("Sorry, that word has no synonyms")
    return synonyms

def play_the_game(starting_word, end_word, num_turns, corpus):
    print(f"You can get from {starting_word} to {end_word} in {num_turns} steps")
    synonyms = get_synonyms_subset(starting_word, corpus)
    for i in range(num_turns):
        print("")
        print(f"Your options are: {synonyms}")
        synonyms = take_turn(end_word, synonyms, corpus)
        if len(synonyms) == 0:
            print("Hooray")
            return
    print("Sorry, you lost!")

common_words = wordfreq.top_n_list('en', 5000)
max_length = 5
start_word = "stand"

print("Initializing game play!")
path = game_setup(start_word, max_length, common_words)
print("Secret path")
print(path)
end_word = path[-1]

play_the_game(start_word, end_word, max_length, common_words)
