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

Data collection is still in progress.

## Sources

- Game play is currently sourcing synonyms from an [API Ninjas](https://api.api-ninjas.com/v1/thesaurus) thesaurus API. Game play fetches these synonyms on the fly.
- Ultimately, we want to build up our own dictionary of synonyms. Sources include:
  - 20,000 most common words occurring in the English language. Currently stored in `data/first20hours-google-10000-english-20k.txt`. This is sourced from [this repo](https://github.com/first20hours/google-10000-english). There may be profanity included in this list, so tread carefully.
  - The remainder of synonyms are sourced using a subset of sources using the [`wordhoard`](https://wordhoard.readthedocs.io/en/latest/) library (specifically 'merriam-webster', 'synonym.com', 'thesaurus.com'. The remaining sources from wordhoard have too stringent of a CloudFlare DDoS mitigation for the purpose of this project)

## GraphDB:

Data can now be stored and queried using a Memgraph database. This is implemented
using docker (currently).

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
