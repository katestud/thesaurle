import random
import mgclient

GUESS_OPTION_COUNT = 8

conn = mgclient.connect(host="127.0.0.1", port=7687)
cursor = conn.cursor()

def fetch_shortest_path(start, end, max_hops=10):
  query = f"""
  MATCH path=(n:Word {{name: $start_word}})-[relationships:SYNONYM *BFS ..{max_hops}]->(m:Word {{name: $end_word}})
  RETURN nodes(path);
  """
  cursor.execute(query, {'start_word': start, 'end_word': end})
  path = []
  for row in cursor.fetchall():
    for item in row[0]:
      path.append(item.properties['name'])

  if len(path) == 0:
    return None

  return path

def get_synonyms(word):
  query = """
  MATCH (a:Word {name: $word})-[r:SYNONYM]->(b:Word)
  RETURN b
  """
  cursor.execute(query, {"word": word})
  results = cursor.fetchall()

  syns = []
  for row in results:
      name = row[0].properties['name']
      syns.append(name)

  return syns

def game_setup():
  lines = open("data/possible_pairs.txt").read().splitlines()
  start,end,_ =random.choice(lines).split(",")

  return fetch_shortest_path(start, end)

def sampled_guesses(guesses, target_word, num_samples):
  print(f"Guesses: {guesses}")
  random.shuffle(guesses)
  sampled_guesses = guesses[:(num_samples - 1)]
  remaining = list(set(guesses) - set(sampled_guesses))
  for guess in remaining:
    path = fetch_shortest_path(guess, target_word)
    if path:
      sampled_guesses.append(guess)
      break

  return sampled_guesses


def play_the_game(path, num_turns):
  start_word = path[0]
  target_word = path[-1]
  dist_to_target = len(path) - 1

  print(f"You can get from {start_word} to {target_word} in {dist_to_target} steps")
  guess_options = sampled_guesses(get_synonyms(start_word), target_word, GUESS_OPTION_COUNT)

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
        shortest_path = fetch_shortest_path(guess, target_word)
        if not shortest_path:
          print(f"Sorry, {guess} is a dead end. Try again")
          continue
        dist_to_target = len(shortest_path) - 1
        print(f"Guesses so far: {taken_guesses}. Try to get to {target_word}. You are at least {dist_to_target} steps away")
        guess_options = sampled_guesses(get_synonyms(guess), target_word, GUESS_OPTION_COUNT)


  if(game_won):
    print("🎉🎉🎉 Hooray 🎉🎉🎉!")

print("Initializing game play!")
path = game_setup()
print("Secret path")
print(path)

play_the_game(path, 5)

# Close connection
conn.close()
