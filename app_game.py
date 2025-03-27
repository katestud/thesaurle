import random
import mgclient


class Game:
    def __init__(self):
        self.dbconn = mgclient.connect(host="127.0.0.1", port=7687)
        self.dbcursor = self.dbconn.cursor()

        lines = open("data/possible_pairs.txt").read().splitlines()
        start, end, _ = random.choice(lines).split(",")

        direct_path = self.fetch_shortest_path(start, end)
        print(direct_path)

        self.initial_path = direct_path
        self.initial_path_length = len(direct_path) - 1
        self.turns_taken = 0
        self.game_won = False
        self.taken_guesses = [(start, len(direct_path) - 1)]
        self.start_word = start
        self.target_word = end
        self.current_word = start
        self.dist_to_target = 0
        self.guess_options = []

    def fetch_shortest_path(self, start, end, max_hops=10):
        query = f"""
  MATCH path=(n:Word {{name: $start_word}})-[relationships:SYNONYM *BFS ..{max_hops}]->(m:Word {{name: $end_word}})
  RETURN nodes(path);
  """
        self.dbcursor.execute(query, {'start_word': start, 'end_word': end})
        path = []
        for row in self.dbcursor.fetchall():
            for item in row[0]:
                path.append(item.properties['name'])

        return path

    def get_synonyms(self, word):
        query = """
  MATCH (a:Word {name: $word})-[r:SYNONYM]->(b:Word)
  RETURN b
  """
        self.dbcursor.execute(query, {"word": word})
        results = self.dbcursor.fetchall()

        syns = []
        for row in results:
            name = row[0].properties['name']
            syns.append(name)

        return syns

    def available_guesses(self):
        self.current_guesses = self.get_synonyms(self.current_word)
        return self.current_guesses

    def send_guess(self, guess):
      self.turns_taken += 1
      if guess == self.target_word:
        self.game_won = True
      else:
        path = self.fetch_shortest_path(guess, self.target_word)
        dist = len(path) - 1

        self.taken_guesses.append((guess, dist))
        self.current_word = guess

    def complete_game(self):
        self.dbconn.close()
