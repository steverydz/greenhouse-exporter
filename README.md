# Greenhouse extractor

This project extracts the data from greenhouse and restructures it into a event style database.

The database diagram can be found here: https://miro.com/app/board/o9J_l86oZgU=/

## Populate the database

- Start a postgresql database for local development
- Create a file `.env.local`: `mkdir .env.local`
- In this file add the 2 databases strings (ours and greenhouse's):
```
GREENHOUSE_DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
CANONICAL_DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
```
- `dotrun`
- Have fun querying your new database.