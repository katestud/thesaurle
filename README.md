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

To start up the database server and the console:
```
docker run -p 7687:7687 -d --name memgraph memgraph/memgraph
docker exec -it memgraph mgconsole
```

To migrate data (insert it into the database), run the migration file:
`python db/migrate.py`. This only needs to be run once (unless it changes).
Maybe we need a Makefile.

> [!NOTE]
> The migration step is not super performant. It will take about 8 minutes or
> so to insert all the data into the database. The command currently scrubs
> the database at the start of the command so that it's using a fresh data set,
> but because the command is idempotent (the MERGE command will not overwrite)
> existing data.
> Also note that memgraph only supports one database per machine so we may want
> to ship the database inside of the container to keep it separate from any
> local data. TBD! (We might also be able to get a DB dump and load from there
> rather than inserting but not today, Satan.)

To run sample queries against the database, execute `python sample_queries.py`.

