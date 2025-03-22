import random
import dictionary

SYNONYMS = dictionary.build_dictionary()

def get_synonyms(word):
  if word in SYNONYMS:
    return SYNONYMS[word]
  return []

def game_setup(length):

  path_success = False

  while not path_success:

    current = random.choice(list(SYNONYMS.keys()))
    path = [current]

    seen_words = set([current])

    for _ in range(length):
      synonyms = get_synonyms(current)

      possible_choices = list(set(synonyms).difference(seen_words))
      if len(possible_choices) == 0:
        path_success = False
        break
      current = random.choice(possible_choices)

      seen_words.update(synonyms)
      path.append(current)
    path_success = True

  return path


def play_the_game(path, num_turns):
  start_word = path[0]
  target_word = path[-1]

  print(f"You can get from {start_word} to {target_word} in {num_turns} steps")
  guess_options = get_synonyms(start_word)

  turns_taken = 0
  game_won = False
  taken_guesses = []

  factor = 2

  while not game_won and turns_taken < factor * num_turns:
    turns_taken = turns_taken + 1
    for index, o in enumerate(guess_options):
      print(f"{index}: {o}")

    try:
      guess_index = input("enter your guess: ")
      # TODO: Validate the input
      guess = guess_options[int(guess_index)]
      print(f"You chose: {guess}")
    except KeyboardInterrupt:
      print("quitting game")
      break

    if not (guess in guess_options):
      print("not a valid guess")
    else:
      if guess == target_word:
        game_won = True
      else:
        taken_guesses.append(guess)
        print(f"Guesses so far: {taken_guesses}. Try to get to {target_word}")
        guess_options = get_synonyms(guess)

  if(game_won):
    print("🎉🎉🎉 Hooray 🎉🎉🎉!")

num_turns = 5
print("Initializing game play!")
path = game_setup(num_turns)
print("Secret path")
print(path)

play_the_game(path, num_turns)

# number of turns
# better relationship bw numturns and path length

