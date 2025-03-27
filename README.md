# Thesaurle

Have you ever played [Semantle](https://semantle.com/) and found yourself
frustrated with how it determines of the semantic similarity? Us, too! Many
times, Semantle can feel simply unplayable. We believe this is because it's relying
on the word2vec library which (IIUC) calculates semantic similarity based on
how likely it is for words to appear near each other in a corpus of text. This
doesn't necessarily mean that the words are _semantically_ related.

For Thesaurle, we wanted to take a different approach. Let's source _actual synonyms_
from a variety of sources and build up a game which allows users to navigate
from one word to another by following a path through synonyms.

## Sources / Method

In order to facilitate a more semantically-related experience, we built our own
thesaurus dictionary using the following method:

- Fetch The 20,000 most common words occurring in the English language. This data set was sourced from [this repo](https://github.com/first20hours/google-10000-english).
- Removed "obscene" words by scrubbing words which occur in [LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words](https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/blob/master/en)
- Sourced synonyms using a subset of sources available via the [`wordhoard`](https://wordhoard.readthedocs.io/en/latest/) library (specifically 'merriam-webster', 'synonym.com', 'thesaurus.com'. The remaining sources from wordhoard have too stringent of a CloudFlare DDoS mitigation for the purpose of this project).
- Data was imported into a Memgraph Graph Database for further querying and to
facilitate game play. The game is powered by a number of pre-calculated word pairs
which have a known path and shortest distance.

## Development Notes:

The project takes a dependency on the memgraph docker container and also requires
that textual is installed to power the UI.

To install dependencies:
```
pip install textual
pip install textual-dev
```

To start up the database server:

```
docker-compose up
```

This will start the database server and load the database snapshot. If you need
to connect to the database to run queries or verify data, that can be done using
mgconsole:

```
docker exec -it memgraph mgconsole
```

Data was migrated into the database originally using the migration script:

```
python db/migrate.py
```

This isn't necessary to run if using the docker container, as the database is now
loaded using the database snapshot stored in the `snapshots` directory. If the
snapshot needs to be regenerated for any reason, this can be done by:

- Starting up the memgraph container
- Rerunning the migration script
- Creating the snapshot: `docker exec -it memgraph mgconsole` and then `CREATE SNAPSHOT;`
- Copy the snapshot out of the container and into the repo: `docker cp memgraph:/var/lib/memgraph/snapshot ./snapshots/snapshot`
- Commit!

To migrate data (insert it into the database), run the migration file:
`python db/migrate.py`. This only needs to be run once (unless it changes).

To run sample queries against the database, execute `python sample_queries.py`.

To run the game itself:

- In Debug Mode:
  - Run `textual console` in one window. Printed statements will appear here.
  - Run `textual run --dev app.py` in another window for game play
- In Regular Mode:
  - Run `python app.py`

(Coming in the future: Running the game in the browser via Textual Web?)
